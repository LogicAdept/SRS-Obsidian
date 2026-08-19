<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`RowCallbackHandler` processes each row of a `ResultSet` without returning a list of objects. Interview text: custom per-row work when you do not want to map into Java domain objects — logging, aggregation, or streaming.

The functional method in the exam notes is `void processRow(ResultSet rs) throws SQLException`. No example body was given there.

> [!warning] Unverified traps from the dump
> - Unlike `RowMapper`, there is no mapped object returned to `JdbcTemplate`.
> - Climb contrasts it with `ResultSetExtractor`: one row at a time versus the whole set at once.

