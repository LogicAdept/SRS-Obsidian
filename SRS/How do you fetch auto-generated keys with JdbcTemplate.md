<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Climb: use `JdbcTemplate.update` for the INSERT, pass a `PreparedStatementSetter` to bind values, and a `KeyHolder` to receive the generated keys.

> [!warning] Unverified traps from the dump
> - The dump does not show `GeneratedKeyHolder` construction or `PreparedStatementCreator` that calls `prepareStatement(sql, new String[]{"id"})`.
> - This is not `queryForObject` after insert unless you have another dump that says so.

