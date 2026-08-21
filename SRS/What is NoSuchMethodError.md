<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview lists: `Exception in thread main java.lang.NoSuchMethodError: main` when you launch a class that has no `main` method.

Broader dump claim: the method existed at compile time but the runtime class no longer defines that method or signature (partial rebuild or library version skew). Hierarchy dumps nest this under incompatible class-change / `LinkageError`.
> [!warning] Unverified traps from the dump
> - Reflective lookup failures are NoSuchMethodException (checked), not NoSuchMethodError.
> - Missing main is only one dump example; dependency version mismatch is the usual production case.
