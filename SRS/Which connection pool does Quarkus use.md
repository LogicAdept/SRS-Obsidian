<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# Which connection pool does Quarkus use?

> [!abstract] Short answer
> **Agroal** — Quarkus' own JDBC connection pool, not HikariCP. Adding any built-in JDBC driver extension (PostgreSQL, H2, MariaDB, ...) pulls in `quarkus-agroal` automatically; it integrates with the Narayana transaction manager for transaction-scoped connections, exposes pool metrics, and is configured through `quarkus.datasource.jdbc.*` — pool sizing (`initial-size`, `min-size`, `max-size`), `acquisition-timeout`, validation intervals and leak detection. Reactive drivers (Vert.x SQL clients) are pooled separately and do not go through Agroal.

## Where Agroal sits and why it matters

Every JDBC connection handed to Hibernate ORM comes from the Agroal pool for the named datasource (`<default>` or named via `quarkus.datasource."name".*`). The integration points interviewers care about: **transactions** — inside an active JTA transaction the connection is borrowed and returned transactionally, so `@Transactional` methods and the pool agree on lifecycle ([[How do transactions work in Quarkus]]); **health checks** — the `quarkus-smallrye-health` extension registers a built-in "Database connections health check" per datasource, so `/q/health` reports `<default>: UP` without custom code; **metrics** — pool counters flow into Micrometer when the metrics extension is present. Named datasources each get their own pool instance, isolated and individually tunable.

```java
// application.properties of the verified run (JDK 21, Quarkus 3.39.2, H2 in-memory, no Docker):
// quarkus.datasource.db-kind=h2
// quarkus.datasource.username=sa
// quarkus.datasource.password=
// quarkus.datasource.jdbc.url=jdbc:h2:mem:demo;DB_CLOSE_DELAY=-1
//
// Boot of the packaged fast-jar then GET /q/health (verbatim fragment):
// {
//     "status": "UP",
//     "checks": [ {
//         "name": "Database connections health check",
//         "status": "UP",
//         "data": { "<default>": "UP" }
//     }, ... ]
// }
// The named check exists because Agroal + smallrye-health are on the classpath;
// Hibernate ORM + Panache above it borrowed connections from this pool for every query.
```

**Listing 1.** One datasource stanza configures the whole chain — driver, pool, transaction integration — and the health endpoint proves the pool answers, which is exactly what a Kubernetes readiness probe polls ([[What health checks does Quarkus expose]]).

```d2
direction: down
cfg: "quarkus.datasource.jdbc.*\nurl, max-size, acquisition-timeout" {
  width: 320
  height: 65
  style.fill: "#e3f2fd"
}
pool: "Agroal pool (<default> or named)\nborrow / return, validation, leak detection" {
  width: 340
  height: 70
  style.fill: "#fff3e0"
}
orm: "Hibernate ORM / Panache\nJDBC stack" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
tx: "Narayana JTA\ntransaction-scoped borrow" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
obs: "Health check / Micrometer\npool gauges" {
  width: 250
  height: 55
}
cfg -> pool
pool -> orm
tx -> pool
pool -> obs
```

**Fig. 1.** Agroal is the middle box: configuration on top, consumers below, transaction manager and observability plugged in from the side. Reactive clients bypass it entirely ([[What is Hibernate Reactive in Quarkus]]).

## Sizing and failure modes worth quoting

`max-size` (the example guides use 16) is the concurrency ceiling for blocking JDBC work — under a burst, callers wait up to `acquisition-timeout` and then fail with a pool timeout exception, which is a startup-config problem wearing a runtime costume. `min-size`/`initial-size` control warm capacity, validation intervals guard against stale connections after DB restarts, and leak detection (`extended-leak-report`) names the code paths that borrowed and never returned. For reactive stacks, `quarkus.datasource.reactive.max-size` plays the same role on the Vert.x client pool — a different knob, easy to tune by mistake when both stacks exist.

> [!warning] "Quarkus uses HikariCP" — the reflex answer that is wrong
> Spring Boot ships Hikari by default; Quarkus does not use it. The practically relevant follow-up: because the reactive client pool and the Agroal pool are separate, an app that mixes JDBC and reactive datasources has two capacity regimes for the same database — one tuned, one default — and incidents show up as timeouts in exactly one of them. Also note Agroal is required explicitly only for a **custom** JDBC driver; built-in drivers bring it automatically.

> [!tip] Interview answer
> Quarkus pools JDBC connections with Agroal, its own pool — not HikariCP. Any built-in driver extension pulls it in, it cooperates with the Narayana transaction manager so transaction-scoped borrowing just works, and it feeds both the built-in database health check and Micrometer metrics. Configuration lives under quarkus.datasource.jdbc — max-size, acquisition-timeout, validation and leak detection — and named datasources each get their own isolated pool. Reactive drivers are the exception: they use the Vert.x client pool instead.
