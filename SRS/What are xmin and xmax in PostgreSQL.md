<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Transactions #SRS

# What are `xmin` and `xmax` in PostgreSQL?

> [!abstract] Short answer
> They are the two system columns in every tuple header that implement MVCC visibility: `xmin` is the ID of the transaction that inserted this version, `xmax` is the ID of the transaction that deleted it or replaced it with a newer version. A row version is visible to a snapshot when its `xmin` is finished (committed) before the snapshot and its `xmax` is not finished before the snapshot.

## Visibility rules

A snapshot is essentially "all transactions that were running when I started, plus their future XIDs are invisible to me". For each candidate tuple the engine checks:

1. Is `xmin` committed and older than the snapshot? If not — invisible (except the transaction's own writes).
2. Is `xmax` set, and is it committed before the snapshot? If yes — the version is dead for this snapshot.
3. Otherwise the version is visible.

```sql
CREATE TABLE t (id int);
INSERT INTO t VALUES (1);          -- v1: xmin=100, xmax=0
UPDATE t SET id = 2;               -- v1: xmax=101 (expired)
                                   -- v2: xmin=101, xmax=0
SELECT xmin, xmax, id FROM t;      -- shows 101, 0, 2  (v2)
SELECT xmin, xmax FROM t WHERE id = 2;
```

**Listing 1.** After the update, the old version keeps `xmin=100, xmax=101`; the new one is `xmin=101, xmax=0`. Reading `xmin`/`xmax` in a query exposes the live version's stamps.

## Related header fields

- **cmin/cmax** — command IDs ordering changes made by the same transaction.
- **ctid** — physical location `(page, item)`; used by HOT chains ([[What is a HOT update in PostgreSQL]]).
- **infomask bits** — per-tuple status flags (committed, aborted, frozen) that let later readers skip lookups into the commit log.
- A special **FrozenTransactionId** marker replaces old `xmin` values during aggressive vacuum so they survive transaction ID wraparound ([[What is transaction ID wraparound in PostgreSQL]]).

## Why they matter in practice

Dead-tuple cleanup ([[What is a dead tuple in PostgreSQL]]) exists precisely to remove versions whose `xmax` has long been committed and which no snapshot can see anymore. VACUUM walks the heap, checks these stamps against the oldest running snapshot, and reclaims the space. The 32-bit width of these IDs is also the reason wraparound protection exists at all.

> [!warning] xmax is not "the deleter's ID" in every case
> `xmax` also records row locks: `SELECT FOR UPDATE` stamps `xmax` on the locked tuple without deleting it. After a lock-only transaction rolls back, the tuple is still alive — the `xmax` stamp is just a lock artifact. Treating `xmax` as proof of deletion is a popular lie.

> [!tip] Interview answer
> `xmin` and `xmax` are the MVCC stamps on every tuple: who created this version, and who deleted or replaced it. A reader compares them against its snapshot to decide visibility, VACUUM compares them against the oldest snapshot to decide what is garbage, and freezing rewrites ancient `xmin` values so the 32-bit counter can wrap safely.
