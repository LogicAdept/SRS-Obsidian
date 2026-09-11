<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS

# How would you explain the SQL VACUUM command in PostgreSQL?

> [!abstract] Short answer
> VACUUM is PostgreSQL's maintenance command that scans tables, removes dead tuples that no snapshot can see, marks that space as reusable, and freezes old row versions to protect against transaction ID wraparound. It never shrinks the table file and never blocks normal reads or writes — unlike VACUUM FULL, which rewrites the whole table.

## What it actually does

1. Scans pages that may contain dead tuples (normal VACUUM skips all-visible pages using the visibility map).
2. Removes dead tuples and records freed space in the Free Space Map for future inserts.
3. Updates the visibility map (all-visible and all-frozen bits).
4. Freezes tuples whose `xmin` is older than `vacuum_freeze_min_age` and advances `relfrozenxid`.
5. Optionally updates planner statistics when run as `VACUUM ANALYZE`.

```sql
VACUUM;                          -- whole database, standard mode
VACUUM orders;                   -- one table
VACUUM (VERBOSE, ANALYZE) orders;-- progress output + fresh statistics
VACUUM (FREEZE) events;          -- aggressive freeze, e.g. before major upgrade
```

**Listing 1.** Everyday forms of VACUUM; the parenthesized options syntax is the modern one.

```d2
scan: "Scan heap pages\n(skip all-visible)" {width: 260; height: 80}
reclaim: "Remove dead tuples\nrecord space in FSM" {width: 280; height: 80}
vm: "Set visibility-map bits\nall-visible / all-frozen" {width: 290; height: 80}
freeze: "Freeze old tuples\nadvance relfrozenxid" {width: 280; height: 80}
scan -> reclaim -> vm -> freeze
```

**Fig. 1.** A VACUUM pass is garbage collection plus bookkeeping: the FSM feeds later inserts, the visibility map feeds index-only scans, and freezing feeds wraparound protection.

## What VACUUM does not do

- It does not reduce the file size on disk; it only makes space inside the file reusable. Shrinking requires VACUUM FULL or `pg_repack` ([[What is the difference between VACUUM and VACUUM FULL]], [[What is pg_repack]]).
- It does not defragment or reorder data — that is CLUSTER.
- It does not update statistics by itself — pair it with ANALYZE.

## Where it runs from

Usually autovacuum runs it for you ([[What is autovacuum in PostgreSQL]]); manual VACUUM is for after bulk loads, bulk deletes, before `pg_upgrade`, or when tuning per-table storage parameters. Its lock is `SHARE UPDATE EXCLUSIVE`, which conflicts with DDL and other vacuum runs but not with plain DML ([[What lock granularities exist in a relational database]]).

> [!warning] VACUUM cannot clean what a snapshot protects
> Dead tuples stay if any transaction started before the deleting transaction is still running — including idle-in-transaction sessions and orphaned replication slots. VACUUM will "succeed" but remove nothing; check the vacuum horizon in `pg_stat_activity` before blaming vacuum. See [[Why do long-running transactions hurt PostgreSQL]].

> [!tip] Interview answer
> VACUUM reclaims space from dead MVCC tuples without blocking DML: it frees space inside the file (does not shrink it), maintains the visibility map, and freezes old tuples to keep the 32-bit transaction counter safe. Manual VACUUM complements autovacuum after bulk operations; VACUUM FULL is the separate, blocking, table-rewriting tool.
