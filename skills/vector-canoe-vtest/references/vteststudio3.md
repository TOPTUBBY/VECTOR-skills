# vTESTstudio 3.0 SP3: local Help map

The inspected `vTESTstudio3/Help01/vTESTstudio.chm` identifies Version 3.0 SP3. `Doc/vTESTstudio_ConceptManual_EN.pdf` describes the concepts; `Doc/vTESTstudio_MigrationManual_EN.pdf` is useful for older test projects. The `Doc/ReleaseNotes.txt` contains restrictions and workarounds, not a complete feature history.

| Topic | CHM topic path after local decompilation |
| --- | --- |
| Create, build, execute a test unit | `Topics/vTESTstudio/General/TestUnitsCreationExecution.htm` |
| CANoe environment symbols | `Topics/vTESTstudio/General/CANoeInteraction.htm` |
| Editors | `Topics/vTESTstudio/Editors/Editors.htm` |
| Test Table | `Topics/vTESTstudio/Editors/TestTableEditor.htm` |
| Test Diagram | `Topics/vTESTstudio/Editors/TestDiagramEditor/TDE.htm` |
| Parameters and variants | `Topics/vTESTstudio/General/Parameters.htm`, `Variants.htm` |
| Traceability/test case overview | `Topics/vTESTstudio/General/TestCaseOverview.htm` and `Topics/vTESTstudio/REQMTDM/` |
| Exact new features | `Topics/vTESTstudio/General/NewFeatures.htm` |

Version 3.0 introduced project/test-unit case overview, navigation to test design, ribbon and multi-monitor improvements, C# access to CANoe's newer communication concept, and Visual Studio integration. SP3 added runtime-message interface parameters, waveform checkpoints, variant filtering in Path View, and execution-adapter improvements. These are **vTESTstudio 3 features**, not claims about CANoe 19.

The local release notes flag 64-bit signal handling in Test Table commands, symbol-typed interface parameters, CAPL include handling, and limits around variant/property names. Check the installed service pack before applying a workaround.
