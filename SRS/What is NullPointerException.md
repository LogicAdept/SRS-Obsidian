<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `NullPointerException` is an unchecked `RuntimeException` thrown when code uses `null` where an object is required. Typical cases: calling an instance method or reading/writing a field on a null reference, taking `length` or indexing a null array, unboxing a null wrapper, or `throw null`.
> [!warning] Unverified traps from the dump
> - Empty Optional.get() is NoSuchElementException, not NPE.
> - A declared but uninitialized object array still holds null slots; indexing then dereferencing an element NPEs.
