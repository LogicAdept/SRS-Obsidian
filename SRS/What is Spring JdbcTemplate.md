<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`JdbcTemplate` is the central Spring JDBC helper. Dumps say it executes SQL queries, updates, and stored-procedure calls, iterates `ResultSet`s, and extracts values, while creating and releasing JDBC resources so you do not forget to close the connection.

It catches JDBC exceptions and translates them into the `org.springframework.dao` hierarchy. Once configured it is described as thread-safe. Typical methods in the dumps: `query`, `queryForObject`, `update`, `execute`, `batchUpdate`.

A usage dump injects it into a `@Repository` and maps rows with `BeanPropertyRowMapper` or a custom `RowMapper`.

> [!warning] Unverified traps from the dump
> - SimpleJdbcTemplate still appears in older API lists; dumps do not say it is the class you should start with today.
> - `execute()` is described as similar to `update()` and mainly for DDL, not as the default DML path.

