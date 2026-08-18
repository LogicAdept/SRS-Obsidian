<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`getConstructor()` only sees public constructors. Use `getDeclaredConstructor(...)`, then `setAccessible(true)`, then `newInstance(...)`.

Dumps present this as how you still construct types whose constructors are private (tests, some singleton / utility patterns).

> [!warning] Unverified traps from the dump
> - Bypassing a private constructor can break singleton / factory invariants.
