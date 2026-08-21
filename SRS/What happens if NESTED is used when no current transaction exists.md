<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

With no current transaction, NESTED behaves like REQUIRED: Spring starts a new transaction. The savepoint path only appears when an outer transaction already exists.
> [!warning] Unverified traps from the dump
> - Interview answers that say NESTED always creates a savepoint miss the no-outer-transaction case.
