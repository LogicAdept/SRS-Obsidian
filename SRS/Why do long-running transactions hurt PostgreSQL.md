<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# Why do long-running transactions hurt PostgreSQL?

> [!abstract] Short answer
> An open transaction holds a snapshot, and the snapshot's xmin defines the vacuum horizon: dead tuples newer than it cannot be removed anywhere in the cluster. A single hours-long query or idle-in-transaction session therefore blocks cleanup, produces bloat, delays freezing (wraparound pressure), and can freeze out autovacuum workers.

## The vacuum horizon

MVCC cleanup ([[What is a dead tuple in PostgreSQL]]) can only remove tuples invisible to every snapshot. The oldest active snapshot belongs to the longest transaction — including idle-in-transaction sessions, prepared transactions, replication slots ([[What is a replication slot in PostgreSQL]]), and hot-standby feedback. Everything updated after that xmin is unremovable, no matter how many times VACUUM runs.

```d2
tx: "Long transaction\nstarted 10:00, idle 40 min" {width: 300; height: 80}
horizon: "Vacuum horizon pinned\nat 10:00" {width: 280; height: 70}
dead: "All dead tuples since 10:00\nin ALL tables are protected" {width: 340; height: 90}
av: "Autovacuum runs finish\nwithout reclaiming anything" {width: 330; height: 80}
tx -> horizon -> dead -> av
```

**Fig. 1.** The blast radius is cluster-wide: one forgotten transaction protects garbage in every table, not just the tables it touched.

## The three damage channels

1. **Bloat** — dead tuples accumulate in heap and indexes ([[What is table bloat in PostgreSQL]]), scans slow down, autovacuum burns I/O for nothing.
2. **Wraparound** — freezing cannot advance past the horizon, `relfrozenxid` age grows toward the stop-the-world limit ([[What is transaction ID wraparound in PostgreSQL]]).
3. **Locks and contention** — the session also holds row/table locks it acquired; conflicts multiply ([[How does PostgreSQL handle locks and deadlocks]]).

## Guardrails

```sql
SET idle_in_transaction_session_timeout = '5min';  -- kills idle BEGINs
SET statement_timeout = '30s';                     -- per-statement cap
SET transaction_timeout = '10min';                 -- whole-transaction cap (PG 17+)
```

**Listing 1.** Role- or database-level timeouts are the standard protection; `idle_session_timeout` covers sessions without an open transaction. Monitor with `pg_stat_activity` (columns `xact_start`, `state`, `backend_xid`) and alert on `state = 'idle in transaction'`.

> [!warning] Read-only does not mean harmless
> A long `SELECT` on a standby, or a read-only transaction on the primary, still pins a snapshot. Applications that "just hold a query open in a cursor" cause the same bloat as a write transaction. Only `DEFERRABLE` read-only serializable transactions and true snapshot-less reads escape this.

> [!tip] Interview answer
> The oldest active snapshot sets the vacuum horizon cluster-wide. A long-running or idle-in-transaction session protects every dead tuple created after it started, so autovacuum cleans nothing, tables bloat, indexes fatten, and wraparound freezing stalls. The cures are timeouts like idle_in_transaction_session_timeout, monitoring pg_stat_activity, and never shipping code that leaves transactions open.
