<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When an outer transaction exists, both map to the same physical transaction. REQUIRED has no savepoint: an inner rollback-only mark prevents the outer commit. NESTED sets a savepoint so the inner failure can be undone locally and the outer method can still commit the rest.
> [!warning] Unverified traps from the dump
> - Without an outer transaction both start a new one, so the savepoint difference never appears.
> - Catching an inner REQUIRED RuntimeException and continuing still cannot commit; NESTED is the savepoint path for that pattern.
