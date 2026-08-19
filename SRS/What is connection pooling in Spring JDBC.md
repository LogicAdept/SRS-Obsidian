<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview list: connection pooling keeps a pool of already-open database connections so each operation does not pay create/close. In Spring JDBC that is called important because it cuts connection overhead in database-heavy apps.

The same list’s DataSource question says you can configure pooling on the `DataSource` bean. in28minutes wires `ComboPooledDataSource` (c3p0) as that bean.

> [!warning] Unverified traps from the dump
> - Boot’s default pool is HikariCP (`What is HikariCP in Spring Boot`); this card is the generic dump claim.
> - `DriverManagerDataSource` examples are not pooling.

