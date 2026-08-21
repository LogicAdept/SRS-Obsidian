<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The generated close path null-checks each resource. close() is not invoked on null, so close does not throw NullPointerException. Using the null resource inside the body is still an ordinary NPE.
> [!warning] Unverified traps from the dump
> - The null-tolerance is only for automatic close, not for your use of the resource.
