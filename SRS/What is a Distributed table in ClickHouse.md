<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Replication #SRS

# What is a Distributed table in ClickHouse?

> [!abstract] Short answer
> The Distributed engine is a *virtual* table over local tables on a cluster's shards: `Distributed(cluster, database, table[, sharding_key])`. INSERTs split data by the sharding key and send it to the right shards (in the background), SELECTs fan out to every shard and merge the results — it is a routing and aggregation layer, not a storage engine.

## Mechanics

The engine references a cluster defined in the server config (no dynamic config; clusters reload without restart) and a local table that must exist on every shard. On INSERT, the block is split by the sharding key expression and written first to local filesystem pending dirs, then forwarded asynchronously (`distributed_background_insert_*` settings control pacing; pending files are visible in the table's directory — an at-least-once queue). On SELECT, the query is rewritten per shard, executed in parallel, and the initiator merges partial results; `prefer_localhost_replica` biases work to the local node. A common topology: `ON CLUSTER` creation of a Distributed table over sharded `ReplicatedMergeTree` locals ([[What is ReplicatedMergeTree]]), so each shard is also fault tolerant.

```sql
CREATE TABLE hits_distributed ON CLUSTER main AS default.hits
ENGINE = Distributed(main, default, hits, rand());

SELECT CounterID, count()
FROM hits_distributed
WHERE EventDate >= '2026-09-01'
GROUP BY CounterID;   -- fans out, shards return partial aggregates
```

**Listing 1.** A Distributed table with random sharding for even load; the SELECT is one statement over all shards.

## What it does not do

Distributed performs no storage, no local indexes, and no global coordination beyond query fan-out: correctness of JOINs across shards needs care ([[What is GLOBAL JOIN in ClickHouse]]), deduplication and ordering semantics follow the local engines, and each shard's data volume is the designer's responsibility — the sharding key determines everything ([[How do you choose a ClickHouse sharding key]]). In ClickHouse Cloud the Distributed engine is replaced by shared-storage architectures ([[What is SharedMergeTree]]), which remove shard routing from user code entirely.

> [!warning] "INSERT succeeded" does not mean "data arrived"
> The engine acknowledges after local staging; the background forward can lag or retry — monitoring pending files and `system.distribution_queue` (older versions) is part of operating this topology. Combined with async replication, end-to-end visibility windows are asynchronous at two layers, which surprises teams used to single-node acks.

> [!tip] Interview answer
> Distributed is a virtual routing layer over local MergeTree tables: INSERTs shard rows by key and forward asynchronously, SELECTs fan out and merge. It holds no data itself, requires cluster config and identical local tables, and shifts the hard problems — key choice, cross-shard joins, delivery monitoring — to you.
