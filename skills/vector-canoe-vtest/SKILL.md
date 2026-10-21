---
name: vector-canoe-vtest
description: Assist with Vector CANoe configuration, CAPL, network simulation, measurement, diagnostics, test nodes, vTESTstudio test design, VTUEXE execution, version compatibility, and troubleshooting. Use when a task involves CANoe 14, CANoe 19, vTESTstudio 3 or 6, or their interaction.
---

# Vector CANoe and vTESTstudio

## First choose product and version

1. Identify the installed CANoe version/service pack, vTESTstudio version/service pack, bus/option, hardware, and whether the task is simulation, analysis, diagnostics, or test execution. Ask only for missing facts that change the answer; otherwise state assumptions.
2. Treat CANoe as the runtime for measurement, simulation, diagnostics, and tests. Treat vTESTstudio as the test design and build environment. A network node simulates behavior in CANoe's Simulation Setup; a test unit executes checks and stimuli in a CANoe test configuration. Do not conflate these roles.
3. For CAPL syntax questions, start with [CAPL basics](references/capl-basics.md), then check the named Help topic. For CANoe 14 details read [CANoe 14](references/canoe14.md). For vTESTstudio 3 or 6 read the corresponding [v3](references/vteststudio3.md) or [v6](references/vteststudio6.md) reference. For cross-version execution and migration always read [compatibility](references/compatibility.md). For CANoe 19 and source limitations read [CANoe 19](references/canoe19.md).

## Work from evidence

- Use this skill as a navigational and procedural guide, not a substitute for the installed product help. Consult the exact local Help topic, current official online Help, and version-specific release/compatibility notes before asserting an API signature, menu name, license requirement, or supported feature.
- The user's local source folders, when available, are `CANoe14/Doc`, `CANoe14/Help01`, `vTESTstudio3/Doc`, `vTESTstudio3/Help01`, `vTESTstudio6/Doc`, and `vTESTstudio6/Help01`. Their documents are **not distributed** with this skill. Search locally with `scripts/search_help.py` or the product Help search. CHM may be decompiled for local indexing on Windows with `hh.exe -decompile <destination> <file.chm>`; never commit the extracted manual.
- Label claims `verified local`, `verified official online`, or `needs version check` in complex answers. Give a topic path or official URL for consequential steps. Explain uncertainty when online pages are unavailable or require authentication.
- Treat CAPL function names, event context, signatures, object availability, return values, and timing as version and bus specific. Verify in CAPL Functions Help before giving production code; distinguish illustrative pseudocode from checked code.

## Practical workflow

1. Map the system: DBC/ARXML/LDF, CAN/LIN/FlexRay/Ethernet, channels, real/simulated bus, network nodes, test nodes/units, signal and system-variable ownership.
2. Choose the CANoe configuration and test setup. Keep simulation CAPL in the simulation node; put assertions, verdicts, timeouts, and report steps in a test unit/test module.
3. For vTESTstudio, select Test Table, Test Diagram, State Diagram, CAPL, or C# based on the test. Bind the system environment, create parameters and variants, build `.vtuexe`, then add it to the CANoe Test Setup for Test Units. Confirm test configuration, execution order, and Test Trace/report.
4. Check compatibility at both the test-unit level **and** individual commands, parameters, libraries, and CANoe options. Build success is not proof of execution compatibility.
5. Diagnose with reproducible evidence: project versions, exact error, minimal test unit, measurement state, trace, bus configuration, and the relevant source topic. Avoid destructive edits to original CANoe configurations.

## References

- [CANoe 14 local map](references/canoe14.md)
- [CAPL basics: timers, writeEx, sysGetVariableString](references/capl-basics.md)
- [vTESTstudio 3 local map](references/vteststudio3.md)
- [vTESTstudio 6 local map](references/vteststudio6.md)
- [CANoe 19 online status and comparison](references/canoe19.md)
- [Version compatibility and migration](references/compatibility.md)
- [Provenance and source register](references/sources.md)

This independent community skill is maintained by Patiphan Phakdeeburi (TOPTUBBY). Vector product names belong to Vector Informatik GmbH.
