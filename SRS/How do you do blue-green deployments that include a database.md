<!--
reps: 0
priority: 0
-->
#DevOps/Deployment/Strategies #Databases #SRS

# How do you do blue-green deployments that include a database

> [!abstract] Short answer
> **Run two identical environments — blue (live) and green (next release) — and switch traffic at the router; the database is the hard part, so deploy schema changes separately, in a backward-compatible (expand) step that both application versions can use, and only remove old structures (contract) after the switch.** A shared schema must serve the old and the new app at the same time.

## The sequence that keeps rollback possible

Blue-green for stateless code is a router flip. With a database behind both versions, the flip order matters: (1) **Expand** — apply schema changes that are purely additive: new tables, new nullable columns, new indexes built concurrently so writes are not blocked. (2) **Deploy the green app** against the expanded schema and test it while blue still serves traffic; both versions now coexist on one schema. (3) **Switch** traffic blue → green, ideally with in-flight transactions drained (AWS's RDS Blue/Green Deployments automate the database side: green stays in sync with blue through replication, and switchover completes in under a minute with built-in guardrails). (4) **Contract** — after a soak window, drop the old columns, tables, and NOT NULL re-adds the old version needed.

Martin Fowler's original write-up states the governing rule: separate schema deployment from application upgrade. First a *database refactoring* that supports both old and new code, then the application cutover, then removal of the old-version support once the release has bedded down.

```d2
direction: right
blue: "BLUE (live)\napp v1" {
  width: 190
  height: 90
  style.fill: "#e3f2fd"
}
green: "GREEN (staging)\napp v2" {
  width: 190
  height: 90
  style.fill: "#e8f5e9"
}
db: "Database\nexpand: additive schema\nserves v1 and v2" {
  width: 260
  height: 110
  style.fill: "#fff3e0"
}
router: "Router" {
  width: 130
  height: 70
  style.fill: "#eeeeee"
}
router -> blue: "1. traffic"
blue -> db
green -> db: "2. tested against same schema"
router -> green: "3. switch"
```

**Fig. 1.** Both environments point at one database whose schema is expanded to serve both versions; only after the router flip is the old version's schema support removed.

## Why plain blue-green breaks on databases

Two live application versions imply two schema expectations. A column the new code makes NOT NULL, a renamed table, or a value-format change will crash the old version mid-request. Hence the discipline: migrations must be backward-compatible during the overlap window, dual-writes or triggers may be needed to backfill new columns, and destructive changes wait for the contract phase. If true schema incompatibility is unavoidable (a rewrite), the fallback is a copy of the database for green plus a change-data-capture sync and a cutover freeze — heavier, rarer, and planned.

> [!warning] "Two databases, one per environment" silently forks your data
> Pointing blue and green at separate databases and syncing them "somehow" creates split-brain writes: orders taken by blue after green's snapshot are missing in green at switchover. Keep one authoritative database; replicate for the staging copy (as RDS does), never let both ends accept writes to different copies during the switch.

Connect this to zero-downtime column changes in [[How do you add a column to a large PostgreSQL table without downtime]], and to the migration-tool layer in [[How does Liquibase manage database schema changes]].

> [!tip] Interview answer
> Blue-green keeps two identical environments and flips the router. With a database, I split the migration from the release: additive, backward-compatible schema first — new tables and nullable columns, indexes built online — then deploy green, test, switch traffic, and contract the old structures after a soak period. RDS-style managed blue-green can replicate blue into green and switch over in under a minute with guardrails.
