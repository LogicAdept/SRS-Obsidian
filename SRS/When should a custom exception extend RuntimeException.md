<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: extend `RuntimeException` when the failure is a programming error, contract/validation violation, or something the caller usually cannot recover from — so you do not force `throws` on every method. Modern stacks (Spring, Hibernate) prefer unchecked application exceptions. Extend `Exception` only when the caller should be forced to handle a recoverable expected condition.
> [!warning] Unverified traps from the dump
> - Do not extend Error for business failures; dumps treat Error as JVM/system territory.
> - A custom unchecked type still can be caught; it just is not compiler-enforced.
