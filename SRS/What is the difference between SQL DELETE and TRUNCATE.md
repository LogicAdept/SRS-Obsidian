<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is the difference between SQL DELETE and TRUNCATE?

> [!abstract] Short answer
> **DELETE** is DML: row-by-row removal, fires triggers, respects FK constraints, logs each row, and (PostgreSQL) leaves dead tuples for vacuum. **TRUNCATE** is DDL-level: deallocates the whole table's storage in one operation — faster by orders of magnitude on big tables, fires only statement-level TRUNCATE triggers, and resets identity sequences by default. SQL Server/MySQL: TRUNCATE is minimally logged, non-row-wise. PostgreSQL's twist: TRUNCATE is *transactional* — it can be rolled back ([[What integrity constraints exist in SQL]]).

The mechanism difference drives everything. DELETE without WHERE still visits rows (SQLite applies its internal "truncate optimization" for the unfiltered case — the row-store equivalent of what TRUNCATE does formally); TRUNCATE discards the storage allocation itself — O(1)-ish bookkeeping versus O(N) row processing. The verified demo shows DELETE's selective form doing exactly that: remove only `lvl = 'info'` rows, count the survivor — the operation TRUNCATE cannot do, since TRUNCATE has no WHERE. The decision matrix: full reset of a staging/work table on a schedule — TRUNCATE (speed, minimal WAL, sequence reset); partial or conditional removal — DELETE only; deletion that must fire per-row audit triggers — DELETE (TRUNCATE fires neither row triggers nor FK cascades; it *errors* on referencing tables unless CASCADE — documented behavior worth quoting). The FK interaction is the sharpest edge: TRUNCATE on a referenced table fails outright without `CASCADE` (which truncates referencing tables too — a bigger blast radius than any DELETE), while DELETE cascades row-by-row with per-row cost. The portability footnote: SQLite has no TRUNCATE statement at all — `DELETE FROM t` is the idiom, with the engine's own unfiltered-delete optimization; PostgreSQL's TRUNCATE being transactional is the divergence from SQL Server's folklore ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE logs (id INTEGER PRIMARY KEY, lvl TEXT);
INSERT INTO logs VALUES (1,'info'),(2,'error'),(3,'info');

DELETE FROM logs WHERE lvl = 'info';
-- (row-wise, filterable, trigger-firing removal)
SELECT * FROM logs;
-- 2|error
-- TRUNCATE TABLE logs;  -- not SQLite SQL; on PostgreSQL:
-- (deallocates the whole table: no WHERE, resets sequences by default,
--  transactional -- ROLLBACK restores the rows on PG)
```

**Listing 1.** Verified on SQLite 3.53.1 for the DELETE half — selective, row-wise, countable. TRUNCATE is the DDL-level complement documented for PostgreSQL: whole-table deallocation, no WHERE, rollback-able there, absent in SQLite.

```d2
direction: right
d1: "DELETE
DML, row-by-row
WHERE + triggers + FK rows" {width: 220; height: 90}
d2: "TRUNCATE
DDL-level, whole table
fast, resets sequence" {width: 220; height: 90}
q1: "partial removal / audit trail" {width: 220; height: 80}
q2: "full reset of big staging table" {width: 230; height: 80}
d1 -> q1
d2 -> q2
```

**Fig. 1.** Two removal models with two decision criteria: granularity and audit needs keep DELETE; wholesale speed on big tables picks TRUNCATE — with FK blast radius checked first.

> [!warning] TRUNCATE CASCADE is a schema-wide event, not a table-wide one
> It truncates every table that references the target through FK chains — on a live database, "clear the staging table" becomes an incident deleting reference data. Check pg_constraints before scripting TRUNCATE; prefer DELETE or ON DELETE actions when the dependency graph is unclear ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> DELETE is DML: row-by-row, filterable with WHERE, fires row triggers, honors FK cascades, and in PostgreSQL leaves dead tuples for vacuum. TRUNCATE is DDL-level: the whole table's storage is deallocated at once — orders of magnitude faster on big tables, resets identity sequences, fires only statement triggers, and cannot take a WHERE. The nuances I quote: PostgreSQL's TRUNCATE is transactional and rolls back, unlike SQL Server's folklore; it refuses on referenced tables without CASCADE, which truncates them too; and SQLite has no TRUNCATE — DELETE is the idiom there. Selective or audited removal is DELETE; full staging-table resets are TRUNCATE.
