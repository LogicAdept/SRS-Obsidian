<!--
reps: 0
priority: 0
-->
#Databases #SRS

# Which database schema versioning tools do you know

> [!abstract] Short answer
> The two dominant tools are **Flyway** (plain SQL migration scripts, `V1__create_orders.sql`, minimal magic) and **Liquibase** (XML/YAML/JSON/SQL changelogs with a deeper abstraction layer, rollback support, and database-independent "change types"). Both apply ordered, tracked migrations to a live database — the database-equivalent of commits for schema — and both are the standard answers in Java interviews. They solve a problem plain `.sql` dumps and ORM `hbm2ddl.auto=update` famously do not: controlled, repeatable, auditable evolution of schema in every environment.

## Why schema needs its own versioning discipline

Code in Git re-deploys from scratch; a database *carries* its history — you cannot recreate the table with data in it. So schema changes must be **applied in order, exactly once, to every environment**, which is what migration tooling provides: a migrations directory (committed to the repo, reviewed like code — [[What are Git branches for]]'s review unit applies to DDL too), a metadata table in the database recording which migrations ran (`flyway_schema_history` / `DATABASECHANGELOG`), and on deployment the tool diffs the directory against that table and applies what is missing. Result: schema state is reproducible from the repo — the "what version is this database" question gets a Git answer ([[What does a commit object contain]]'s immutability is why the scripts themselves must never be edited after shipping).

- **Flyway** — convention-first: `V<N>__<desc>.sql` versioned migrations, `R__` repeatable ones (views, functions), optional Java-based migrations when SQL is not enough. The whole mental model fits on a napkin; DBAs read the scripts directly.
- **Liquibase** — changelog-first: changes declared in XML/YAML/JSON (or plain SQL via `sqlFile`), giving platform-neutral *change types* (`createTable`, `addColumn`), automatic **rollback** statements for many types, **contexts/labels** for environment-specific runs, and preconditions ("apply only if table missing"). More machinery, more portability — heavier to read.

```d2
direction: right
repo: "Migrations in Git\nV1, V2, V3…" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
tool: "Flyway / Liquibase\nat app start or in CI" {
  width: 320
  height: 110
  style.fill: "#fff3e0"
}
meta: "History table in DB\nwhat already ran" {
  width: 320
  height: 100
  style.fill: "#e8f5e9"
}
db: "Schema\nevolved in order, once" {
  width: 260
  height: 100
  style.fill: "#f3e5f5"
}
repo -> tool: "diff dir vs history"
tool -> meta: "read / append"
tool -> db: "apply pending"
```

**Fig. 1.** The migration loop: the repo is the source of truth, the history table is the database's own bookmark, and deployments apply only the delta.

Where it sits in the stack: Spring Boot integrates both out of the box (auto-running migrations at startup); CI pipelines validate migrations against an ephemeral database ([[Which CI CD tools do you know]]); and release strategy interacts directly — expanding/contracting columns under [[How does trunk based development differ from long lived feature branches]]' flags needs *backward-compatible migration steps*, not monolithic rewrites.

> [!warning] Migrations are one-way in production — and "the ORM will create the schema" is not versioning
> Editing a migration that already ran corrupts the checksum and the history (Flyway fails validation; the fix is a *new* migration, never an edit); destructive changes (`DROP`, column type narrowing) need the expand-migrate-contract pattern so old code keeps running during deploys. Hibernate's `hbm2ddl.auto=update` is the interview trap: it mutates schema *without* history, review, or the ability to reproduce — banned beyond dev toys. Also: a migration touching data (backfills) must be batched and idempotent — a 40-minute single transaction on the orders table is an outage, and tools will not save you from a bad script.

> [!tip] Interview answer
> **Flyway and Liquibase are the standard schema-migration tools. Flyway is convention-driven plain SQL — versioned scripts applied in order once, tracked in a history table; Liquibase adds a changelog abstraction with change types, rollback metadata, contexts and preconditions, trading readability for portability. Both make schema evolution reviewed, ordered and reproducible from the repo — which is exactly what ORM auto-DDL lacks. The disciplines that matter: never edit a shipped migration, plan destructive changes as expand-migrate-contract, and keep data backfills batched.**

