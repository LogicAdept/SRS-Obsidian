<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Exam notes: `RowMapper` maps each row to one domain object; `ResultSetExtractor` maps the whole `ResultSet` to one result. You iterate the `ResultSet` yourself (`rs.next()`), which looks closer to raw JDBC, but you can build a graph (for example one `Order` plus line items) instead of a list of maps.

It is a functional interface: `T extractData(ResultSet rs) throws SQLException, DataAccessException`. Used as the callback on `JdbcTemplate.query`.

A Climb Q&A: `ResultSetExtractor` processes the entire `ResultSet` at once; `RowCallbackHandler` processes each row one at a time.

> [!warning] Unverified traps from the dump
> - This is the exceptional path in those notes; everyday SELECT-to-list mapping is `RowMapper`.
> - A dump example needed a cast on the lambda: `(ResultSetExtractor<Order>)(rs) -> { ... }`.

