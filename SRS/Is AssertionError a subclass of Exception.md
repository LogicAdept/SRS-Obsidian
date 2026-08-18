<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Exceptions #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `AssertionError` is a **child class of `Error`**, not of `Exception`. It is **unchecked**. The JVM raises it when an `assert` statement fails (assertions enabled, condition false).

> [!warning] Unverified traps from the dump
> - Unchecked means you do not declare `throws AssertionError`.
> - Some dumps still say “generates an exception `java.lang.AssertionError`” while also placing it under `Error`.
