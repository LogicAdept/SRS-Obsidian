<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. Spring maps NESTED onto JDBC savepoints, typically with DataSourceTransactionManager. Dumps note that databases such as PostgreSQL, MySQL, and Oracle support savepoints. Without savepoint support, nested partial rollback is not available that way.
> [!warning] Unverified traps from the dump
> - JPA/JTA managers often do not give you NESTED savepoints out of the box.
> - A nested rollback still disappears if the outer transaction rolls back.
