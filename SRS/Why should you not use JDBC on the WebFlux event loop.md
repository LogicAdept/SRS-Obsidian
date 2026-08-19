<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

JDBC `ResultSet.next()` blocks the calling thread. On WebFlux that is the event loop — “catastrophe”. R2DBC is the non-blocking SQL API (drivers for PostgreSQL, MySQL, H2, MSSQL). Spring Data R2DBC gives `ReactiveCrudRepository`. Trade-off: lose lazy loading, entity graphs, L2 cache, and JPA features.

If you must wrap blocking JDBC: `Mono.fromCallable(() -> jdbcTemplate.queryForObject(...)).subscribeOn(Schedulers.boundedElastic())` — never bare `fromCallable` on the loop.

> [!warning] Unverified traps from the dump
> - R2DBC is not JPA; dumps trade non-blocking SQL for losing lazy loading, entity graphs, L2 cache, and JPA features.
> - `boundedElastic` is a Reactor scheduler; the WebFlux rule is still “do not block Netty threads”.

