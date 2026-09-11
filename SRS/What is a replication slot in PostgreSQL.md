<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Replication #SRS

# What is a replication slot in PostgreSQL?

> [!abstract] Short answer
> A replication slot is a named marker on the primary that remembers how far a consumer (streaming standby or logical subscriber) has progressed and guarantees the primary retains everything that consumer still needs: WAL segments are never recycled before the slot confirms, and (with hot_standby_feedback) vacuum is restrained. The guarantee cuts both ways: an abandoned slot holds WAL and rows forever until pg_wal fills up.

## What it solves

Without slots, a disconnected standby that falls behind can lose WAL the primary already recycled (wal_keep_size and archiving are the manual workarounds). A slot tracks the consumer's restart position precisely — only the segments actually needed are retained ([[What is the difference between streaming and logical replication in PostgreSQL]]).

```sql
SELECT slot_name, slot_type, active, restart_lsn,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained
FROM pg_replication_slots;
-- drop abandoned ones explicitly:
SELECT pg_drop_replication_slot('stale_report_slot');
```

**Listing 1.** The health check: retained WAL per slot; slots with active = false and a growing gap are incidents.

```d2
prim: "Primary\nWAL segments" {width: 220; height: 60}
s1: "Physical slot\nstandby position" {width: 260; height: 70}
s2: "Logical slot\ndecoder position" {width: 260; height: 70}
ok: "Recycle WAL before\nrestart_lsn only" {width: 300; height: 70}
danger: "Dead consumer\nslot retains everything\npg_wal fills, disk full" {width: 330; height: 90}
prim -> s1
prim -> s2
s1 -> ok
s2 -> ok
s1 -> danger: "consumer gone"
s2 -> danger
```

**Fig. 1.** The slot is a lease: precise retention while alive, unbounded retention if orphaned.

## Types and behavior

- **Physical slots** — one per streaming standby; retain WAL only.
- **Logical slots** — for decoding (subscriptions, CDC pipelines); additionally pin catalog rows against vacuum; creating one needs wal_level = logical. On a hot standby, logical slots require hot_standby_feedback and can be invalidated if required rows are removed.
- Created via SQL (`pg_create_physical_replication_slot`, `pg_create_logical_replication_slot`) or in `postgresql.auto.conf` via `primary_slot_name` on the standby.

## Guardrails

Cap the damage with `max_slot_wal_keep_size` (a slot retaining beyond it is marked failed rather than filling the disk); monitor `pg_replication_slots` for inactive slots; treat slot lifecycle as part of consumer lifecycle — a dropped subscriber must drop its slot ([[Why do long-running transactions hurt PostgreSQL]] — the same horizon-pinning idea, at the WAL layer).

> [!warning] An inactive slot is a disk-full timer
> A standby that is decommissioned without dropping its slot silently retains every WAL segment from the moment it disconnected — reads, archives, checkpoints continue until pg_wal hits the partition limit and the primary stops. The monitoring alert on inactive slots with growing retained WAL is one of the cheapest production safeguards in PostgreSQL.

> [!tip] Interview answer
> A replication slot is a named position marker that makes the primary retain exactly what a consumer still needs — WAL for physical standbys, WAL plus catalog rows for logical decoders. It removes the guesswork of wal_keep_size, and it introduces the opposite failure: an orphaned slot retains WAL forever, so you cap it with max_slot_wal_keep_size and alert on inactive slots.
