<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Exam notes: `queryForObject` when you expect a single result (a scalar with `Integer.class` / `Date.class`, or one domain object plus a `RowMapper`). `query` when you expect multiple rows; return type becomes a `List` and the same `RowMapper` runs per row.

in28minutes: `query` with a user bind for many todos; `queryForObject` with an id bind for one todo.

> [!warning] Unverified traps from the dump
> - Using `queryForObject` for a query that can return zero or many rows is the failure mode the dumps imply by stressing “single result”.
> - There is also `queryForMap` / `queryForList` when you do not want a domain type.

