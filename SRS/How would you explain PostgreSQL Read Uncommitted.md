<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How would you explain PostgreSQL Read Uncommitted?

> [!abstract] Short answer
> PostgreSQL accepts SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED but never provides it: dirty reads do not exist in the engine, so Read Uncommitted behaves exactly like Read Committed — the only sensible mapping of the standard levels onto MVCC snapshots, as the documentation states. Interviewers use it to check whether you know PostgreSQL's isolation is snapshot-based, not lock-based.

## Why the level collapses

A dirty read means seeing another transaction's uncommitted writes. In PostgreSQL uncommitted row versions are simply invisible: visibility is computed from `xmin`/`xmax` against the snapshot ([[What are xmin and xmax in PostgreSQL]]), and an uncommitted creator's version fails the check for everyone but itself. There is no mode that would relax this — relaxing it would require a fundamentally different storage design ([[What is MVCC in PostgreSQL]]).

```sql
BEGIN ISOLATION LEVEL READ UNCOMMITTED;
SHOW transaction_isolation;    -- 'read uncommitted' accepted...
-- ...but reads still take a Read Committed snapshot:
-- no dirty reads, per-statement fresh snapshots
COMMIT;
```

**Listing 1.** The setting is accepted and reported back, with no behavioral difference — the documented "internally only three distinct isolation levels" statement.

```d2
std: "SQL standard\nRead Uncommitted:\ndirty reads allowed" {width: 320; height: 80}
pg: "PostgreSQL\nMVCC makes uncommitted\nrows invisible — always" {width: 320; height: 80}
map: "Read Uncommitted ->\nRead Committed behavior" {width: 330; height: 80}
std -> map
pg -> map
```

**Fig. 1.** The mapping is one-way: you can ask for the level, the engine answers with Read Committed semantics.

## What to say next in the interview

- The default is Read Committed: each statement gets a fresh snapshot; concurrent updates re-evaluate WHERE on the updated rows ([[What are SQL transaction isolation levels]]).
- The anomalies that Read Uncommitted would permit (dirty reads) are impossible at every level; the real PG-specific stories are what Repeatable Read adds ([[How does Repeatable Read prevent phantom reads in PostgreSQL]], [[How would you explain Repeatable Read PG]]) and how Serializable detects conflicts ([[What is PostgreSQL Serializable Snapshot Isolation]]).
- The dirty-read vocabulary still matters cross-engine: other systems have real Read Uncommitted ([[How do you handle transaction isolation anomalies]] for the general anomaly catalog).

> [!warning] "PostgreSQL supports four isolation levels" is the trap phrasing
> It accepts four; it implements three. A candidate who answers with the standard table verbatim — dirty reads possible at Read Uncommitted — has memorized the SQL standard, not PostgreSQL. The correction is one sentence and instantly separates book knowledge from engine knowledge.

> [!tip] Interview answer
> PostgreSQL has no Read Uncommitted behavior: MVCC makes uncommitted versions invisible, so the level is accepted and then behaves as Read Committed — the engine implements only three distinct levels. No dirty reads exist at any setting; the differences between levels start at nonrepeatable reads and phantoms.
