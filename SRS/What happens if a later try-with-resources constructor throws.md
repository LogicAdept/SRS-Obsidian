<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Resources are initialized left to right. If a later resource expression throws, earlier resources that were successfully created are closed in reverse order, later ones are never created, and the initializer exception propagates.

An exception from closing an already-opened resource is suppressed onto that initializer exception rather than replacing it.
> [!warning] Unverified traps from the dump
> - This is the nested-try/finally case that manual resource code often got wrong.
