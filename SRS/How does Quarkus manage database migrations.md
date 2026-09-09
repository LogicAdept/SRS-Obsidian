<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does Quarkus manage database migrations?

> [!abstract] Short answer
> Via the **`quarkus-flyway`** extension (or the `quarkus-liquibase` sibling): migrations live in `src/main/resources/db/migration` as usual, and with `quarkus.flyway.migrate-at-start=true` Flyway runs **at application startup, before Hibernate ORM** — the schema is current by the time the entity manager opens. Migration execution is integrated with dev mode, Dev Services, named datasources and the Dev UI; the alternative is injecting the `Flyway` bean and running migrations yourself.

## Startup migration, step by step

With `migrate-at-start=true`, the recorded bootstrap includes a Flyway run: it validates the applied history (`flyway_schema_history`), applies pending scripts in order, and only then Quarkus continues booting Hibernate. Schema ownership is explicit in code: set `quarkus.hibernate-orm.database.generation=none` so Hibernate never fights Flyway for the schema — the combination "Flyway migrates, Hibernate validates/uses" is the recommended production shape and the standard answer to "how do schema changes get to production" ([[Which connection pool does Quarkus use]]). Per-datasource configuration is `quarkus.flyway."name".migrate-at-start` when several datasources exist; locations, placeholders and clean-at-start (dev convenience) all have `quarkus.flyway.*` properties.

```java
// src/main/resources/db/migration/V1__person.sql (verified run, JDK 21, Quarkus 3.39.2)
// CREATE SEQUENCE IF NOT EXISTS Person_SEQ START WITH 1 INCREMENT BY 1;
// CREATE TABLE IF NOT EXISTS person (
//     id BIGINT PRIMARY KEY,
//     name VARCHAR(255),
//     age INT
// );
//
// application.properties:
//   quarkus.flyway.migrate-at-start=true
//   quarkus.hibernate-orm.database.generation=none
//
// Boot log of java -jar target/quarkus-app/quarkus-run.jar (verbatim):
// 2026-09-09 23:15:29,253 INFO  [org.flywaydb.core.internal.command.DbValidate] (main)
//   Successfully validated 1 migration (execution time 00:00.010s)
// 2026-09-09 23:15:29,315 INFO  [org.flywaydb.core.internal.command.DbMigrate] (main)
//   Migrating schema "PUBLIC" to version "1 - person"
// 2026-09-09 23:15:29,328 INFO  [org.flywaydb.core.internal.command.DbMigrate] (main)
//   Successfully applied 1 migration to schema "PUBLIC", now at version v1
//   (execution time 00:00.003s)
// ...and only afterwards the entity manager and Panache queries ran against the schema.
```

**Listing 1.** The ordering is the whole point: `V1__person.sql` created the sequence and table before the first query; the missing-sequence error in an earlier run of this same app (`Sequence "PERSON_SEQ" not found` at insert time) is precisely what migrate-at-start prevents ([[What is Panache in Quarkus]]).

```d2
direction: down
boot: "Application boot (runtime init)" {
  width: 280
  height: 50
}
fly: "Flyway validate + migrate\ndb/migration V*n__*.sql" {
  width: 300
  height: 65
  style.fill: "#e3f2fd"
}
hib: "Hibernate ORM starts\nschema generation = none" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
serve: "App serves traffic\nschema guaranteed" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
boot -> fly -> hib -> serve
```

**Fig. 1.** Migration is a bootstrap step, not a background job: the order Flyway → Hibernate is recorded in the artifact itself ([[What are the bootstrapping phases of a Quarkus application]]).

## Dev-loop niceties

In dev mode the Dev UI exposes Flyway state — applied and pending migrations — and with Dev Services a fresh database is migrated on every start, which makes "rebuild the schema from zero" a restart rather than a procedure. Liquibase follows the same pattern (`quarkus.liquibase.migrate-at-start`), so the choice between tools is team-standard, not Quarkus-driven. What the extension deliberately does not do is generate application code or manage data migrations — those remain scripts you write.

> [!warning] migrate-at-start is a startup gate, not a zero-downtime solution
> With multiple replicas, a backward-incompatible migration can take the new version down while old replicas still run — or worse, run before the old replicas drain. The startup gate also means a broken migration fails the boot: the app never comes up, which is good for correctness but turns "bad DDL" into an outage. The common misconfiguration to call out: leaving Hibernate's `database.generation` at default alongside Flyway — two schema owners produce drift that only shows up in staging or prod ([[How does Quarkus manage database migrations]] is the procedure; the property pair is the exam question).

> [!tip] Interview answer
> Quarkus ships Flyway and Liquibase as extensions; the standard setup is quarkus-flyway with migrate-at-start=true — migrations from db/migration run during startup, before Hibernate initializes, and I set hibernate-orm.database.generation to none so Flyway owns the schema. The boot log shows validate, migrate to version N, then the app starts; Dev Services and the Dev UI make the dev loop rebuild schemas for free. Named datasources get their own migrate-at-start switches.
