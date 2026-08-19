<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Climb: yes, Spring JDBC can run DDL, but it is generally not recommended because DDL can cause data loss. If you must, use `JdbcTemplate.execute()`.

Exam notes: `execute()` showed up on a test exam, is similar to `update()`, and javadoc-level commentary in that note says it is mainly for DDL (create/alter/drop structures).

> [!warning] Unverified traps from the dump
> - Do not use `update()` vs `execute()` interchangeably just because both run SQL; dumps split DML (`update`) and DDL (`execute`).

