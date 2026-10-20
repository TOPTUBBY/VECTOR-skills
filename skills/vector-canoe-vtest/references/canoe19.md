# CANoe 19: online Help and version comparison

Checked 2026-10-20 UTC. Vector's [support page](https://www.vector.com/en/services/support/) links to [Product Docs / Help](https://help.vector.com/) and the [CANoe DE Family Help](https://help.vector.com/CANoeDEFamily/index.html). The [release information page](https://www.vector.com/en/services/release-information/) links to [CANoe release notes](https://help.vector.com/CANoeDEFamily/). Direct Help pages returned HTTP 403 in this research environment; their full chapter content was **not** ingested or locally validated. Open them in an authorized browser/Vector account for exact CANoe 19 API and service-pack changes. Vector's current general product page highlights version 20, so its current highlights must not be attributed to 19.

An [official Vector announcement of CANoe 19](https://www.linkedin.com/posts/vectorgrp_canoe-19-release-activity-7336651878094528512-n0bf) describes dashboard-style desktops, .NET 8 development for tests/application models/simulation nodes, CAPL integration into Replay Blocks, and DDS/Connectivity/eMobility enhancements. This is a release overview, not detailed function documentation; check the corresponding 19 service-pack Help before implementing. The [official compatibility matrix](https://www.vector.com/dam/jcr:36d480b6-1246-4f0e-8430-345ea4f9cb22/vTESTstudio_CANoe_Compatibility.pdf) also confirms distinct vTESTstudio 10/11 combinations involving CANoe 19.

| Dimension | Bundled CANoe 14 SP2 source | CANoe 19 evidence and handling |
| --- | --- | --- |
| Help delivery | Installed `Help01/CANoeCANalyzerHTML5/` plus companion CHMs; `Doc/` PDFs | Vector links to online CANoe DE Family Help; exact pages require successful access before detailed claims |
| Desktop | v14 Help documents desktop management | Official v19 announcement highlights dashboard-style desktop layouts |
| .NET test/model/node development | v14 local API and application notes are version-bound | Official v19 announcement highlights .NET 8; do not assume old code or assemblies migrate unchanged |
| Replay/CAPL | v14 has Replay Block and CAPL references | Official v19 announcement highlights CAPL integration into Replay Blocks; inspect the v19 Help for exact event/API behavior |
| DDS / connectivity / eMobility | v14 Help covers its installed domains/options | Official v19 announcement highlights these areas; availability depends on edition, option, and service pack |

Do not present this table as a full v14-to-v19 changelog: intervening versions and complete 19 release notes were not compared chapter by chapter. When online access succeeds, update this file with dated, topic-level links and exact version gates.
