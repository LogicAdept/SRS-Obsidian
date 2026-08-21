<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

NESTED uses one physical transaction plus a JDBC savepoint: inner rollback undoes only nested work, but an outer rollback still undoes the nested changes. REQUIRES_NEW uses a separate physical transaction that can already be committed while the outer is still open. NESTED does not need a second connection; REQUIRES_NEW does.
> [!warning] Unverified traps from the dump
> - If the parent rolls back, NESTED work is gone; REQUIRES_NEW work that already committed stays.
> - NESTED needs savepoint support; REQUIRES_NEW needs a pool sized for the extra connection.
