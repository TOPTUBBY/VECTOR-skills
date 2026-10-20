# vTESTstudio 6 SP3: local Help map

The inspected `vTESTstudio6/Help01/vTESTstudio.chm` identifies Version 6 SP3. Its `Doc/vTESTstudio_ConceptManual_EN.pdf` and `Doc/ReleaseNotes.txt` complement the CHM. `Help01/VectorCANoeNETAPI.chm` is a separate API reference.

## Core lifecycle

`Topics/vTESTstudio/General/TestUnitsCreationExecution.htm` describes source/parameter files -> Build -> `.vtuexe` -> CANoe Test Setup for Test Units -> test configuration -> Test Trace/report. Editable parameters may be placed next to `.vtuexe` in a `.SRC` directory if configured. `Topics/vTESTstudio/General/CANoeInteraction.htm` describes database and system-variable symbols from the CANoe environment. Confirm the executable's actual source and report paths in the user's project.

| Task | CHM topic |
| --- | --- |
| Editors and test-table commands | `Topics/vTESTstudio/Editors/Editors.htm`, `Topics/vTESTstudio/Editors/TestTableEditor.htm`, `Topics/TestCommands/` |
| Test Diagram / State Diagram | `Topics/vTESTstudio/Editors/TestDiagramEditor/TDE.htm`, `Topics/vTESTstudio/Editors/StateDiagramEditor/` |
| Parameters / variants | `Topics/vTESTstudio/General/Parameters.htm`, `Topics/vTESTstudio/General/Variants.htm` |
| Test tree, reports, requirements | `Topics/vTESTstudio/General/ExecutionTreeSetup.htm`, `Topics/vTESTstudio/REQMTDM/` |
| Feature chronology | `Topics/vTESTstudio/General/NewFeatures.htm` |

## Differences visible in the bundled Help

- v4 added CAPL parallel test execution, test execution plan export, and a vTESTstudio Viewer with CANoe 12.
- v4 SP3 added a Fuzz Test Cases command; v5 added Distributed Objects, parameter types for messages/nodes/networks, and further fuzzing options.
- v5 SP3 documented a TestUnitBuildCLI add-on and encrypted CAPL sources; these require the relevant installation/add-on.
- v6 added composite states, background checks inside loops, `.NET Framework 4.7` target selection, and Distributed Object string data members in test commands.
- v6 SP3 added system-variable fuzz inputs, decision paths in state diagrams, test case descriptions from sequence diagrams, and migration of obsolete `DbNetwork`, `DbNode`, `DbMsg` function parameters to network-specific types. Obsolete `Auto` For-loop type is converted to `Float`.

The local release notes also state that XML test module import was discontinued since v4 SP3. Do not recommend this route for v6 without checking a supported migration path. Check CANoe runtime compatibility separately; the presence of a command in the editor does not establish support in CANoe 14.
