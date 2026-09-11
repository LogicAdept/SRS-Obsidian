<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is the difference between VACUUM and VACUUM FULL?

> [!abstract] Short answer
> Plain VACUUM is a concurrent garbage collector: it removes dead tuples and marks space reusable inside the existing file, needing only a `SHARE UPDATE EXCLUSIVE` lock — reads and writes continue. VACUUM FULL rewrites the entire table into a new compacted file and requires an `ACCESS EXCLUSIVE` lock that blocks everything for the duration, so it is an offline operation.

## Side-by-side

| | VACUUM | VACUUM FULL |
|---|---|---|
| Lock | SHARE UPDATE EXCLUSIVE | ACCESS EXCLUSIVE |
| DML during run | allowed | blocked |
| File size | unchanged | shrunk to near-live size |
| How it frees space | FSM bookkeeping | full table rewrite |
| Extra disk | none | ~2x table size during rewrite |
| Speed | incremental | proportional to table size |

```d2
old: "Table file\nlive + dead pages" {width: 250; height: 70}
vac: "VACUUM\nmark dead pages reusable in place\nfile keeps its size" {width: 330; height: 100}
new: "VACUUM FULL\ncompact copy built, swap in\nfile shrinks" {width: 330; height: 100}
old -> vac
old -> new
```

**Fig. 1.** VACUUM tidies the existing file; VACUUM FULL replaces the file wholesale — hence the exclusive lock and the temporary double disk usage.

## When each is appropriate

- VACUUM — the routine tool, normally via autovacuum ([[What is autovacuum in PostgreSQL]]). It answers dead tuples ([[What is a dead tuple in PostgreSQL]]).
- VACUUM FULL — after a one-off event that left the file mostly empty (huge bulk delete, mass update migration), when downtime is acceptable and no high-availability cluster can absorb the lock.
- Online alternatives: `pg_repack` rebuilds the table without holding the exclusive lock for the whole operation ([[What is pg_repack]]); for partitioned tables, dropping old partitions shrinks instantly ([[How does PostgreSQL declarative partitioning work]]).

## Operational details

VACUUM FULL is effectively a CLUSTER without an order: it copies live tuples into a fresh relfile, then swaps. Because it must hold `ACCESS EXCLUSIVE` from start to finish ([[What is ACCESS EXCLUSIVE in PostgreSQL]]), a few minutes of runtime means minutes of full outage for that table, including reads. During an anti-wraparound emergency it is even harmful: it consumes an XID while the goal is to stop consuming them.

> [!warning] The popular lie: "run VACUUM FULL regularly to keep the DB healthy"
> Scheduled VACUUM FULL on a live table is an anti-pattern: each run rewrites every byte and locks the table against all access. Regular VACUUM plus sensible autovacuum settings prevent pathological growth in the first place; VACUUM FULL is a last-resort, scheduled-maintenance-window tool.

> [!tip] Interview answer
> VACUUM is online garbage collection: frees dead-tuple space in place under a SHARE UPDATE EXCLUSIVE lock but never shrinks the file. VACUUM FULL compacts by rewriting the whole table under ACCESS EXCLUSIVE, so it blocks all access and needs spare disk. For online compaction you reach for pg_repack or partition drops instead.
