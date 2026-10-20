#!/usr/bin/env python3
"""Search a user's local Vector HTML Help; do not redistribute source pages."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        elif tag in ("p", "h1", "h2", "h3", "li", "tr", "br"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", type=Path, help="Local Help HTML root or a locally decompiled CHM directory")
    ap.add_argument("query", help="Case-insensitive literal phrase")
    ap.add_argument("--limit", type=int, default=20, help="Maximum matching files (default: 20)")
    args = ap.parse_args()
    if not args.root.is_dir() or not args.query.strip() or args.limit < 1:
        ap.error("root must be a directory, query must be nonempty, and limit must be positive")
    needle = args.query.casefold()
    matches = scanned = 0
    for path in sorted(args.root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in (".htm", ".html", ".txt"):
            continue
        scanned += 1
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
            if path.suffix.lower() == ".txt":
                body = raw
            else:
                parser = Text()
                parser.feed(raw)
                body = " ".join(parser.parts)
            body = re.sub(r"\s+", " ", body)
        except (OSError, ValueError):
            continue
        at = body.casefold().find(needle)
        if at < 0:
            continue
        excerpt = body[max(0, at - 95):at + len(args.query) + 140]
        print(f"{path.relative_to(args.root).as_posix()}\n  ...{excerpt}...\n")
        matches += 1
        if matches >= args.limit:
            break
    print(f"Matches displayed: {matches}; files scanned: {scanned}", file=sys.stderr)


if __name__ == "__main__":
    main()
