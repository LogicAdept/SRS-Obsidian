<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Partitioning #SRS

# What is PARTITION BY in ClickHouse?

> [!abstract] Short answer
> `PARTITION BY` splits a MergeTree table's parts into logical units by an expression — usually a time bucket like `toYYYYMM(date)`. It is a data-management tool: it enables fast whole-partition drops, TTL at partition level, and separate merge tracks; the docs are explicit that partitioning is *not* primarily a query-optimization technique and should not be granular.

## What it changes

Each insert produces at least one part *per distinct partition value* in the block, and parts from different partitions never merge with each other. For every part, ClickHouse automatically stores MinMax files on the partition-key columns, so a `WHERE` on the partition key can prune whole partitions before granule-level work — that is the query-side benefit, useful mainly when the partition key is *not* already leading the sort key. The management side is where partitions pay: `ALTER TABLE ... DROP PARTITION '202608'` ([[How do you drop old data quickly in ClickHouse]]), per-partition TTL rules ([[What is TTL in ClickHouse]]), and partition-level `ATTACH`/`DETACH` for archiving.

Operationally, the partition id is stamped into every part name and visible in `system.parts` grouped by `partition`; part-count limits ([[What causes Too many parts in ClickHouse]]) are evaluated per partition, which is exactly why high-cardinality keys are dangerous. The MinMax files are automatic — no index declaration needed — and pruning by them shows up as the first stage of `EXPLAIN indexes = 1`, before the primary-key analysis.

```sql
CREATE TABLE hits
(
    EventDate Date,
    CounterID UInt32,
    UserID    UInt64
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(EventDate)      -- one partition per month
ORDER BY (CounterID, EventDate, UserID);

ALTER TABLE hits DROP PARTITION '202501';   -- instant, metadata-level
```

**Listing 1.** Monthly partitioning with the recommended `toYYYYMM` expression, and the instant-drop payoff.

> [!warning] Never partition by client id or another high-cardinality column
> Because parts never merge across partitions, N partitions multiply the parts that must be tracked and merged independently — a high-cardinality key explodes part counts and triggers the "Too many parts" error ([[Why do too many partitions hurt ClickHouse]]). The MergeTree reference states the rule directly: partition by no finer than month, don't partition by client identifiers, and put the client id first in ORDER BY instead. Cardinality guidance is "under 1000..10000" partitions.

> [!tip] Interview answer
> PARTITION BY groups parts into logical units — monthly time buckets by convention — enabling instant partition drops, TTL, and coarse MinMax pruning. It's a data-lifecycle tool, not the main query accelerator (that's the sort key), and over-partitioning is actively harmful because merges can't cross partition boundaries. Choose months, not user ids.
