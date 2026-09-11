<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A **temporary table** is a table scoped to a session (or transaction): created with `CREATE TEMP TABLE`, it lives in the session's private namespace, vanishes at session end, and is invisible to other connections — ideal for multi-step query work (stage, transform, join) without touching production tables or contending for locks ([[When should you use a subquery JOIN or CTE in SQL]]).

The verified demo proves the isolation: the temp table is readable from its own connection and returns `no such table` from a second one. The decision it settles: complex logic that a single statement cannot express cleanly (or that would recompute an expensive intermediate many times) gets staged — write the intermediate result once, then query it repeatedly with full indexing available (`CREATE INDEX` works on temp tables). The sibling tools and their boundaries: a **CTE** is statement-scoped and unindexed — perfect for named readability, wrong for repeated random access ([[What is the difference between Nested Loop Hash Join and Merge Join]]); a **table variable** (SQL Server) is transaction-scoped-ish with different statistics behavior; a **real staging table** persists and is visible to other sessions — needed only when multiple processes share the work. Temp-table pitfalls worth naming: they bloat temp storage on huge data (PostgreSQL temp buffers, SQLite temp store PRAGMA), they pin session memory, and long-lived connections accumulate forgotten temp tables — cleanup is per-session at disconnect, not on last use ([[What harmful SQL patterns or pitfalls do you know]]). PostgreSQL distinguishes ON COMMIT PRESERVE/DELETE/DROP ROWS for the transaction-scoped flavor.

```sql
CREATE TEMP TABLE scratch (x INTEGER);
INSERT INTO scratch VALUES (7);
SELECT * FROM scratch;
-- 7
-- (from a SECOND connection:)
-- SELECT * FROM scratch;
-- ERROR: no such table: scratch
-- (temp tables are session-private: same name, different namespaces)
```

**Listing 1.** Verified on SQLite 3.53.1. Visible to its session, invisible to the next — the temp table is a private workspace that needs no permissions, no locking, and no cleanup.

```d2
direction: right
s1: "session A
CREATE TEMP TABLE" {width: 200; height: 80}
s2: "session B
same name? own namespace" {width: 220; height: 80}
s3: "session ends
temp table dropped" {width: 190; height: 80}
t: "tempdb / temp store
per-session storage" {width: 200; height: 80}
s1 -> t
s2 -> t
s1 -> s3
```

**Fig. 1.** Temp tables live in a per-session layer: private by construction, gone by session end — a workspace nobody else can see or clean up for you.

> [!warning] Temp tables are a code smell when they replace a single query — and a savior when they replace N+1
> "Loop over rows, insert into temp, update per row" is application logic misplaced into SQL; but "compute expensive aggregate once into temp, join twice" turns repeated scans into one. The test: does the temp table remove *repeated* work, or just move the loop into SQL syntax? ([[What is the N plus 1 problem in SQL]]).

> [!tip] Interview answer
> A temp table is session-scoped storage: CREATE TEMP TABLE, invisible to other connections — my demo shows the second session failing to see it — and dropped when the session ends. I use it for multi-step transformations: stage an expensive intermediate once, index it, join repeatedly. Versus a CTE, it survives across statements and can be indexed; versus a real staging table, it is private and self-cleaning. The pitfalls are temp-store bloat and forgotten tables on long-lived connections, so I keep their lifetime short and scoped.
