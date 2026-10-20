# CANoe 14 SP2: local Help map

Source root: `CANoe14/Help01/CANoeCANalyzerHTML5/Content/Topics/`. The inspected HTML topics identify themselves as Version 14 SP2. `CANoe14/Doc/` contains quick starts, application notes, format specifications, and VT System manuals; use those for task-specific detail. `Help01/` also contains companion CHMs for .NET API, licensing, Vector tools, protocols, and more. Do not confuse this documentation layout with executable binaries.

## Where to look

| Task | Local topic or document |
| --- | --- |
| Network node concept | `CANoeCANalyzer/General/HELP_NETNODES.htm` |
| Test units and their configuration | `CANoeCANalyzer/Windows/TestConfigurations/TC.htm` |
| Legacy test environment/test modules | `CANoeCANalyzer/Windows/TestEnvironments/TestEnvironment.htm` |
| General test functions | `CANoeCANalyzer/Test/` and `TestCommands/` |
| CAPL signatures by bus | `CAPLFunctions/<bus>/` |
| COM automation | `COMInterface/` and `Doc/AN-AND-1-117_CANalyzer_CANoe_as_a_COM_server.pdf` |
| .NET interface | `Help01/VectorCANoeNetAPI.chm` and `Doc/AN-IND-1-011_Using_CANoe_NET_API.pdf` |
| Diagnostics / DoIP | `CANoeCANalyzer/Diagnostics/`, `Doc/AN-IND-1-001_CANoe_CANalyzer_as_Diagnostic_Tools.pdf`, `Doc/AN-IND-1-026_DoIP_in_CANoe.pdf` |
| ASC and BLF logs | `Doc/LoggingFormat_ASCII/`, `Doc/LoggingFormat_BLF/` |
| Intro / feature history | `Doc/CANoe_QuickStartExport_EN.pdf`, `CANoeCANalyzer/NewFeatures/NewFeatures.htm` |

`Help01/CANoeCANalyzerHTML5/` is a locally bundled browser Help application. `Doc/` is a collection of separate PDF references, not a replacement for the Help's function reference.

## Roles and execution

- **Network node**: a controller/system component with receive/transmit and I/O behavior, represented in Simulation Setup; CAPL can implement event-driven behavior. Source: `General/HELP_NETNODES.htm`.
- **Test unit**: a unit in a CANoe test configuration. The Test Setup for Test Units manages configurations and Test Trace windows; test units in one configuration execute sequentially. Source: `Windows/TestConfigurations/TC.htm`.
- **Test environment**: legacy `*.TSE` tree of test blocks, generators, and replay elements under Test Setup for Test Modules. A shared TSE file can affect multiple CANoe configurations. Source: `Windows/TestEnvironments/TestEnvironment.htm`.
- A CAPL network node that sends an ECU response and a CAPL test module that waits/checks for that response serve different execution roles. Name the intended placement explicitly in any code answer.

For exact CAPL APIs, open the relevant `CAPLFunctions` topic. A function present in CANoe 14 is not automatically supported in another runtime context or in CANoe 19 with identical behavior.
