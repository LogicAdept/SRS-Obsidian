<!--
reps: 0
priority: 0
-->
#Databases/Partitioning #SRS

# How do you design good database partitioning

> [!abstract] Short answer
> **Partition along the axis your queries filter on: pick a key and scheme (range, list, hash) so that almost every query prunes to one or few partitions, hot rows spread evenly, and old data drops by detaching a partition instead of a multi-hour DELETE.** A partition key that does not appear in WHERE clauses buys you nothing — the planner then scans every partition.

## The decisions, in order

**Scheme.** RANGE fits time and monotonically growing data (events by month, logs by day) and makes retention a DDL operation: `DETACH PARTITION`/`DROP PARTITION` removes a month instantly instead of deleting millions of rows (which bloats tables and replication streams — the same logic as [[How do you drop old data quickly in ClickHouse]]). LIST fits discrete categories (region, tenant) with stable membership. HASH spreads otherwise-unkeyed data evenly and kills hotspots, at the cost of losing range-pruning. **Key.** The dominant filter predicate: time for time-series, tenant_id for multi-tenant isolation (per [[How do you implement multi-tenancy in PostgreSQL]]), user_id for per-user data. Every important query should include the key; MySQL's partitioning guide is explicit that pruning only happens when the WHERE clause carries the partition function. **Granularity.** Enough partitions for retention and pruning, few enough that the planner can handle them — thousands of partitions inflate planning time and lock tables.

```sql
-- PostgreSQL: monthly range partitions on the dominant filter
CREATE TABLE events (
  id      bigint,
  payload text,
  at      timestamptz NOT NULL
) PARTITION BY RANGE (at);

CREATE TABLE events_2026_09 PARTITION OF events
  FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
-- retention: DETACH/DROP one partition, not DELETE 100M rows
```

**Listing 1.** Range partitioning by time: pruning turns "this week's events" into one-partition scans, and old months leave the table as a DDL no-op.

```d2
direction: right
q: "Query with\nWHERE at >= '2026-09-01'" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
pr: "Planner prunes\nother partitions out" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
p9: "events_2026_09\nscan only this" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
px: "events_2026_08, ...\nuntouched" {
  width: 230
  height: 80
  style.fill: "#ffebee"
}
q -> pr
pr -> p9
pr -> px: "skipped"
```

**Fig. 1.** The payoff of a well-chosen key: partition pruning excludes every partition the predicate cannot touch before any I/O happens.

> [!warning] The partition key must cover uniqueness — and partitions are not replicas or shards
> Every unique constraint on a range-partitioned PostgreSQL table must include the partition key, so "global unique id + monthly partition" needs the id composed with time or a different design; that surprises teams who expected a plain PK. And partitioning splits a table *within one node* — it does not add write capacity or failover the way sharding and replication do, per [[What is the difference between database replication and sharding]]. The classic failure is choosing the key by intuition ("id, it's unique!") instead of by query predicates: pruning never fires, every query opens all partitions, and planning time grows — worse than no partitioning.

The engine-level mechanics behind this: [[How does PostgreSQL declarative partitioning work]]; the columnar engine's take on ordering and pruning: [[How do you choose ORDER BY in ClickHouse]].

> [!tip] Interview answer
> I pick the scheme by data shape — range for time with DETACH-based retention, list for categories, hash against hotspots — and the key by the dominant query predicate so pruning actually fires. Granularity balances retention needs against planner overhead. I also check the constraint trap: unique keys must include the partition key, and partitioning scales manageability within a node — write scale still needs sharding.
