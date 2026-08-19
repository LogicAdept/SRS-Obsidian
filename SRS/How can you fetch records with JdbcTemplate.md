<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps name a small set of read methods: `query` (list of mapped objects), `queryForObject` (one value or one mapped object), `queryForMap` (one row as `Map<String,Object>`), `queryForList` (list of those maps).

For domain objects you pass a callback: `RowMapper` (per row), or `ResultSetExtractor` if you walk the whole `ResultSet`. Java Code Geeks starts the same answer with “two interfaces” for fetching records (the list in that dump is truncated).

`update` in those notes is INSERT/UPDATE/DELETE, not a fetch.

> [!warning] Unverified traps from the dump
> - Bind-variable order on `JdbcTemplate` must match `?` order.
> - `queryForObject` is for a single result; `query` is for multiple rows. Dumps do not name the exception if the row count is wrong.

