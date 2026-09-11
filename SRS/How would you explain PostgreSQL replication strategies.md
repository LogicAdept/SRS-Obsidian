<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SystemDesign/Reliability #SystemDesign/Availability #DistributedSystems #SRS

# How would you explain PostgreSQL replication strategies?

> [!abstract] Short answer
> Two built-in families: physical (streaming) replication — a standby receives and replays the same WAL records byte-for-byte, giving an identical hot copy for failover and read scaling — and logical replication — a publisher decodes changes per table into row streams that subscribers apply into their own schemas. Around them: synchronous versus asynchronous commit, replication slots for WAL retention, and archive-based solutions.

## The map

```d2
wal: "WAL stream" {width: 200; height: 60}
phys: "Physical / streaming\nidentical cluster copy,\nsame version, read-only standby" {width: 360; height: 100}
log: "Logical\npublish/subscribe per table,\nrows decoded, versions may differ" {width: 360; height: 100}
arch: "Archiving (PITR)\nWAL segments to storage" {width: 300; height: 90}
wal -> phys: "shipping"
wal -> log: "decoding"
wal -> arch: "archiving"
```

**Fig. 1.** Everything starts from the WAL ([[What is the PostgreSQL WAL]]); the strategies differ in how they consume it.

- **Streaming (physical)**: `wal_level = replica`; a standby restores a base backup then continuously receives WAL. One primary, cascading standbys possible. The standby is read-only (hot standby queries). Failover = promote a standby. Details: [[What is the difference between streaming and logical replication in PostgreSQL]].
- **Logical**: `wal_level = logical`; publications on the primary, subscriptions on consumers; the initial table snapshot is copied, then changes stream per table. Enables version upgrades with near-zero downtime, selective table replication, and consolidation into other systems. Details: [[What is the difference between streaming and logical replication in PostgreSQL]].
- **Synchronous commit** controls the durability contract of either scheme: async (default) risks losing the last transactions on failover; sync (`synchronous_standby_names` + `synchronous_commit = on` or `remote_apply`) waits for the standby. Details: [[What is synchronous versus asynchronous replication in PostgreSQL]].
- **Slots** ([[What is a replication slot in PostgreSQL]]) guarantee a standby or logical consumer never misses WAL — with the retention danger.

Two operational notes complete the picture. First, replication applies to every change equally: DDL, grunts of maintenance, and mistakes — a standby is a mirror, not a filter. Second, lag is a first-class metric: pg_stat_replication reports write, flush and replay lag per standby, and alerting on replay lag growth is what converts "replication exists" into "replication works" ([[What is synchronous versus asynchronous replication in PostgreSQL]] for the contract those lags support).

## Choosing

HA and read replicas: streaming. Upgrades and selective or cross-version copies: logical. Backup-plus-recovery: base backup + archived WAL (PITR) — [[How do you take a PostgreSQL backup]], [[What is point-in-time recovery in PostgreSQL]]. This mirrors the general tradeoffs in [[How would you explain database replication strategies]] and contrasts with [[How would you explain MySQL replication strategies]] and [[How would you explain Oracle replication strategies]].

> [!warning] Asynchronous streaming replication is not backup
> A standby replays destruction as faithfully as it replays inserts: a dropped table on the primary is dropped on every standby within seconds. Recovery from logical mistakes needs PITR from archived WAL or a delayed standby — an HA replica answers availability, not data-recovery ([[What is point-in-time recovery in PostgreSQL]]).

> [!tip] Interview answer
> PostgreSQL replication comes in two families fed by the same WAL: physical streaming for identical hot standbys and failover, logical publish-subscribe for per-table, cross-version replication and upgrades. Commit mode — synchronous versus asynchronous — sets the data-loss window; replication slots manage WAL retention. Standbys give availability, not undo: mistakes replicate too.

## What to state before the follow-ups

Set the vocabulary first — primary, standby, wal_level, slot, publication — because the interviewer's follow-ups ride on those terms. Then the two failure axes: how much data a failover may lose (commit mode), and how much lag a consumer may accumulate (retention and monitoring). Both axes have dedicated cards ([[What is a replication slot in PostgreSQL]] for retention, [[What is synchronous versus asynchronous replication in PostgreSQL]] for the loss window), so keep the overview card to the map, not the mechanics.
