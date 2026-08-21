<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: validate arguments (`Objects.requireNonNull`), use `Optional` for maybe-absent returns, put a constant on the left of `equals` (`"x".equals(s)`), prefer `getOrDefault` over a raw `Map.get` that you then dereference, and initialize fields. Treat NPE as a programming error to fix, not something to catch in every method.
> [!warning] Unverified traps from the dump
> - Optional.get() without a presence check swaps NPE for NoSuchElementException.
> - Unboxing a null Integer (for example a missing Map value) still NPEs.
