<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When the try body throws and a resource close() also throws, try-with-resources propagates the body exception as primary and attaches each close failure with Throwable.addSuppressed. Call getSuppressed() on the primary to read them. Printed stack traces list them under a Suppressed heading.

If the body completes normally, there is no primary to attach to, so a close() exception is thrown as the statement's result instead of being suppressed.
> [!warning] Unverified traps from the dump
> - Cause (getCause) is a different relationship from suppressed exceptions.
> - You cannot add a throwable as suppressed of itself; passing null to addSuppressed throws NullPointerException.
