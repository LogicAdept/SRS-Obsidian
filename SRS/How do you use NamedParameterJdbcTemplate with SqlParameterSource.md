<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview steps: put named parameters in SQL with a colon prefix (`:paramName`). Build a `SqlParameterSource` — dumps name `MapSqlParameterSource` or `BeanPropertySqlParameterSource` — then call `NamedParameterJdbcTemplate.query` or `update`.

Climb insert: `NamedParameterJdbcTemplate.update` with the INSERT string and a map of column names to values.

> [!warning] Unverified traps from the dump
> - Plain `JdbcTemplate` does not take named sources; it takes `?` and positional args.
> - Bean property source implies the Java bean field names match the `:names` in SQL.

