<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# Which connection pool does Quarkus use

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: Agroal — Quarkus's own JDBC connection pool, integrated with Narayana transactions and metrics; configuration via quarkus.datasource.* (jdbc min/max size, acquisition timeout); alternatives (HikariCP) are not the default integration path.
