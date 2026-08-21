<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `AssertionError` is a child of `Error` and is **unchecked**. It is **legal** to catch it, but **not recommended**.

A dump example catches `AssertionError` after `assert(x > 10)` and prints that catching it is not good practice, then continues.

> [!warning] Unverified traps from the dump
> - Catching it can hide a failed invariant and let the program continue in a broken state.
> - Interview wording may say “exception”; the type in the hierarchy is `Error`.
