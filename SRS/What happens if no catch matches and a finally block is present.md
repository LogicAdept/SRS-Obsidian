<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

finally still executes. After a normal finally, the original exception continues propagating. If nothing further up the call stack handles it, the thread's default uncaught handler runs (typically printing a stack trace and terminating that thread).

If finally completes abruptly (return or throw), that abrupt completion replaces the pending exception.
> [!warning] Unverified traps from the dump
> - finally runs even when the exception will later be handled by an enclosing try.
> - System.exit or JVM termination can still prevent finally from running at all.
