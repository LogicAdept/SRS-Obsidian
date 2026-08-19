<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Exam notes: `queryForMap` returns one row as `Map<String,Object>` (column name to value). You do not pass the mapped Java type. Example: `select * from PERSON where id=?` → `{ID=1, FIRST_NAME="JOHN", LAST_NAME="DOE"}`.

> [!warning] Unverified traps from the dump
> - This is for a single row. Multiple rows in that same note use `queryForList`.
> - Column keys in the dump are shown uppercased; do not assume every driver does that.

