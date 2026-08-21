<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `Objects.requireNonNull(obj)` (and the message / `Supplier` overloads) fail fast with `NullPointerException` if the reference is null, otherwise return the same reference. Interview answers present it as the idiomatic parameter check instead of a hand-written `if (x == null) throw ...`.
> [!warning] Unverified traps from the dump
> - It throws NullPointerException, not IllegalArgumentException.
> - requireNonNullElse / requireNonNullElseGet return a fallback instead of throwing when the first argument is null.
