<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If a transaction already exists, NESTED takes a JDBC savepoint in that same physical transaction. Failure of the nested scope rolls back only to the savepoint so the outer method can continue. If the outer transaction later rolls back, nested work is undone too. If no transaction exists, NESTED behaves like REQUIRED and starts one.
> [!warning] Unverified traps from the dump
> - NESTED is not an independent commit; only REQUIRES_NEW commits before the outer method ends.
> - Savepoints work on JDBC DataSourceTransactionManager; JTA/JPA setups often do not nest this way.
