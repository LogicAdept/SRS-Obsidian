<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. When an exception is thrown in try, the rest of that try block is skipped. The first matching catch runs, then finally if present, then execution continues after the whole try statement — not back into the remaining try statements.
> [!warning] Unverified traps from the dump
> - If no catch matches, remaining try code is still skipped; finally runs, then the exception propagates.
