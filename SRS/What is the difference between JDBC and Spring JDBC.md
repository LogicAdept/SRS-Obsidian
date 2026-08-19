<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Raw JDBC: open a connection, prepare and execute a statement, loop the `ResultSet`, handle exceptions, handle transactions, close the connection. in28minutes shows that as several lines of `PreparedStatement` / `execute` / `close`.

Spring JDBC: the same update becomes `jdbcTemplate.update(sql, args...)`. Dumps say Spring JDBC removes connection/statement/`SQLException`/close boilerplate and gives `JdbcTemplate` (and friends) as the abstraction.

Java Code Geeks lists the JDBC workflow Spring is supposed to take off your plate: connection parameters, open, specify statement, prepare/execute, iterate, per-row work, exceptions, transactions, close.

> [!warning] Unverified traps from the dump
> - You still write SQL. Spring JDBC is not an ORM.
> - Exception translation and connection pooling are extra dump talking points, not automatic just because you constructed a `JdbcTemplate` with a raw `DriverManagerDataSource`.

