# Coverage map for the supplied documentation

The private index covers searchable text in all supplied `Help01` and `Doc` trees for CANoe 14 SP2, vTESTstudio 3.0 SP3 and vTESTstudio 6 SP3. Use this map to find a source category, then retrieve its specific topic. The counts include duplicate CHM/HTML copies; zero recorded extraction omissions does not mean every diagram or code example was manually checked.

| Question | CANoe 14 source and role | vTESTstudio 3/6 source and role |
| --- | --- | --- |
| Network behavior | `CANoeCANalyzerHTML5/Content/Topics/CANoeCANalyzer/`, network and measurement configuration, analysis windows, diagnostics and logging | `Topics/vTESTstudio/General/CANoeInteraction.htm` describes the CANoe environment and symbols consumed by test design |
| CAPL syntax | `Content/Topics/CAPLFunctions/` by bus and function family; exact signatures, parameters, availability, examples when present | CHM `Topics/CAPLFunctions/` covers CAPL as used by test units; confirm its context separately from a simulation node |
| Test execution | CANoe Test Setup for Test Units, test configurations, test traces; legacy Test Environment has a separate workflow | `TestUnitsCreationExecution.htm`, editors and `Topics/TestCommands/`; build `.vtuexe`, load/run in CANoe |
| Test modeling | CANoe runs and analyzes tests | Test Table, Test Diagram, State Diagram, CAPL/C#; parameters, variants, requirements, reports |
| Automation and integration | COM and .NET CHMs/application notes; network databases, channels and hardware | Build CLI, source/test-unit integration and CANoe interaction, subject to version/add-on availability |
| Background and migration | `Doc` quick starts, format and diagnostic application notes, VT System references | `Doc` Concept Manual, release notes, installation/licensing and migration information |

The main cross-product boundary: CANoe owns the configured measurement/simulation/test runtime; vTESTstudio authors and builds test units for CANoe execution. A CAPL function page may describe a particular program type or setup placement. Do not assume the same API works in a test unit because it works in a simulation node.

CANoe 19 was not present in the supplied folders. Its [online Help](https://help.vector.com/CANoeDEFamily/index.html) and release notes are a separate current source. The local CANoe 14 index cannot certify CANoe 19 syntax or behavior. See [compatibility](compatibility.md) for the dated vTESTstudio/CANoe matrix and command-level checks.
