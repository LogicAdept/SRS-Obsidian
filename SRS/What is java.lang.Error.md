<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `Error` is a subclass of `Throwable` (a sibling of `Exception`). It marks serious JVM-level problems that a reasonable application should not try to catch.

Typical dump examples: `OutOfMemoryError`, `StackOverflowError`, `VirtualMachineError`, `AssertionError`. Errors are treated as abnormal conditions; `ThreadDeath` is called out as an Error that is a "normal" condition but still must not be caught.
> [!warning] Unverified traps from the dump
> - Catching Error is legal; dumps still say not to treat it like a recoverable Exception.
> - Error is unchecked: no throws clause is required.
