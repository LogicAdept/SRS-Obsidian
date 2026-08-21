<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A plain try must be followed by catch, finally, or both. try { } alone is a compile error.

From Java 7, try-with-resources may omit both catch and finally because the compiler generates resource closing. The resources must implement AutoCloseable; otherwise the statement does not compile.
> [!warning] Unverified traps from the dump
> - try-finally without catch remains valid and is the usual answer to try-without-catch, which is a different question.
> - Omitting catch/finally is allowed only for try-with-resources, not for an empty resource list pretending to be a bare try.
