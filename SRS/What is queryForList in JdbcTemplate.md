<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Exam notes: `queryForList` returns `List<Map<String,Object>>` — one map per row. `select * from PERSON` with no binds in the simple example; overloads can take bind varargs.

Use this when you want generic column maps instead of a `RowMapper` into a domain type.

> [!warning] Unverified traps from the dump
> - A list of maps is not the same as `query` plus `RowMapper`, which returns `List<Person>`.
> - `queryForMap` is the one-row cousin.

