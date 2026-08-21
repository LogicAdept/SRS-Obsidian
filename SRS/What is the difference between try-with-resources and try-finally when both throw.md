<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Handwritten try/finally: if the body and close() in finally both throw, the finally exception wins and the body exception is lost.

Try-with-resources reverses that priority: the body exception is primary; close() exceptions are suppressed on it. That is the main exception-handling reason dumps give for preferring TWR over manual finally close.
> [!warning] Unverified traps from the dump
> - An explicit catch or finally on a try-with-resources statement still runs after resources have been closed.
> - If the TWR body succeeds, a close() exception is not suppressed; it propagates normally, same as a failing finally close with no prior exception.
