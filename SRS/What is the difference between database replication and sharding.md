<!--
reps: 0
priority: 0
-->
#Databases/Replication #Databases/Partitioning #SRS

# What is the difference between database replication and sharding

> [!abstract] Short answer
> **Replication copies the same data onto several nodes — every replica holds everything, and the gain is read throughput and failover. Sharding splits one logical dataset across nodes — every shard holds its own slice by key, and the gain is write throughput and working-set scale.** They solve different bottlenecks and are routinely combined: each shard is itself a replicated group.

## The mechanics and what each one buys

**Replication** duplicates the change log: MySQL ships the binlog, PostgreSQL streams WAL, MongoDB replicates the oplog across a replica set. Every copy holds the whole dataset; reads can spread across replicas, but writes still go through the primary, so write capacity does not grow — and replicas trail by their lag, with failover possibly losing tail commits. **Sharding** partitions by a shard key: hash or range of the key decides which node owns which rows (user_id → shard 3; tenant → shard 7). Each shard owns a distinct slice, so total write throughput and storage scale with node count; the price is that every query must know its shard — key-based lookups hit one shard, while queries without the shard key scatter-gather across all of them, and cross-shard transactions become expensive two-phase work.

```d2
direction: right
rep: "Replication: copies\nReplica 1 = full data\nReplica 2 = full data\n(reads, failover)" {
  width: 280
  height: 130
  style.fill: "#e3f2fd"
}
sh: "Sharding: slices\nShard 1 = users A..H\nShard 2 = users I..P\n(writes, storage scale)" {
  width: 290
  height: 130
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Copies versus slices: replication multiplies the same dataset for reads and availability; sharding divides it for writes and size.

The two compose in real systems: MongoDB and ClickHouse/CockroachDB-style clusters replicate every shard across nodes — the shard answers write scale, the replicas per shard answer availability and local reads. Oracle's sharding documentation draws the same line: horizontal partitioning across shards, each shard a replicated unit. Inside a *single* node, partitioning (declarative ranges in PostgreSQL, PARTITION BY in MySQL/ClickHouse) splits tables logically without adding nodes — the third concept this card is routinely confused with, and its own drill in [[How do you design good database partitioning]].

> [!warning] Sharding is not a fix for "the database is slow" — it is a tax you take when nothing else works
> Shard first, and everything that was one transaction becomes distributed: no cross-shard FKs, two-phase or saga-style writes, scatter-gather queries, and a shard-key choice that determines performance for years — pick a low-cardinality or skew-prone key and one shard melts while others idle (see [[How do you choose a ClickHouse sharding key]] for the same trade at engine level). Re-sharding later is a migration project. Replication first, sharding when write volume or dataset size genuinely outgrows one node.

The replication mechanics: [[What is Master-Slave]]; the intra-node version of splitting: [[How does PostgreSQL declarative partitioning work]]; scaling contrast with NoSQL stores: [[How do NoSQL databases scale compared with SQL databases]].

> [!tip] Interview answer
> Replication copies the full dataset to replicas that serve reads and failover; sharding slices the data by key across nodes so writes and storage scale horizontally. They compose — each shard replicated. The cost profiles differ: replication costs lag and a single write path; sharding costs scatter-gather queries, cross-shard transactions, and a careful shard key. Partitioning, by contrast, splits tables within one node.
