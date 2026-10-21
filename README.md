# VECTOR Skills

**Community AI skills for Vector CANoe and vTESTstudio**  
Maintainer: **Patiphan Phakdeeburi (TOPTUBBY)** · Skill version: **0.4.0** · [MIT license](LICENSE)

> คู่มือช่วยให้ AI แยกบทบาท CANoe กับ vTESTstudio, อ้างอิงเอกสารตามเวอร์ชัน, และตรวจ compatibility ก่อนแนะนำขั้นตอนหรือเขียน CAPL/test unit เอกสารต้นฉบับของ Vector อยู่ในเครื่องผู้ใช้และไม่ได้อัปโหลดลงรีโปสาธารณะ

![CANoe and vTESTstudio workflow](assets/workflow.svg)

## What it covers

| Product | Studied source | Tasks covered |
| --- | --- | --- |
| CANoe 14 SP2 | Local `Help01` HTML/CHM and `Doc` references | Simulation vs test setup, network nodes, CAPL navigation, diagnostics, logs, COM/.NET, Test Trace |
| vTESTstudio 3.0 SP3 | Local Help CHM, concept/migration manuals and release notes | Test editors, parameters/variants, build and `.vtuexe`, traceability |
| vTESTstudio 6 SP3 | Local Help CHM, concept manual and release notes | Newer test design, Distributed Objects, fuzzing, state diagrams, migration caveats |
| CANoe 19 | Vector's online Help/release links, official announcement, compatibility matrix | Bounded comparison to 14, links to verify current details; no claim of full v19 Help ingestion |

The [CAPL basics guide](skills/vector-canoe-vtest/references/capl-basics.md) now covers `msTimer`, `setTimer`, `on timer`, `writeEx`, and `sysGetVariableString` with CANoe 14 SP2 syntax, short examples, and local Help topic paths. It is a starter guide, not a complete function catalog; the skill instructs an AI to check the matching Help for any other function or version.

**Full function coverage from your own installation:** [build a private local corpus](skills/vector-canoe-vtest/references/local-corpus.md) with `local_corpus.py`. It indexes supplied HTML Help and locally extracted CHM pages, preserves each page's full local text and examples, and extracts recognizable function syntax for exact-name lookup. Optional `pypdf` adds PDF page text. Run `stats` to see exact indexed counts and omissions; the public repository does not contain the generated corpus.

For a function question, `card` separates the matching topic into syntax, purpose, parameters, return values and availability; `lookup --full` retains the exact local page for checking parser errors; `compare` displays extracted signatures across supplied products. The [answer protocol](skills/vector-canoe-vtest/references/answer-protocol.md) then checks the original topic and an independent official source for the exact version and CAPL context. These tools cover indexed text, not a manually verified catalog of every API. The [domain map](skills/vector-canoe-vtest/references/domain-map.md) routes broader CANoe and vTESTstudio questions to their source categories.

In the supplied local folders, the builder indexed **51,288 HTML pages**, **2,025 extracted PDF pages**, and **9 text files** across CANoe 14 and vTESTstudio 3/6; all **33 CHMs** and **68 PDFs** were processed with **zero reported text-extraction omissions**. These numbers include overlapping Help copies, not that many unique APIs. Images, JavaScript, CSS, binary spreadsheets, and the unsupplied CANoe 19 Help are outside this text index. The generated private database is about 160 MB and is ignored by Git.

The source folders provided for analysis contained **8,375** CANoe HTML topics, **2,924** vTESTstudio 3 CHM HTML topics, **3,853** vTESTstudio 6 CHM HTML topics, and 57 PDFs in CANoe `Doc`. These are inventory counts, not a claim that every line has been manually reviewed. The published skill is an original, curated navigation and workflow layer. See [source register](skills/vector-canoe-vtest/references/sources.md).

### CANoe versus vTESTstudio

| CANoe | vTESTstudio |
| --- | --- |
| Configure network, hardware, bus, measurement, analysis and simulation | Design test cases and sequences with Test Table/Diagram/State Diagram, CAPL or C# |
| Run CAPL network nodes in Simulation Setup | Build test units into `.vtuexe` |
| Execute test units in Test Setup for Test Units; view Test Trace and reports | Maintain test parameters, variants, and traceability |

An older CANoe **test environment** (`*.TSE`) is distinct from the newer test-unit setup. The exact choice depends on the user's configuration and version.

## Repository structure

```text
VECTOR-skills/
├── .agents/skills/vector-canoe-vtest/SKILL.md   # Codex repository entry
├── .claude/skills/vector-canoe-vtest/SKILL.md  # Claude Code entry
├── skills/vector-canoe-vtest/
│   ├── SKILL.md                                # Canonical instructions
│   ├── references/                            # Versioned, original summaries
│   └── scripts/                              # Build/query private local Help corpus
├── gemini/GEM_INSTRUCTIONS.md                 # Paste into a Gemini Gem
├── assets/workflow.svg                        # Original diagram
├── VERSION
├── CHANGELOG.md
└── LICENSE
```

The wrappers link to the canonical skill so cross-platform guidance stays consistent. They need the **whole repository** or a copy preserving the relative paths. No Vector proprietary manuals are bundled. `skills/vector-canoe-vtest/scripts/local_corpus.py` builds a private resource from the user's own installed Help.

### Build the comprehensive private resource locally

From the repository root, with the three source folders next to the repository:

```powershell
python skills/vector-canoe-vtest/scripts/local_corpus.py build `
  --input "CANoe14=..\CANoe14" `
  --input "vTESTstudio3=..\vTESTstudio3" `
  --input "vTESTstudio6=..\vTESTstudio6" `
  --output ".local-vector-help\corpus.sqlite"

python skills/vector-canoe-vtest/scripts/local_corpus.py lookup `
  --db ".local-vector-help\corpus.sqlite" sysGetVariableString `
  --product CANoe14 --full

python skills/vector-canoe-vtest/scripts/local_corpus.py card `
  --db ".local-vector-help\corpus.sqlite" writeEx --product CANoe14

python skills/vector-canoe-vtest/scripts/local_corpus.py compare `
  --db ".local-vector-help\corpus.sqlite" sysGetVariableString

python skills/vector-canoe-vtest/scripts/local_corpus.py stats `
  --db ".local-vector-help\corpus.sqlite"
```

The resource stays on your computer. For PDFs, install `pypdf` locally first; otherwise PDF files are reported as omissions. On Windows, the tool uses `hh.exe` to extract local CHMs into an ignored cache. Images, executable scripts, and binary spreadsheets are not converted into searchable text. See [build/query/coverage details](skills/vector-canoe-vtest/references/local-corpus.md).

## Install and use

### ChatGPT Work / Codex

Clone or download the repository. In a Codex project, keep `.agents/skills/vector-canoe-vtest/SKILL.md` and the canonical `skills/` folder together, or copy the **entire** `skills/vector-canoe-vtest/` directory into the Codex skills location configured for your installation. If ChatGPT Work offers custom skill import, import that complete canonical skill directory through its UI. In a chat, ask: “Use the vector-canoe-vtest skill to explain a CANoe 14 CAPL test node.” Check your Work environment's current skill-import workflow; a GitHub URL alone does not automatically install a skill.

### Claude Code

Clone the repository into your project so Claude Code can discover `.claude/skills/vector-canoe-vtest/SKILL.md` and follow its relative link to `skills/vector-canoe-vtest/`. For a global installation, copy the canonical directory to your user-level Claude skills directory instead. Ask Claude to use `vector-canoe-vtest` and specify the exact product versions.

### Gemini Gem

Create a Gem, paste the block in [GEM_INSTRUCTIONS.md](gemini/GEM_INSTRUCTIONS.md) into its **Instructions**, and optionally attach the original `skills/vector-canoe-vtest/references/*.md` as knowledge. Re-upload these reference files after updating the Gem. A Gem does not execute the repository's `SKILL.md` or access the private local corpus; full offline lookup is available to coding agents with access to the local files, not to a standalone Gem.

### Search your own installed Help

On Windows, from the repository root (Python 3, standard library only):

```powershell
python skills/vector-canoe-vtest/scripts/search_help.py "C:\Program Files\Vector CANoe 14\Help01\CANoeCANalyzerHTML5\Content\Topics" "test configuration" --limit 10
```

Adjust the path to your installation. To search a **locally owned** CHM after extraction:

```powershell
hh.exe -decompile "C:\Temp\vtest6-help" "C:\path\to\vTESTstudio.chm"
python skills/vector-canoe-vtest/scripts/search_help.py "C:\Temp\vtest6-help\Topics" "test unit" --limit 10
```

Do not commit extracted Help or PDFs. The search utility emits short local snippets; confirm the whole topic and service pack in the original Help.

## Version compatibility example

Vector's [compatibility matrix dated 7 October 2026](https://www.vector.com/dam/jcr:36d480b6-1246-4f0e-8430-345ea4f9cb22/vTESTstudio_CANoe_Compatibility.pdf) lists CANoe **15 SP3** as recommended for a vTESTstudio **6 SP3** unit and lists **CANoe 14** among older minimum candidates. Execution on CANoe 14 still depends on the commands and parameters actually used, plus CAPL/C# APIs and options. See [compatibility and migration](skills/vector-canoe-vtest/references/compatibility.md).

## CANoe 19 online Help and evidence boundary

Vector links to the [CANoe DE Family online Help](https://help.vector.com/CANoeDEFamily/index.html) and [release notes](https://www.vector.com/en/services/release-information/). Direct Help content returned HTTP 403 to the research environment on 20 October 2026, so this release does **not** claim exhaustive CANoe 19 API coverage. The [CANoe 19 reference](skills/vector-canoe-vtest/references/canoe19.md) compares only verified high-level items with the local CANoe 14 SP2 material and instructs the AI to open the exact online Help topic when accessible. Vector's current product page highlights CANoe 20; those items are not ascribed to 19.

## Example prompts

- “CANoe 14 SP2: explain Network Node vs Test Unit and where each CAPL file belongs.”
- “vTESTstudio 6 SP3 + CANoe 14: review these Test Table commands for runtime compatibility.”
- “My `.vtuexe` builds but fails when added to CANoe. Give a diagnosis checklist with Help topics.”
- “Compare CANoe 14 and 19 for this specific Replay Block workflow; mark unverified APIs.”

## Releases, authorship, and rights

Skill releases use [Semantic Versioning](CHANGELOG.md) and the root [VERSION](VERSION) file; Git tags `vX.Y.Z` can identify published snapshots. Product versions are separate: **skill v0.4.0** is not CANoe 0.4.0. Contributions should identify the product version/service pack, source URL or local topic path, and verification status. Do not submit Vector copyrighted manuals, extracted CHMs, generated private databases, or screenshots without permission.

Created and maintained by **Patiphan Phakdeeburi (TOPTUBBY)**. The repository's original code and written skill content are MIT licensed. **Vector**, **CANoe**, and **vTESTstudio** are names of Vector Informatik GmbH; the project is independent and is not endorsed by Vector. The MIT license does not apply to Vector's documentation or software.

Vector's [terms and conditions](https://www.vector.com/en/company/get-info/terms-and-conditions/) say that copying/distributing Vector-provided content requires express authorization. This repository therefore distributes the indexing tool and original guidance, while the user's generated Help corpus remains private on their own computer.
