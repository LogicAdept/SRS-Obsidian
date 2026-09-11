<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Replication #SRS

# What is the difference between streaming and logical replication in PostgreSQL?

> [!abstract] Short answer
> Streaming replication copies WAL records physically: the standby is a byte-identical clone of the same major version, replicated wholesale, read-only, with the same schema and system catalog state. Logical replication decodes WAL into row-level changes per table and applies them through SQL: subscriber tables can differ in layout, the subscriber is writable, versions can differ — the cost is heavier decoding, no DDL replication, and per-table management.

## Side by side

| | Streaming (physical) | Logical |
|---|---|---|
| Unit | whole cluster, WAL bytes | tables in publications, row changes |
| Standby writable | no (hot standby reads only) | yes (conflicts possible) |
| Schema/DDL | identical; DDL replays | DDL not replicated; manage separately |
| Versions | same major version | cross-version allowed (upgrade path) |
| Granularity | all databases | per publication/subscription |
| Setup | base backup + wal_level replica | wal_level logical + publications |

```d2
p: "Primary\nwal_level = replica" {width: 250; height: 70}
pb: "Primary\nwal_level = logical" {width: 250; height: 70}
sb: "Standby\nWAL replay, byte-identical" {width: 300; height: 80}
dec: "Logical decoding\nwalsender -> row stream" {width: 300; height: 80}
sub: "Subscriber\napplies row changes via SQL\nwritable, own schema" {width: 320; height: 90}
p -> sb: "streaming"
pb -> dec -> sub: "logical"
```

**Fig. 1.** One mechanism (WAL), two consumers: byte replay versus decoded rows.

## The operational consequences

- Streaming failover is the HA story: promote the standby; slots ([[What is a replication slot in PostgreSQL]]) keep the primary from recycling WAL the standby still needs.
- Logical replication starts with a snapshot copy of published tables, then continuous changes in commit order per subscription; conflicts (subscriber-side writes) stop the apply and need manual resolution.
- Logical subscriptions are the standard near-zero-downtime major-version upgrade path, complementing pg_upgrade ([[How do you do a PostgreSQL major version upgrade]]); the change-stream itself is the basis of CDC tooling ([[What is change data capture with Kafka]]).
- Sequence state and large object changes are not logically replicated; TRUNCATE is.

> [!warning] Logical replication does not carry DDL — by design
> Adding a column on the publisher with no matching subscriber column stops the apply with an error until both sides match. Teams that treat logical replication as "magic sync" discover this on the first schema migration. Streaming clusters share this pain differently: DDL replays everywhere at once, including the mistakes ([[What is ACCESS EXCLUSIVE in PostgreSQL]] — the lock travels too).

> [!tip] Interview answer
> Streaming is physical: the standby replays WAL and is a read-only identical twin of the same version — failover and read scaling. Logical decodes WAL into per-table row changes applied via SQL into possibly different schemas, writable and cross-version — selective replication, upgrades, CDC. Logical skips DDL and sequences; streaming skips nothing, including your errors.
