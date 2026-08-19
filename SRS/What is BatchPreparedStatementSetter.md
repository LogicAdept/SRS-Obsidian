<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A Spring JDBC interview list: `BatchPreparedStatementSetter` is a callback for batch updates. It sets parameter values for a batch of SQL statements so many inserts or updates run as one batch, cutting round-trips.

> [!warning] Unverified traps from the dump
> - This is the setter callback, not the only batch API; dumps also show `JdbcTemplate.batchUpdate`.

