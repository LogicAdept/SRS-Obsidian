<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`RowMapper` maps one `ResultSet` row to a Java object. Dumps use it with `JdbcTemplate.query` and `queryForObject`. The only method named is `mapRow(ResultSet rs, int rowNum)`.

Spring is said to call `mapRow` for every returned row. Exam notes call it a functional interface, usable as a lambda, parameterized with the return type, and valid for both single-row and multi-row queries.

in28minutes shows a custom `TodoMapper` that copies columns into a `Todo`, and also `new BeanPropertyRowMapper(Todo.class)`.

> [!warning] Unverified traps from the dump
> - `mapRow` is not supposed to call `ResultSet.next()`; dumps that iterate themselves are describing `ResultSetExtractor`, not `RowMapper`.
> - Do not confuse with `RowCallbackHandler`, which processes a row and returns void.

