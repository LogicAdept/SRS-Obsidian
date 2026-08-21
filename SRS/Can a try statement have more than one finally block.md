<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. One try statement has at most one finally clause. Multiple cleanup steps belong in that single finally, or in nested try statements each with their own finally.
> [!warning] Unverified traps from the dump
> - try-with-resources already supplies an implicit close; an explicit finally on the same statement still runs after resources close, and it is still only one finally.
