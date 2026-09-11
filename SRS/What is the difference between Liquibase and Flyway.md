<!--
reps: 0
priority: 0
-->
#Databases #SRS

# What is the difference between Liquibase and Flyway

> [!abstract] Short answer
> **Both are version-control tools for database schema — applied migrations are recorded in a tracking table and never re-run. Flyway is plain, version-numbered SQL (V2__add_index.sql) applied in version order with checksums; Liquibase is a vendor-neutral changeset model (XML/YAML/JSON/SQL) with a database abstraction layer, rich execution filters, and built-in diff/rollback machinery.** The trade: Flyway's transparency and simplicity versus Liquibase's abstraction and control features.

## The same contract, different shapes

The shared core: migrations are append-only artifacts; a history table (Flyway's `flyway_schema_history`, Liquibase's `DATABASECHANGELOG`) records what ran on each database; the tool applies only pending changes; editing an applied migration breaks checksum verification — the discipline in [[What merge strategies are important in database development]] applies to both. The shapes differ. **Flyway:** files named by version (`V1__create_users.sql`, `V2__add_email.sql`) are applied in version order; migrations are SQL (or Java-based when needed); pending migrations are discovered by scanning the classpath; repeatable migrations (`R__view.sql`) re-run on checksum change. Everything the DB will do is literal SQL you wrote — easy to review, easy to debug, and dialect-specific by nature. **Liquibase:** changesets declare *what* changes in XML/YAML/JSON (or raw SQL), and Liquibase generates the dialect-specific SQL — one changelog can target MySQL, PostgreSQL, and Oracle; contexts and labels gate which changesets run per environment; preconditions guard destructive steps; diff can generate changelogs from an existing schema, and rollback can be generated or declared per changeset.

```d2
direction: right
fly: "Flyway\nV2__add_index.sql\nversion order · checksums\nSQL = what runs" {
  width: 290
  height: 120
  style.fill: "#e3f2fd"
}
liq: "Liquibase\nchangeSet author:id\nXML/YAML/JSON -> generated SQL\ncontexts · labels · diff" {
  width: 330
  height: 130
  style.fill: "#fff3e0"
}
led: "History table\nflyway_schema_history /\nDATABASECHANGELOG" {
  width: 280
  height: 120
  style.fill: "#e8f5e9"
}
fly -> led
liq -> led
```

**Fig. 1.** Two authoring models over one ledger: Flyway feeds literal versioned SQL; Liquibase feeds declarative changesets it translates per dialect.

> [!warning] "Multi-DB abstraction" cuts both ways — and version collisions hurt both
> Liquibase's abstraction is its selling point and its hazard: generated SQL can hide dialect details (locking, index storage) that you would have written correctly by hand in Flyway, and debugging happens in Liquibase's layer. Conversely Flyway's per-dialect SQL costs you maintenance when one schema serves several engines. The shared trap matters more: two branches both adding `V7__` (Flyway) or colliding changesets (Liquibase) — the ledger cannot invent an order, so CI must apply the merged set to a scratch database, and teams need timestamp-based versions or changelog includes, per [[What merge strategies are important in database development]].

The tool-in-depth on one side: [[How does Liquibase manage database schema changes]]; the deployment choreography these tools serve: [[How do you do blue-green deployments that include a database]].

> [!tip] Interview answer
> Both track applied migrations in a history table and apply only pending ones. Flyway is version-named SQL applied in order with checksums — transparent, review-friendly, dialect-bound. Liquibase is a declarative changeset model in XML/YAML/JSON/SQL with per-dialect generation, contexts, labels, preconditions, and diff/rollback support — more machinery, more abstraction. Teams choose literal SQL discipline versus cross-database abstraction; both need append-only migration discipline.
