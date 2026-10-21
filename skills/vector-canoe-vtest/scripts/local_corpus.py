#!/usr/bin/env python3
"""Build and query a PRIVATE, local index of a user's installed Vector Help.

Only this program belongs in the public repository. Its generated database and
extracted CHM files contain third-party documentation and must stay local.
"""

import argparse
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import time


SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
 id INTEGER PRIMARY KEY, product TEXT NOT NULL, kind TEXT NOT NULL,
 source TEXT NOT NULL, title TEXT NOT NULL, syntax TEXT NOT NULL, body TEXT NOT NULL,
 UNIQUE(product, source)
);
CREATE VIRTUAL TABLE IF NOT EXISTS document_search USING fts5(
 title, body, content='documents', content_rowid='id'
);
CREATE TABLE IF NOT EXISTS omissions (
 product TEXT NOT NULL, source TEXT NOT NULL, reason TEXT NOT NULL,
 UNIQUE(product, source)
);
"""


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.title_parts = []
        self.hidden = 0
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg"):
            self.hidden += 1
        elif tag == "title":
            self.in_title = True
        elif tag in ("p", "div", "h1", "h2", "h3", "h4", "li", "tr", "br", "pre"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg") and self.hidden:
            self.hidden -= 1
        elif tag == "title":
            self.in_title = False
        elif tag in ("p", "div", "h1", "h2", "h3", "h4", "li", "tr", "pre"):
            self.parts.append("\n")

    def handle_data(self, data):
        if self.hidden:
            return
        if self.in_title:
            self.title_parts.append(data)
        self.parts.append(data)


def normalize(text):
    lines = [re.sub(r"[ \t\r\f\v]+", " ", line).strip()
             for line in text.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(x for x in lines if x)).strip()


def parse_html(path):
    data = path.read_bytes()
    header = data[:4096].decode("ascii", errors="ignore")
    declared = re.search(r"(?i)charset\s*=\s*['\"]?([\w-]+)", header)
    encoding = declared.group(1) if declared else "utf-8"
    try:
        raw = data.decode(encoding, errors="replace")
    except LookupError:
        raw = data.decode("utf-8", errors="replace")
    if raw.count("\ufffd") > max(3, len(raw) // 100):
        raw = data.decode("cp1252", errors="replace")
    page = Page()
    page.feed(raw)
    title = normalize(" ".join(page.title_parts)) or path.stem
    body = normalize("".join(page.parts))
    return title, body


def syntax_section(body):
    match = re.search(r"(?im)^(?:Function )?Syntax\s*$", body)
    if not match:
        return ""
    section = body[match.end():]
    section = re.split(
        r"(?im)^(?:Function|Method Syntax(?: \(Dynamic\))?|Parameters|Return Values|Availability|Example|Note)\s*$",
        section, maxsplit=1)[0]
    return section.strip()[:6000]


def add_document(db, product, kind, source, title, body):
    syntax = syntax_section(body)
    cursor = db.execute(
        "INSERT OR REPLACE INTO documents(product, kind, source, title, syntax, body) VALUES(?,?,?,?,?,?)",
        (product, kind, source, title, syntax, body))
    db.execute("INSERT INTO document_search(rowid,title,body) VALUES(?,?,?)",
               (cursor.lastrowid, title, body))


def index_html(db, product, root, prefix, counts):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in (".htm", ".html", ".txt"):
            continue
        source = prefix + "/" + path.relative_to(root).as_posix()
        try:
            if path.suffix.lower() == ".txt":
                title, body = path.name, path.read_text(encoding="utf-8", errors="replace")
            else:
                title, body = parse_html(path)
            if body.strip():
                add_document(db, product, "text" if path.suffix.lower() == ".txt" else "html",
                             source, title, body)
                counts[(product, path.suffix.lower())] += 1
        except (OSError, UnicodeError, ValueError) as exc:
            db.execute("INSERT OR REPLACE INTO omissions VALUES(?,?,?)",
                       (product, source, "read/parse: " + str(exc)[:200]))


def decompile_chm(chm, dest):
    if any(dest.rglob("*.htm")):
        return True
    exe = shutil.which("hh.exe")
    if not exe:
        return False
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run([exe, "-decompile", str(dest), str(chm)],
                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   timeout=120)
    stable = 0
    prior = -1
    for _ in range(60):
        count = sum(1 for _ in dest.rglob("*.htm"))
        if count and count == prior:
            stable += 1
        else:
            stable = 0
        if stable >= 2:
            return True
        prior = count
        time.sleep(1)
    return False


def index_pdf(db, product, path, source, counts):
    already = db.execute("SELECT 1 FROM documents WHERE product=? AND source LIKE ? LIMIT 1",
                         (product, source + "#page=%")).fetchone()
    if already:
        return
    try:
        from pypdf import PdfReader  # Optional local-only dependency.
    except ImportError:
        db.execute("INSERT OR REPLACE INTO omissions VALUES(?,?,?)",
                   (product, source, "pypdf unavailable; install locally with python -m pip install pypdf"))
        return
    try:
        reader = PdfReader(str(path))
        for number, page in enumerate(reader.pages, 1):
            body = page.extract_text() or ""
            if body.strip():
                add_document(db, product, "pdf", f"{source}#page={number}",
                             f"{path.name} — page {number}", body)
                counts[(product, ".pdf pages")] += 1
        db.execute("DELETE FROM omissions WHERE product=? AND source=?", (product, source))
    except Exception as exc:
        db.execute("INSERT OR REPLACE INTO omissions VALUES(?,?,?)",
                   (product, source, "PDF extraction: " + str(exc)[:200]))


def connect(path):
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    return db


def build(args):
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    cache = args.cache.resolve() if args.cache else output.parent / "extracted-chm"
    sources = []
    for item in args.input:
        if "=" not in item:
            raise SystemExit("--input needs LABEL=PATH")
        product, location = item.split("=", 1)
        root = Path(location).resolve()
        if not product.strip() or not root.is_dir():
            raise SystemExit(f"Missing source directory: {item}")
        if output == root or root in output.parents:
            raise SystemExit("Place the database outside the source directory")
        sources.append((product.strip(), root))

    # Build into a new database so a failed build never corrupts the previous one.
    temporary = output.with_suffix(output.suffix + ".building")
    if temporary.exists():
        raise SystemExit(f"Incomplete build exists: {temporary}; inspect it first")
    db = connect(temporary)
    counts = Counter()
    try:
        for product, root in sources:
            print(f"Indexing {product}: {root}", flush=True)
            index_html(db, product, root, "local", counts)
            db.commit()
            if not args.skip_chm:
                for chm in root.rglob("*.chm"):
                    relative = chm.relative_to(root).as_posix()
                    dest = cache / product / relative.removesuffix(".chm")
                    print(f"  CHM {relative}", flush=True)
                    if decompile_chm(chm, dest):
                        index_html(db, product, dest, "chm/" + relative, counts)
                    else:
                        db.execute("INSERT OR REPLACE INTO omissions VALUES(?,?,?)",
                                   (product, relative, "CHM decompiler unavailable or extraction failed"))
                    db.commit()
            if not args.skip_pdf:
                for pdf in root.rglob("*.pdf"):
                    index_pdf(db, product, pdf, pdf.relative_to(root).as_posix(), counts)
                db.commit()
        print("Indexed:", dict(sorted((f"{p} {k}", v) for (p, k), v in counts.items())), flush=True)
        print("Omissions:", db.execute("SELECT COUNT(*) FROM omissions").fetchone()[0], flush=True)
    finally:
        db.close()
    temporary.replace(output)
    print(f"Private database: {output}", flush=True)


def display(row, full=False, max_chars=1600):
    product, kind, source, title, syntax, body = row
    print(f"\n{title} [{product} | {kind}]\nSource: {source}")
    if syntax:
        print("Syntax:\n" + syntax)
    print("Local Help text:\n" + (body if full else body[:max_chars]))
    if not full and len(body) > max_chars:
        print(f"… {len(body) - max_chars} more characters; use --full for the local page")


SECTION_NAMES = {
    "function syntax": "syntax", "syntax": "syntax", "method syntax": "syntax",
    "function": "purpose", "description": "purpose", "parameters": "parameters", "parameter": "parameters",
    "return values": "return_values", "return value": "return_values",
    "availability": "availability", "availability canoe": "availability",
    "availability vteststudio": "availability", "example": "examples", "examples": "examples",
    "note": "notes", "notes": "notes", "version extensions": "version_extensions",
}


def function_card(row):
    """Separate exact local topic sections; retain the full page for ambiguous layouts."""
    product, kind, source, title, syntax, body = row
    sections = {}
    current = None
    for line in body.splitlines():
        key = " ".join(line.casefold().split())
        if key in SECTION_NAMES:
            current = SECTION_NAMES[key]
            sections.setdefault(current, [])
        elif key in ("see also", "related topics", "class"):
            current = None
        elif current:
            # Product/version footer ends the topic's functional sections.
            if re.fullmatch(r"Version\s+\d+.*", line) or line.startswith("©"):
                current = None
            else:
                sections[current].append(line)
    fields = {key: "\n".join(lines).strip() for key, lines in sections.items() if lines}
    if syntax and not fields.get("syntax"):
        fields["syntax"] = syntax
    return {"product": product, "kind": kind, "title": title, "source": source,
            "fields": fields, "section_parser": "best-effort; inspect the full topic"}


def exact_rows(db, name, product=None, limit=20):
    return db.execute("""
      SELECT product, kind, source, title, syntax, body FROM documents
      WHERE (lower(title)=lower(?) OR lower(source) LIKE lower(?))
        AND (? IS NULL OR lower(product)=lower(?))
      ORDER BY CASE WHEN lower(title)=lower(?) THEN 0 ELSE 1 END,
        CASE WHEN source LIKE 'local/%' THEN 0 ELSE 1 END, product, source
      LIMIT ?
    """, (name, "%/caplfunction" + name + ".htm", product, product, name, limit)).fetchall()


def card(args):
    with connect(args.db) as db:
        rows = exact_rows(db, args.name, args.product, args.limit)
    cards = [function_card(row) for row in rows]
    if args.json:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
    else:
        for item in cards:
            print(f"\n{item['title']} [{item['product']}]\nSource: {item['source']}")
            for key, value in item["fields"].items():
                print(f"{key}:\n{value[:args.max_chars]}")
                if len(value) > args.max_chars:
                    print(f"… {len(value) - args.max_chars} more characters; use --max-chars")
        print(f"\nMatches: {len(cards)}; parsed sections need confirmation in lookup --full")


def compare(args):
    with connect(args.db) as db:
        rows = exact_rows(db, args.name, limit=100)
    by_product = {}
    for row in rows:
        by_product.setdefault(row[0], function_card(row))
    for product, item in sorted(by_product.items()):
        print(f"{product} | {item['source']}\n  Syntax: {item['fields'].get('syntax', '(not parsed)')}")
    signatures = {p: c["fields"].get("syntax", "") for p, c in by_product.items()}
    normalized = {"\n".join(line.strip().rstrip(";") for line in value.splitlines())
                  for value in signatures.values()}
    print(f"Comparison: {'same extracted signature after punctuation normalization' if len(normalized) == 1 and all(signatures.values()) else 'different or missing extracted syntax'}")
    print("This compares local text only; check overloads, semantics, applicability, and current official Help.")


def lookup(args):
    with connect(args.db) as db:
        # Exact title first; filenames provide a fallback for differently cased titles.
        rows = db.execute("""
          SELECT product, kind, source, title, syntax, body FROM documents
          WHERE (lower(title)=lower(?) OR lower(source) LIKE lower(?))
            AND (? IS NULL OR lower(product)=lower(?))
          ORDER BY CASE WHEN lower(title)=lower(?) THEN 0 ELSE 1 END, product, source
          LIMIT ?
        """, (args.name, "%/caplfunction" + args.name + ".htm", args.product,
              args.product, args.name, args.limit)).fetchall()
        for row in rows:
            display(row, args.full, args.max_chars)
        print(f"\nMatches: {len(rows)}")


def search(args):
    with connect(args.db) as db:
        pattern = "%" + args.query.lower().replace("%", "\\%").replace("_", "\\_") + "%"
        rows = db.execute("""
          SELECT product, kind, source, title, syntax, body FROM documents
          WHERE (lower(title) LIKE ? ESCAPE '\\' OR lower(body) LIKE ? ESCAPE '\\')
            AND (? IS NULL OR lower(product)=lower(?))
          LIMIT ?
        """, (pattern, pattern, args.product, args.product, args.limit)).fetchall()
        for row in rows:
            display(row, args.full, args.max_chars)
        print(f"\nMatches: {len(rows)}")


def stats(args):
    with connect(args.db) as db:
        for product, kind, count in db.execute(
                "SELECT product, kind, count(*) FROM documents GROUP BY product, kind ORDER BY product, kind"):
            print(f"{product}: {kind} {count}")
        omissions = db.execute("SELECT product, source, reason FROM omissions ORDER BY product, source").fetchall()
        print(f"Omissions: {len(omissions)}")
        for item in omissions[:args.limit]:
            print("  ", *item, sep=" | ")


def augment_pdfs(args):
    counts = Counter()
    with connect(args.db) as db:
        for item in args.input:
            if "=" not in item:
                raise SystemExit("--input needs LABEL=PATH")
            product, location = item.split("=", 1)
            root = Path(location).resolve()
            if not root.is_dir():
                raise SystemExit(f"Missing source directory: {item}")
            for pdf in root.rglob("*.pdf"):
                index_pdf(db, product, pdf, pdf.relative_to(root).as_posix(), counts)
            db.commit()
    print("Added PDF pages:", dict(counts), flush=True)


def refresh_syntax(args):
    count = 0
    with connect(args.db) as db:
        for id_, body in db.execute("SELECT id,body FROM documents WHERE kind='html'"):
            syntax = syntax_section(body)
            if syntax:
                db.execute("UPDATE documents SET syntax=? WHERE id=?", (syntax, id_))
                count += 1
        db.commit()
    print(f"Function syntax sections refreshed: {count}")


def main():
    # Windows legacy consoles may default to a code page that cannot print Help text.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build", help="Index locally owned documentation")
    b.add_argument("--input", action="append", required=True, metavar="LABEL=PATH")
    b.add_argument("--output", type=Path, required=True)
    b.add_argument("--cache", type=Path, help="Local CHM extraction directory")
    b.add_argument("--skip-chm", action="store_true")
    b.add_argument("--skip-pdf", action="store_true")
    b.set_defaults(func=build)
    for command, function in (("lookup", lookup), ("search", search)):
        q = sub.add_parser(command)
        q.add_argument("--db", type=Path, required=True)
        q.add_argument("name" if command == "lookup" else "query")
        q.add_argument("--product", help="Limit to a source label")
        q.add_argument("--limit", type=int, default=5)
        q.add_argument("--max-chars", type=int, default=1600)
        q.add_argument("--full", action="store_true", help="Show entire local page")
        q.set_defaults(func=function)
    c = sub.add_parser("card", help="Extract sections from an exact local function topic")
    c.add_argument("--db", type=Path, required=True)
    c.add_argument("name")
    c.add_argument("--product")
    c.add_argument("--limit", type=int, default=5)
    c.add_argument("--max-chars", type=int, default=3000)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=card)
    c = sub.add_parser("compare", help="Compare local function signatures by product label")
    c.add_argument("--db", type=Path, required=True)
    c.add_argument("name")
    c.set_defaults(func=compare)
    s = sub.add_parser("stats", help="Show index coverage and omissions")
    s.add_argument("--db", type=Path, required=True)
    s.add_argument("--limit", type=int, default=15)
    s.set_defaults(func=stats)
    a = sub.add_parser("augment-pdfs", help="Add missing PDF text to an existing private database")
    a.add_argument("--db", type=Path, required=True)
    a.add_argument("--input", action="append", required=True, metavar="LABEL=PATH")
    a.set_defaults(func=augment_pdfs)
    f = sub.add_parser("refresh-syntax", help="Re-extract API signatures after a parser update")
    f.add_argument("--db", type=Path, required=True)
    f.set_defaults(func=refresh_syntax)
    args = p.parse_args()
    if args.command != "build" and not args.db.is_file():
        p.error(f"Database not found: {args.db}; run build first")
    args.func(args)


if __name__ == "__main__":
    main()
