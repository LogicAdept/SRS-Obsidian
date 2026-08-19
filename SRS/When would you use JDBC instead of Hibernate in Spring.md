<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/Persistence/Hibernate #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Climb: skip Hibernate/ORM when the legacy schema does not fit Hibernate, when you need JDBC-level control for performance, or when the model is so simple that ORM is overkill.

A separate JdbcTemplate-vs-Hibernate dump (already in the vault under JPA) lists analytics SQL (windows, CTE), huge batch inserts, ORM-generated SQL that is poor, legacy migration, and simple CRUD without graphs.

> [!warning] Unverified traps from the dump
> - Spring JDBC still means you write SQL; Hibernate still means an ORM session. This comparison is not Spring Data JPA repositories.
> - `How would you explain JdbcTemplate Hibernate` already exists as a JPA-tagged card; this cue is the Climb interview wording.

