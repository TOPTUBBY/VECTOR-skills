# CAPL function guide: CANoe 14 SP2 baseline

This is a small, independently written quick guide. For production code, open the exact function page in the installed CANoe Help; signatures and availability can vary by version and execution context. `msTimer` is a **timer variable type**, not a function. CAPL identifiers are shown in the spelling used by the local Help.

## Millisecond timer: `msTimer`, `setTimer`, `on timer`

```capl
variables
{
  msTimer statusTimer;
}

on start
{
  setTimer(statusTimer, 500); // Schedule one event in 500 ms.
}

on timer statusTimer
{
  write("Status timer expired");
  setTimer(statusTimer, 500); // Rearm here only if periodic behavior is wanted.
}
```

`timer` measures seconds; `msTimer` measures milliseconds. `setTimer(msTimer t, long duration)` starts/restarts the millisecond timer. The `on timer` handler runs when it expires. `cancelTimer(statusTimer)` stops a pending event. A one-shot timer does not repeat until rearmed; `setTimerCyclic` is another option for a periodic timer. Timer precision depends on hardware, so do not assume hard real-time millisecond execution. Verify timer availability and the event context for the CAPL node being edited.

Local Help: `CAPLFunctions/Other/Functions/CAPLfunctionSetTimer.htm`, `CAPLFunctions/Other/EventProcedures/CAPLfunctionOnTimer.htm`, and `CAPLFunctions/Other/Functions/CAPLfunctionCancelTimer.htm` under `CANoe14/Help01/CANoeCANalyzerHTML5/Content/Topics/`.

## `writeEx`: append formatted output

```capl
writeLineEx(1, 1, "Received: ");   // Start a new line on the CAPL page.
writeEx(1, 1, "0x%X", 0x123);     // Continue that line.
```

CANoe 14 SP2 signature: `void writeEx(long sink, dword severity, char format[], ...)`. It writes to the **current last line**, without starting a new line. Use `writeLineEx` when each message should start on a new line. Common sink values: `1` CAPL page, `0` System page, `4` Test page, `-3` Trace Window. Severity: `0` success, `1` information, `2` warning, `3` error. Trace output needs the CAPL System Message filter enabled; severity has no meaning in Trace. Sink `-2` is restricted to ASC logging with a CAPL node in the Measurement Setup before the Logging Block; do not treat it as a general file writer.

Local Help: `CAPLFunctions/Other/Functions/CAPLfunctionWriteEx.htm` and `CAPLfunctionWriteLineEx.htm`.

## `sysGetVariableString`: read a string system variable

```capl
variables
{
  char statusText[128];
}

on start
{
  long result;
  result = sysGetVariableString(sysvar::Demo::StatusText,
                                statusText, elcount(statusText));
  if (result == 0)
    write("Status: %s", statusText);
  else
    write("Cannot read Demo::StatusText; code=%d", result);
}
```

Create a **String** system variable named `Demo::StatusText` in the CANoe configuration before using this sample. CANoe 14 SP2 documents two forms:

```capl
long sysGetVariableString(char namespace[], char variable[], char buffer[], long bufferSize);
long sysGetVariableString(SysVarName, char buffer[], long bufferSize);
```

The second form uses a symbol such as `sysvar::Demo::StatusText`. The function copies the string value into the supplied buffer and returns `0` on success; a nonzero return indicates an error, including missing namespace/variable or unsuitable type. Size the destination appropriately and check the return code. The Help has separate details for struct/generic-array members and for older version availability; consult it when those cases arise.

Local Help: `CAPLFunctions/SystemVariables/Functions/CAPLfunctionSysGetVariableString.htm`.

## Answering a CAPL question with this skill

1. Identify exact CANoe/vTESTstudio service pack and CAPL placement: Simulation Setup network node, Measurement Setup program node, test module, or vTESTstudio CAPL file.
2. Resolve the exact function name in the matching local/online Help. Do not confuse a type (`msTimer`) with an operation (`setTimer`).
3. Give purpose, verified signatures, parameter units/types, return/error values, availability, a minimal example, and a practical pitfall.
4. If only the 14 SP2 baseline is available for a CANoe 19 question, mark the example as unverified for 19 and link the official current CAPL documentation instead of inventing differences.

Vector's [CAPL documentation guidance](https://support.vector.com/kb?id=kb_article_view&sysparm_article=KB0011332) identifies the Help in the installed tool as the complete current reference and points CANoe 19 users to online Help. This guide is not an exhaustive CAPL API catalog.
