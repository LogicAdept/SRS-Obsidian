<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If assertions are enabled and the boolean expression is `false`, the JVM raises `java.lang.AssertionError` and (unless caught) stops that path.

Simple form: `assert condition;` — no detail string.

Augmented form: `assert condition : detail;` — dumps say `detail` is converted to a string and passed to the `AssertionError` constructor (example: `AssertionError: here x value should be >10 but it is not`).

If assertions are **disabled**, the statement is skipped and no error is thrown even when the condition would be false.

> [!warning] Unverified traps from the dump
> - Some dumps call `AssertionError` an exception; others say it is a child of `Error`.
> - Failure is **not** a checked exception you must declare.
