<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: a `Throwable` carries a message (`getMessage`), a stack trace captured at construction (`printStackTrace` / `getStackTrace`), an optional cause (`getCause` / a cause constructor), and suppressed throwables attached by try-with-resources (`getSuppressed`).
> [!warning] Unverified traps from the dump
> - Stack traces are usually captured when the exception object is constructed, not when it is thrown.
> - A cause is typically set at construction; initCause can be used at most once if the cause was not already set.
