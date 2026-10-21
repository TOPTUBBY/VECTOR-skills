# Private full Help corpus

The public skill deliberately does not contain Vector's proprietary Help pages. `scripts/local_corpus.py` builds a **private SQLite index on the user's own machine** from their product installation. Each indexed HTML/CHM/PDF page retains its extracted text, source path, title, and any recognizable `Function Syntax` section. `lookup --full` makes the full locally indexed page, including all examples on that page, available during a supported local agent session. No network, API key, or account is used by the script.

## Build from the provided folder layout

Run from the repository root on Windows:

```powershell
python skills/vector-canoe-vtest/scripts/local_corpus.py build `
  --input "CANoe14=..\CANoe14" `
  --input "vTESTstudio3=..\vTESTstudio3" `
  --input "vTESTstudio6=..\vTESTstudio6" `
  --output ".local-vector-help\corpus.sqlite"
```

The tool recursively reads HTML and text files. On Windows, `hh.exe` decompiles each local CHM to a private cache alongside the database. To include PDF pages, install the optional `pypdf` dependency **locally**: `python -m pip install pypdf`. Without it, PDF files are listed under omissions rather than silently treated as indexed. Nontext assets (images, scripts, binary spreadsheets) are not semantically indexed. Product installations and paths vary; point `--input` to folders you are authorized to use.

If PDF support becomes available after the first build, add PDF pages without rebuilding the HTML/CHM index:

```powershell
python skills/vector-canoe-vtest/scripts/local_corpus.py augment-pdfs `
  --db ".local-vector-help\corpus.sqlite" `
  --input "CANoe14=..\CANoe14" `
  --input "vTESTstudio3=..\vTESTstudio3" `
  --input "vTESTstudio6=..\vTESTstudio6"
```

The `refresh-syntax --db <file>` command recalculates signature fields if this script's section parser is upgraded. The local validation run indexed 51,288 HTML pages, 2,025 PDF pages, and 9 text files across 33 CHMs and 68 PDFs, with zero recorded extraction omissions. Some PDF content may be image-only or have imperfect extraction; use the original PDF for figures and layout.

## Query exact CAPL functions

```powershell
python skills/vector-canoe-vtest/scripts/local_corpus.py lookup --db ".local-vector-help\corpus.sqlite" msTimer --product CANoe14
python skills/vector-canoe-vtest/scripts/local_corpus.py lookup --db ".local-vector-help\corpus.sqlite" writeEx --product CANoe14 --full
python skills/vector-canoe-vtest/scripts/local_corpus.py lookup --db ".local-vector-help\corpus.sqlite" sysGetVariableString --product CANoe14 --full
python skills/vector-canoe-vtest/scripts/local_corpus.py search --db ".local-vector-help\corpus.sqlite" "test configuration" --limit 5
python skills/vector-canoe-vtest/scripts/local_corpus.py stats --db ".local-vector-help\corpus.sqlite"
```

`msTimer` is a type and may be documented under `on timer`/`setTimer`, so search for those entries if an exact-title lookup finds none. `lookup` searches exact titles and matching CAPL function filenames. `search` performs a literal text search across indexed pages. `--full` prints the full **local** page; default output is abbreviated for model context. For CAPL answers, cite the `Source:` path and match the version/service pack. If `stats` lists omissions, disclose them.

## Limits and handling

- A generated database and CHM cache can contain the entire copyrighted Help text. `.gitignore` excludes `.local-vector-help/` and SQLite files. Do not publish, upload, or attach the generated corpus or extracted pages to a public skill.
- This is retrieval, not proof that all function examples have been compiled or validated. Verify event context, overloads, parameters, return codes, and availability in the exact installed version.
- Codex/Claude Code with access to the user's local filesystem can execute the query script. A Gemini Gem cannot execute a local Python script or automatically read a local SQLite database. For a Gem, use its instructions and authorized official online Help, or provide the relevant excerpt under your organization's rules; it is not a standalone mirror of all functions.
- This corpus describes the installed CANoe 14 and vTESTstudio 3/6 sources. It does not synthesize CANoe 19 Help that was not supplied; check Vector's official online Help for that version.
