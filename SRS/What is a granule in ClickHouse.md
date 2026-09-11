<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is a granule in ClickHouse

> [!abstract] Short answer
> A granule is the smallest unit of data ClickHouse reads when selecting data: by default 8192 rows of one data part. The sparse primary index stores one mark per granule — the primary key value of its first row — so all index decisions skip whole granules, never individual rows.

## Where it sits in the storage model

Each MergeTree data part is logically divided into granules, each containing an integer number of rows bounded by index_granularity (default 8192) and, under adaptive sizing, by index_granularity_bytes. When data is inserted, the part is sorted by the primary key and ClickHouse builds an index file storing a mark for each granule: the primary key value of the granule's first row. The docs' canonical example is a (CounterID, Date) key where the index has one entry per 8192-row block. Reading a range of the key therefore means finding candidate granule marks, then reading those granules' column files — and the docs warn that reading a single key range can pull up to index_granularity * 2 extra rows per block, because granules are indivisible.

```sql
CREATE TABLE hits
(
    UserID UInt32,
    URL    String,
    EventTime DateTime
) ENGINE = MergeTree
ORDER BY (UserID, EventTime)
SETTINGS index_granularity = 8192;  -- the default
```

**Listing 1.** The table's data is processed in 8192-row units; the primary index holds one mark per such unit.

## Why the design beats per-row indexing at scale

A per-row B-tree index over 8.87 million rows (the sparse-primary-index guide's dataset) would need millions of entries, while one mark per granule yields roughly a thousand entries for the same data — small enough to stay memory-resident. The cost is granularity of reads: filtering by a non-key column cannot exclude rows, only granules, which is exactly what data-skipping indexes do on top of the granule model, per [[What data skipping indexes exist in ClickHouse]]. Granule size is therefore a tunable trade-off: adaptive byte-based sizing keeps wide rows from producing monster granules, per [[What is index_granularity_bytes in ClickHouse]]. Every skip index's GRANULARITY parameter is expressed in granules too, and EXPLAIN indexes = 1 counts eliminated granules, per [[How do you verify a ClickHouse index is used]].

> [!warning] "The primary index points to rows" — it never does
> The marks point to granules, and ClickHouse does not support row-level seeks at all. Saying the sparse index "finds the row" confuses it with a B-tree; the correct statement is that it narrows work to a set of granules whose column data is then scanned. Also, granule ≠ partition: partitions split data by key expression into separate parts, and the docs warn against over-partitioning, a different axis entirely.

> [!tip] Interview answer
> A granule is ClickHouse's read unit — 8192 rows by default per data part — and the sparse primary index stores one mark (the key of the first row) per granule, keeping the index tiny and memory-resident. Everything above it works in granules: the primary key prunes granule ranges, skip indexes drop granules, and EXPLAIN reports granules before and after each index. Rows are never addressed individually.
