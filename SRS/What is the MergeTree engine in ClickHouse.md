<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is the MergeTree engine in ClickHouse?

> [!abstract] Short answer
> MergeTree is the family of ClickHouse table engines built for large analytical tables: rows are appended into immutable sorted parts, parts are merged in the background, and every part carries a sparse primary index over the `ORDER BY` key. Derived engines change merge-time behavior — `ReplacingMergeTree` deduplicates, `SummingMergeTree` pre-aggregates, `ReplicatedMergeTree` adds replication.

## Core contract

Every insert creates a new [[What is a data part in ClickHouse]] whose rows are sorted by the sorting key expression. Each part divides rows into granules (default 8192 rows) and stores one index mark per granule in `primary.idx` — the [[What is a sparse primary index in ClickHouse]]. The engine requires `ORDER BY`; optional clauses add `PARTITION BY` ([[What is PARTITION BY in ClickHouse]]), `SAMPLE BY`, and per-column `TTL` ([[What is TTL in ClickHouse]]). Background merges continuously rewrite small parts into bigger ones and apply family-specific transformations — that is why the engine tolerates the huge write volume that [[Why is ClickHouse fast for analytical queries]] explains.

```sql
CREATE TABLE hits
(
    EventDate  Date,
    CounterID  UInt32,
    UserID     UInt64,
    URL        String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(EventDate)
ORDER BY (CounterID, EventDate, UserID)
SETTINGS index_granularity = 8192;
```

**Listing 1.** The canonical MergeTree DDL shape: monthly partitions, a composite sort key, default granule size.

## Family members

`ReplacingMergeTree(ver)` drops older duplicates of the same sort key during merges; `SummingMergeTree` and `AggregatingMergeTree` fold numeric sums and aggregation states; `CollapsingMergeTree` and `VersionedCollapsingMergeTree` cancel paired rows through a sign column; `GraphiteMergeTree` rolls up metrics. Replication is not a setting but an engine: [[What is ReplicatedMergeTree]] shares part metadata through ClickHouse Keeper. A [[What is a Distributed table in ClickHouse]] then fans inserts and queries across shards of these local tables.

```d2
MergeTree: "MergeTree\nsorted parts, sparse index" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
replacing: "ReplacingMergeTree\ndedup on merge" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
aggregating: "Summing / Aggregating\npre-aggregate on merge" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
collapsing: "Collapsing\n+/- row cancellation" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
replicated: "ReplicatedMergeTree\nKeeper-backed copies" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
MergeTree -> replacing
MergeTree -> aggregating
MergeTree -> collapsing
MergeTree -> replicated
```

**Fig. 1.** All MergeTree family members share the sorted-part storage model; each variant changes what background merges do to the rows.

> [!warning] MergeTree is not a B-tree index store
> The primary key here does not point at rows — it marks granule boundaries inside each part, so point lookups still read whole granules, and "deduplicated" rows coexist until a merge touches their parts. Interviewers probe exactly this: see [[What is FINAL in ClickHouse]] and [[What are mutations in ClickHouse]] for the delayed-writeback consequences.

> [!tip] Interview answer
> MergeTree is ClickHouse's core engine family: append-only sorted parts with an 8192-row granule and a sparse in-memory primary index, merged in the background. Variants specialize merge behavior — replacing, aggregating, collapsing — and ReplicatedMergeTree adds Keeper-coordinated replication. Everything else in ClickHouse, from TTL to projections, is built on this model.
