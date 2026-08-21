<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `ArithmeticException` is an unchecked `RuntimeException` for an exceptional arithmetic condition. The classic interview example is integer division by zero: `int z = 10 / 0` compiles and then throws at run time (`/ by zero`).
> [!warning] Unverified traps from the dump
> - Ordinary int/long overflow wraps; it does not throw ArithmeticException unless you use exact methods such as Math.addExact.
> - Integer divide-by-zero throws; floating-point divide-by-zero does not (see the companion cue).
