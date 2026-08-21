<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. try, its catch clauses, and its finally clause form a single statement. The compiler rejects any statements inserted between those blocks.
> [!warning] Unverified traps from the dump
> - Nested try-catch-finally inside a block is allowed; that is not the same as code sitting between sibling catch/finally clauses.
