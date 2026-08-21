<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: both are standard unchecked precondition failures. `IllegalArgumentException` — a method argument is illegal (wrong value or range), e.g. `age < 0`. `IllegalStateException` — the object is in the wrong state for the operation regardless of the arguments, e.g. `start()` when already running. Prefer these built-ins over a custom type for those two cases.
> [!warning] Unverified traps from the dump
> - If some argument values would have worked, dumps treat it as IllegalArgumentException; if no argument would work, IllegalStateException.
> - Iterator.remove() without a preceding next() is IllegalStateException, not IllegalArgumentException.
