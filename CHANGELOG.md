# Changelog

This project versions its **skill content**, independently of CANoe and vTESTstudio product versions. Releases use Semantic Versioning (`MAJOR.MINOR.PATCH`). Major: incompatible skill structure or behavior; minor: new product/version references or substantial guidance; patch: corrections, links, and wording. A tag such as `v0.1.0` marks an immutable skill snapshot.

## 0.3.0 — 2026-10-21

- Added a private local corpus builder and query tool for available HTML Help, locally extracted CHM, text files, and optional PDF text. The supplied folders yielded 51,288 HTML pages, 2,025 PDF pages, and 9 text files from 33 CHMs and 68 PDFs, with zero extraction omissions reported.
- CAPL questions can retrieve a complete version-specific function page, including its syntax and examples, from a user's local installation.
- Documented indexing coverage, omissions, and the restriction on publishing Vector documentation.

## 0.2.0 — 2026-10-21

- Added a CAPL starter reference for `msTimer`, `setTimer`, `on timer`, `writeEx`, `writeLineEx`, and `sysGetVariableString`, verified against the local CANoe 14 SP2 Help.
- Routed CAPL syntax questions to exact versioned Help topics and marked CANoe 19 API details for online verification.

## 0.1.0 — 2026-10-20

- Initial cross-platform skill for Codex/ChatGPT Work, Claude Code, and Gemini Gem.
- Curated local Help maps for CANoe 14 SP2 and vTESTstudio 3.0 SP3 / 6 SP3; added local Help search utility.
- Added official dated vTESTstudio/CANoe compatibility matrix and bounded CANoe 19 online comparison.
- Documented copyright scope and excluded Vector manuals from distribution.
