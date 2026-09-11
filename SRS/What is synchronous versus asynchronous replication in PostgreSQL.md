<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Replication #SRS

# What is synchronous versus asynchronous replication in PostgreSQL?

> [!abstract] Short answer
> Asynchronous (the default): the primary confirms a commit after local WAL flush; the standby catches up later — failover can lose the last transactions. Synchronous: the primary holds each commit until the standby(s) named in synchronous_standby_names have flushed the commit's WAL to durable storage (synchronous_commit = on), or applied it (remote_apply) — zero confirmed-transaction loss, at the price of commit latency tied to the slowest sync standby.

## The durability ladder

`synchronous_commit` values, from strongest to loosest: `remote_apply` (standby applied — visible there), `on` (standby flushed to disk), `remote_write` (standby wrote to OS cache), `local` (local flush only, no standby wait), `off` (no local wait either). With `synchronous_standby_names` empty, only `on` and `off` differ meaningfully.

```d2
c: "COMMIT on primary" {width: 240; height: 60}
fl: "Local WAL flush" {width: 220; height: 60}
sw: "Standby: write / flush / apply\nper synchronous_commit level" {width: 340; height: 80}
ack: "Client told: committed" {width: 260; height: 60}
c -> fl -> sw -> ack
```

**Fig. 1.** The commit path: how far the wait extends before the client hears "committed" is exactly the durability contract.

## Mechanics and costs

- `synchronous_standby_names` lists the sync candidates (FIRST N or ANY semantics for quorum); a transaction waits until enough named standbys report the level.
- A crashed or disconnected sync standby blocks all commits — availability now depends on a second site; this is the documented tradeoff.
- The wait is per transaction and changeable: `SET LOCAL synchronous_commit = off` makes selected low-stakes transactions async while the cluster stays sync ([[What is the difference between streaming and logical replication in PostgreSQL]] — the mechanism is orthogonal to physical/logical, though most common on streaming standbys).
- `synchronous_commit = off` alone (no sync standby) still flushes WAL via the WAL writer within about three times `wal_writer_delay` — a small, bounded loss window, not a corruption risk.

## Monitoring the contract

pg_stat_replication reports write_lag, flush_lag and replay_lag per standby plus a sync_state column (sync, potential, quorum, async) — the state an application can actually observe. The contract holds only while a qualifying standby is in sync state; if none qualifies, synchronous commits block rather than silently degrade — a documented, intentional failure mode that alerting must treat as page-worthy, since it converts a standby failure into a primary outage.

## What async buys and costs

Async keeps commit latency local — masters take bursts without waiting on network round trips. The bill arrives at failover: the promoted standby may lag, and the last confirmed transactions vanish unless the old primary's WAL is recovered. For money paths and cross-region contracts, sync (often `on` to one regional standby) is the honest setting.

> [!warning] "Synchronous" is not a property of the cluster — it is a per-commit setting
> Transactions decide their own durability via synchronous_commit at commit time; mixing sync and async traffic on one primary is normal. The dangerous assumption is the reverse: believing async standbys are "safe because replication is instant" — under load lag grows, and a primary crash loses exactly the unshipped tail ([[What is a replication slot in PostgreSQL]] guarantees WAL is retained, not that it has arrived).

> [!tip] Interview answer
> Async replication confirms commits locally and lets the standby trail — fast, but failover can lose the tail. Synchronous names standbys in synchronous_standby_names and holds each commit until they flush (on) or apply (remote_apply) the WAL — no confirmed loss, but commit latency follows the network and a dead sync standby blocks writes. The knob is per-transaction, so you can mix contracts.
