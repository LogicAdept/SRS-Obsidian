<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

While REQUIRES_NEW runs, the outer transaction stays suspended and keeps its connection bound. The inner scope acquires another connection. If many threads hold an outer transaction and all wait for a second connection, the pool can empty and threads deadlock waiting on themselves.
> [!warning] Unverified traps from the dump
> - Dumps say size the pool above concurrent threads by at least one before using REQUIRES_NEW in a hot path.
> - NESTED avoids this extra connection because it uses a savepoint on the same connection.
