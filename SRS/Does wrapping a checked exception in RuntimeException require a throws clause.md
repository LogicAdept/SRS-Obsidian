<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: no. The compiler looks at the exception you throw, not at the cause chain. `throw new RuntimeException(new Exception("Chained Exception"));` compiles without `throws` because the thrown type is unchecked. Hiding a checked `IOException` inside `new RuntimeException("I/O failed", ex)` is the pattern dumps cite to drop a checked obligation.
> [!warning] Unverified traps from the dump
> - The original checked exception is only the cause; callers catching IOException will not see it unless they unwrap getCause().
> - Sneaky-throw tricks that cast a checked exception to a type variable are a different (and dump-noted) compiler loophole.
