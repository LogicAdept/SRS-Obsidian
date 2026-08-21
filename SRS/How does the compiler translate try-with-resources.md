<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The compiler desugars TWR into try/finally that tracks a primary exception. After the body, each non-null resource is closed. If a primary exception already exists, close() failures are addSuppressed onto it; if not, close() may throw normally.

Multiple resources compile as nested TWR, which yields reverse (LIFO) close order. Explicit catch/finally wrap that generated close and therefore run after close.
> [!warning] Unverified traps from the dump
> - A resource initialized to null is skipped at close; there is a generated null check.
> - If a later resource initializer throws, already-opened resources are still closed in reverse order.
