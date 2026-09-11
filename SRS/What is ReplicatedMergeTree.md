<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Replication #SRS

# What is ReplicatedMergeTree?

> [!abstract] Short answer
> ReplicatedMergeTree is the MergeTree variant where every replica stores full copies of the table's data parts and coordinates through ClickHouse Keeper: inserts are asynchronous multi-master, metadata (schema, part lists, merge and mutation plans) lives in Keeper, and data parts are fetched between replicas by content hash. Replication works per table, independent of sharding.

## Mechanics

Each replica runs the same `CREATE TABLE ... ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/table', '{replica}')` — the first argument is the Keeper path, the second the replica name; creating the table on another server adds a replica and backfills it from existing ones. Data itself replicates at part level: an INSERT writes locally, registers the part (identified by a content-hash block id) in [[What is ClickHouse Keeper]], and other replicas fetch it in the background — deduplicating identical inserts by the same block hash. INSERT and ALTER payloads replicate; CREATE/DROP/ATTACH/DETACH/RENAME are executed on a single server and do not replicate. Each block (up to `max_insert_block_size` = 1048576 rows) is written atomically, and by default an INSERT is acknowledged after *one* replica persisted it — `insert_quorum` raises that to N replicas.

```sql
CREATE TABLE hits ON CLUSTER main
(
    EventDate Date,
    CounterID UInt32
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/hits', '{replica}')
PARTITION BY toYYYYMM(EventDate)
ORDER BY (CounterID, EventDate);
```

**Listing 1.** Typical sharded+replicated DDL: `{shard}` and `{replica}` macros resolve per server; `ON CLUSTER` issues the DDL everywhere.

```d2
r1: "Replica 1\nINSERT lands locally" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
keeper: "ClickHouse Keeper\npart registry, merges,\nmutations, schema" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
r2: "Replica 2\nfetches part in background" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
r1 -> keeper: register part
keeper -> r2: learn about part
r2 -> r1: fetch compressed part
```

**Fig. 1.** Keeper coordinates, replicas transfer data directly; inserts commit locally and replicate asynchronously.

> [!warning] "Replicated" is not "synchronous" and not "backup"
> Default durability is one replica before ack — a lost server can lose unreplicated parts unless `insert_quorum` is set; recently inserted data appears on other replicas with latency. And if Keeper is unreachable, replicated tables go read-only and INSERTs throw — Keeper is a hard dependency, not an optimization. Recovery moves broken parts to `detached/` and copies missing ones; it never silently deletes.

> [!tip] Interview answer
> ReplicatedMergeTree replicates at table level through Keeper: replicas register parts by content hash, fetch data from each other asynchronously, and every INSERT/ALTER is multi-master with atomic blocks. Schema and part metadata live in Keeper, inserts ack on one replica by default (insert_quorum for more), and losing Keeper makes tables read-only — it's coordination, not a synchronous replication protocol. The cloud-native evolution drops the copying entirely: [[What is SharedMergeTree]] stores parts once in object storage.
