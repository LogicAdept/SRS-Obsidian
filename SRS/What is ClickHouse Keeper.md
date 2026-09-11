<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Replication #SRS

# What is ClickHouse Keeper?

> [!abstract] Short answer
> ClickHouse Keeper (`clickhouse-keeper`) is the coordination system for replication and distributed DDL — a ZooKeeper replacement written in C++ on top of the Raft algorithm (eBay/NuRaft). It keeps the ZooKeeper client protocol and ACL model, but adds linearizable writes, optional linearizable reads, and snapshot-based recovery without a JVM.

## What it coordinates

For [[What is ReplicatedMergeTree]] tables, Keeper stores the part registry, merge and mutation queues, and leader election state; for distributed DDL (`ON CLUSTER`) it holds the query queue that every node applies. Data never flows through Keeper — only metadata — which is why smallKeeper clusters (3 or 5 nodes, majority quorum) coordinate petabyte clusters. It can run standalone (its own process, recommended for production) or embedded inside clickhouse-server, configured through the same XML model.

```sql
-- Keeper is the backend you see from SQL:
SELECT * FROM system.zookeeper WHERE path = '/clickhouse/tables/1/hits';
-- 4-letter-word diagnostics like ZooKeeper:
-- echo mntr | nc keeper-host 9181
```

**Listing 1.** The `system.zookeeper` table exposes the coordination tree; default client port is 9181, and ZooKeeper tools work unchanged.

## Guarantees and compatibility

The protocol is ZooKeeper-compatible — any standard ZooKeeper client works, and ACLs support the same `world`, `auth`, and `digest` schemes. The differences are under the hood: Raft gives linearizable writes and allows linearizable reads, whereas ZooKeeper's ZAB serves reads locally without linearizability (by default Keeper matches ZooKeeper: linearizable writes, non-linearizable reads). Storage is incompatible — snapshots and logs need the `clickhouse-keeper-converter` to migrate from ZooKeeper, and a mixed ZooKeeper/Keeper cluster is impossible. Internal tuning is snapshot-driven: a snapshot every `snapshot_distance` (100000) records, keeping 3 by default.

> [!warning] Keeper is a quorum service, not a per-node cache
> With 2 nodes, one failure stops the majority — run 3 or 5; with 3, one node may be down for writes. Placing it on busy disks hurts latency ("store logs on non-busy nodes" per the docs). And because replicated tables go read-only without it, treating Keeper as optional infrastructure is the classic outage: capacity-plan and monitor it like the database itself ([[What is ReplicatedMergeTree]]).

> [!tip] Interview answer
> ClickHouse Keeper is the C++/Raft replacement for ZooKeeper: it coordinates replication metadata, merges, mutations, and ON CLUSTER DDL, speaking the ZooKeeper client protocol with linearizable writes. It stores no table data, runs 3 or 5 nodes for quorum, and when it's down replicated tables turn read-only — that dependency is the interview point.
