<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A Spring JDBC interview list names three core pieces that work together: `DataSource` (connections), `JdbcTemplate` (SQL execution, exceptions, result handling), and `NamedParameterJdbcTemplate` (named SQL parameters).

A Java Code Geeks list of Spring JDBC *approaches* is broader: `JdbcTemplate`, `SimpleJdbcTemplate`, `NamedParameterJdbcTemplate`, `SimpleJdbcInsert`, and `SimpleJdbcCall`.

> [!warning] Unverified traps from the dump
> - Those lists are not a complete module map: dumps also talk about `RowMapper`, exception translation, and DAO support classes.
> - `SimpleJdbcTemplate` is still listed in old interview sheets even when they give it no description.

