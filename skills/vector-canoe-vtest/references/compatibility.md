# Version compatibility and migration

Primary source: Vector's [CANoe Version to Execute vTESTstudio Test Unit compatibility matrix](https://www.vector.com/dam/jcr:36d480b6-1246-4f0e-8430-345ea4f9cb22/vTESTstudio_CANoe_Compatibility.pdf), dated 2026-10-07. This is a runtime matrix, not a blanket statement that all combinations and features work.

| Builder | Recommended CANoe in matrix | Older minimum candidates when used commands/features permit |
| --- | --- | --- |
| vTESTstudio 3.0 SP3 | 11.0 SP3 | 8.5 SP5, 9.0, 10.0, 11.0 |
| vTESTstudio 6 SP3 / SP4 | 15 SP3 | 12.0, 13.0, 14 |

The matrix explains that for vTESTstudio 2.0 and later, actual Test Table/Test Diagram commands and their parameters determine older-runtime compatibility. Verify individual CAPL/C# APIs and options too. For vTESTstudio 6 SP3 with CANoe 14: target runtime appears in the older-minimum column, but v6 SP3 capabilities may need a newer CANoe. Do not promise support without checking each feature and executing a minimal test.

Local `vTESTstudio6/Help01/vTESTstudio.chm` (`Topics/vTESTstudio/General/NewFeatures.htm`) notes concrete migration hazards: a test design with For loops saved in v5 cannot be loaded by older vTESTstudio versions and requires CANoe 11 SP3 or later; test sequence diagrams with variables from v5 SP3 cannot execute before CANoe 12. v6 SP3 converts obsolete `Auto` loop type to `Float` and offers migration of old database-object function parameter types.

## Review procedure

1. Record exact builder and runtime service packs, installed options, and project backup.
2. List used Test Table/Diagram commands and parameterizations; consult the matrix's detailed tables, then inspect referenced CAPL/C# functions in their versioned Help.
3. Build and execute a tiny representative unit in the target CANoe version; capture compilation/runtime errors, verdict, Test Trace, and report.
4. Make migration edits on a copy. Retest behavior as well as whether the file loads.

Current official matrix may supersede this snapshot. Recheck its date for future work.
