<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`NamedParameterJdbcTemplate` is built on `JdbcTemplate` for lower-level JDBC, but it lets you pass SQL arguments as named key-value pairs instead of `?` placeholders.

A Spring JDBC list says you write names with a colon prefix such as `:paramName`, put values in a `MapSqlParameterSource` or `BeanPropertySqlParameterSource`, and call `query` or `update`.

Java Code Geeks: named parameters make the SQL easier to follow when there are many parameters.

> [!warning] Unverified traps from the dump
> - Dumps still use positional `?` on plain `JdbcTemplate`; named parameters are the NamedParameter wrapper, not a JDBC driver feature by themselves.
> - Insert example: `update` plus a map whose keys are column/parameter names and values are the bind values.

