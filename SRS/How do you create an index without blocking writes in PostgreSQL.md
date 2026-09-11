<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# How do you create an index without blocking writes in PostgreSQL?

> [!abstract] Short answer
> Use `CREATE INDEX CONCURRENTLY`: it builds the index in several transactions with two table scans, waiting for concurrent transactions between phases, so inserts, updates and deletes continue. It is slower, cannot run inside a transaction block, and on failure leaves an INVALID index that must be dropped and rebuilt. REINDEX has the same CONCURRENTLY form since PostgreSQL 12.

## The phases

A normal CREATE INDEX takes a lock that blocks writes until done — fine on small tables, unacceptable in production. The concurrent build:

1. Registers the index as invalid in the catalogs.
2. First table scan: builds the base index; waits for transactions that modified the table to finish.
3. Second table scan: adds entries for rows created meanwhile; waits for snapshots older than the scan.
4. Marks the index valid.

```sql
CREATE INDEX CONCURRENTLY orders_created_at_idx ON orders (created_at);
-- failed run left junk? clean it:
DROP INDEX CONCURRENTLY orders_created_at_idx;
-- rebuild without blocking writes (PG 12+):
REINDEX INDEX CONCURRENTLY orders_created_at_idx;
```

**Listing 1.** The full lifecycle: create, clean up on failure, rebuild.

```d2
reg: "Register index\nINVALID" {width: 240; height: 70}
s1: "Scan 1\nbuild from existing rows" {width: 240; height: 70}
wait1: "Wait for writers\nto finish" {width: 240; height: 70}
s2: "Scan 2\nadd rows added meanwhile" {width: 250; height: 70}
valid: "Mark valid\nqueries can use it" {width: 240; height: 70}
reg -> s1 -> wait1 -> s2 -> valid
```

**Fig. 1.** The extra scans and waits are the price of never blocking DML; only the first scan can use parallel workers.

## Operational rules

- No transaction block: run it outside BEGIN; migration frameworks need a flag to skip wrapping DDL.
- Locks still taken: brief `SHARE UPDATE EXCLUSIVE` phases — it conflicts with other DDL and other concurrent index builds on the same table, not with DML ([[What lock granularities exist in a relational database]]).
- Unique concurrent builds enforce uniqueness already during the build; a conflict can abort the build.
- On partitioned tables the parent CREATE INDEX CONCURRENTLY is not allowed; build per-partition and attach ([[How does PostgreSQL declarative partitioning work]]).
- Long-running transactions are the main latency source: the scans wait for them ([[Why do long-running transactions hurt PostgreSQL]]).

> [!warning] Failure leaves an INVALID index that still costs writes
> If the build dies (deadlock, uniqueness violation), the half-built index remains: ignored by queries but maintained by every write. `\d table` shows INVALID. The fix is DROP INDEX CONCURRENTLY and retry — leaving it "for later" silently degrades every DML ([[How do you find unused indexes in PostgreSQL]] helps find the leftovers).

> [!tip] Interview answer
> CREATE INDEX CONCURRENTLY builds in two scans across several transactions, waiting out concurrent writers, so writes never block. It is slower, forbidden inside transaction blocks, and a failed run leaves an INVALID index that still taxes writes — drop it and retry. REINDEX CONCURRENTLY is the same story for rebuilds.
