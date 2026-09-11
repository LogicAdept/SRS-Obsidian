<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Transactions #SRS

# What is MVCC in PostgreSQL?

> [!abstract] Short answer
> Multi-Version Concurrency Control: PostgreSQL keeps old row versions instead of overwriting them. Each `UPDATE` writes a new tuple and marks the old one dead; every statement or transaction reads a consistent snapshot. Readers never block writers and writers never block readers — but the price is dead tuples, table bloat, and a permanent need for VACUUM.

## How versioning works

Every tuple header carries two system columns: `xmin` (the transaction that inserted the version) and `xmax` (the transaction that deleted or replaced it). A transaction takes a snapshot and decides visibility per row: the tuple's `xmin` must be committed before the snapshot, and its `xmax` must be absent, aborted, or committed after the snapshot. See [[What are xmin and xmax in PostgreSQL]].

```sql
BEGIN;
UPDATE accounts SET balance = 90  WHERE id = 1;  -- tuple v1 dead, v2 live
UPDATE accounts SET balance = 80  WHERE id = 1;  -- tuple v2 dead, v3 live
COMMIT;
-- one logical row, three physical tuples until VACUUM removes the dead ones
```

**Listing 1.** Two updates produce three heap tuples; VACUUM later reclaims the first two.

```d2
shape: sequence
writer: "Writer session\nUPDATE sets xmax on v1,\ninserts v2" {width: 300; height: 80}
reader: "Reader session\nsnapshot taken before UPDATE" {width: 300; height: 80}
heap: "Heap\ntuple v1 (xmin=10, xmax=20)\ntuple v2 (xmin=20, xmax=0)" {width: 360; height: 90}
writer -> heap: "writes new version"
reader -> heap: "checks xmin/xmax vs snapshot\nsees v1, not v2"
```

**Fig. 1.** The reader ignores the new version because its `xmin` is not committed in the reader's snapshot; no locks are taken for this read.

## What the snapshot is

In Read Committed (the default) each statement gets a fresh snapshot; in Repeatable Read and Serializable the snapshot is fixed at the first non-transaction-control statement. This is why [[What are SQL transaction isolation levels]] behave differently in PostgreSQL than in engines with read locks: isolation is implemented by snapshot filtering, not by blocking readers. See [[How would you explain MVCC PostgreSQL]] for why this design was chosen and what it costs.

## Where the costs appear

New versions live in the heap until vacuumed, so write-heavy tables accumulate dead rows. Long transactions keep old snapshots alive, which freezes the cleanup horizon. The countermeasures are VACUUM and autovacuum ([[What is autovacuum in PostgreSQL]]), HOT updates ([[What is a HOT update in PostgreSQL]]), and monitoring bloat ([[What is table bloat in PostgreSQL]]).

> [!warning] MVCC is not free
> The popular lie is "MVCC means no overhead". A single hot row updated many times per second produces a new tuple per update plus (unless HOT applies) new index entries, and VACUUM has to catch up. Unvacuumed tables grow monotonically even when the row count is constant.

> [!tip] Interview answer
> MVCC in PostgreSQL is version-based concurrency: writes create new row versions stamped with `xmin`/`xmax`, and each reader picks the version visible to its snapshot. This gives lockless reads and statement- or transaction-level snapshots, and it underpins the isolation levels. The costs are dead tuples that VACUUM must clean, bloat under long transactions, and heavier writes than in-place-update engines.
