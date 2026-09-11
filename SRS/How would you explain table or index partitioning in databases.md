<!--
reps: 0
priority: 0
-->
#Databases/Partitioning #Databases/Indexes #SRS

# How would you explain table or index partitioning in databases

> [!abstract] Short answer
> Partitioning splits one logical table into physical pieces by a key: within a single server (declarative partitioning in PostgreSQL, PARTITION BY in ClickHouse) as opposed to sharding, which spreads pieces across servers. Each partition carries its own indexes, and queries with the partition key in the predicate prune whole partitions; without that key, partitioning mostly adds overhead.

## Table partitioning: the mechanism

PostgreSQL's declarative partitioning divides a table into child tables by a key expression — RANGE (by time), LIST (by category), HASH (by key hash) — while queries still address the one logical table; the planner eliminates partitions whose bounds cannot match the predicate. The point is management and pruning: dropping an old month is a metadata operation instead of a DELETE, and time-scoped queries scan one partition instead of the whole table. Indexes are built per partition (or on the parent as partitioned indexes, materialized on children). ClickHouse's PARTITION BY does the same job for MergeTree parts — and the docs add the caveat interviewers love: partitioning does not speed up queries in contrast to the ORDER BY expression, over-partitioning hurts, and month granularity is the typical ceiling, per [[How do you choose ORDER BY in ClickHouse]].

```sql
-- PostgreSQL: range partitioning by month
CREATE TABLE events (
    id    BIGINT,
    ts    TIMESTAMPTZ,
    kind  TEXT
) PARTITION BY RANGE (ts);

CREATE TABLE events_2026_08 PARTITION OF events
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE INDEX ON events_2026_08 (kind, ts);
```

**Listing 1.** One logical table, monthly children, per-partition index; old months leave by DETACH/DROP, not by DELETE.

## Index partitioning and the sharding boundary

Index partitioning means each table partition has its own index structures: prunes stay local, maintenance (REINDEX, rebuilds) hits one piece, and global uniqueness needs care (a unique constraint must include the partition key in PostgreSQL, precisely because uniqueness cannot be enforced across partitions by local indexes). The distinction from sharding is deployment: partitioning keeps pieces on one server or one logical cluster; sharding distributes them across servers with a routing layer — the trade-offs live in distributed-systems territory, not index territory. Local indexes per shard per partition remain the same principle at larger scale, and the ClickHouse variant of local pruning (granules, not partitions, doing the fine work) is in [[What is a granule in ClickHouse]] and [[What is a sparse primary index in ClickHouse]].

> [!warning] "Partitioning makes queries faster" — only with the key in the predicate
> Pruning happens when the WHERE constrains the partition key; queries that filter on other columns visit every partition and pay extra planning overhead. The second half-truth: partitioning is not sharding — no data leaves the server — and it is not a substitute for indexes: within a partition, the same B-tree/skip-index logic applies, per [[When is a full table scan cheaper than using an index]].

> [!tip] Interview answer
> Partitioning splits one table into physical pieces by a key — range by time is typical — with each piece holding its own indexes; the planner prunes partitions whose bounds cannot match the predicate, and lifecycle operations become metadata moves. It is local to a server, unlike sharding. It pays off when queries constrain the partition key; otherwise it is overhead, and in ClickHouse the ORDER BY key, not partitioning, is what speeds queries.
