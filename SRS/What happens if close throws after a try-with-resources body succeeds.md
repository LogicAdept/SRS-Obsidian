<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

With no primary exception from the body, the close() exception is thrown out of the try-with-resources statement. A successful body can still fail on cleanup. That matters for types whose close() flushes (for example BufferedWriter): a failed final flush is a real, non-suppressed failure the caller must handle.
> [!warning] Unverified traps from the dump
> - Suppression applies only when the body (or an earlier close/init) already has a primary exception.
