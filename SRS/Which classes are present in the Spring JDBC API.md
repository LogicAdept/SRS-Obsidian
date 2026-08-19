<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Java Code Geeks answers “which classes are present in spring JDBC API” with these approaches for JDBC access:

- `JdbcTemplate`
- `SimpleJdbcTemplate`
- `NamedParameterJdbcTemplate`
- `SimpleJdbcInsert`
- `SimpleJdbcCall`

> [!warning] Unverified traps from the dump
> - The dump does not mention `JdbcClient`, `RowMapper`, or `JdbcDaoSupport` in that list.
> - `SimpleJdbcTemplate` is a legacy name in interview lists; do not assume it is current API without checking a later dump.

