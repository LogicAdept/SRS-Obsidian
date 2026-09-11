<!--
reps: 0
priority: 0
-->
#Databases/Sharding #SystemDesign/Scalability #SRS

# What problem does database sharding solve

> [!abstract] Short answer
> Sharding solves the problem that one database server eventually cannot hold or serve the whole dataset: it splits data horizontally across independent servers, each owning a subset of rows, so storage, CPU, RAM and — crucially — write throughput scale with the number of shards. It is the answer when read replicas stop helping because the primary is saturated by writes, or when the working set and write volume exceed any single node.

## The ceiling it removes

A primary database has one write path: every insert and update serializes through its WAL/redo machinery, and its indexes must fit in a working set one machine can cache. Read replicas multiply read capacity ([[How would you explain database replication strategies]]), but every replica still replays every write, so they add nothing to write throughput and each carries the whole dataset. Sharding breaks both walls at once: rows are divided by a shard key (user id, tenant, hash of a key) across N independent primaries; each stores 1/N of the data, replays 1/N of the writes, and holds 1/N of the working set. Write throughput, storage and cache hit rate all scale with N — this is why sharding-first engines (wide-column stores, MongoDB) dominate high-ingest workloads, and why a mature relational system adopts sharding only when vertical scale and replicas are exhausted ([[How do NoSQL databases scale compared with SQL databases]] contrasts the growth curves).

## What sharding is not, and what it costs

Sharding is horizontal row-splitting across servers; it is not vertical partitioning (splitting columns into tables — [[How does vertical partitioning differ from horizontal partitioning]]) and not plain replication (full copies, not disjoint subsets). The price is paid in query shape and operations: every query should name the shard key or it fans out to all shards; cross-shard transactions and unique constraints need coordination (2PC, sagas, composite keys embedding the shard id); rebalancing shards moves data; and hot spots follow a bad key choice — a hashed key spreads uniformly but kills range queries, a range key preserves ranges but concentrates celebrities or time-monotonic inserts on one shard. [[How would you explain horizontal database sharding]] covers the mechanics; [[How do you choose a ClickHouse sharding key]] shows the same key-design discipline in a concrete engine.

```text
before: 1 primary        writes W/s, rows R, working set M
after:  N shards         each ~W/N writes/s, R/N rows, M/N working set
cost:    queries must carry the shard key, or fan out to N shards
         cross-shard txn / global uniqueness -> coordination layer
```

**Listing 1.** The scaling arithmetic and the two standing costs.

> [!warning] The shard key is a one-way architectural decision
> Changing the shard key later means moving the entire dataset. Choose the key by your dominant query — not by what is easy today — because every query that cannot name it pays a full scatter-gather forever.

> [!tip] Interview answer
> Sharding solves single-server saturation: it splits rows by a shard key across independent primaries, so writes, storage and working set scale with shard count — which replicas alone cannot buy. The costs are key-shaped queries, cross-shard transactions and rebalancing, so I shard when write volume or data size genuinely exceeds one vertical node.
