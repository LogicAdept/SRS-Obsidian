<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is index_granularity_bytes in ClickHouse

> [!abstract] Short answer
> index_granularity_bytes bounds a granule's size in bytes under adaptive granularity: instead of always 8192 rows, a granule is closed when it reaches this many bytes (default about 10 MB), so tables with wide rows get smaller granules and tables with narrow rows get full 8192-row granules. The goal is keeping the skip-unit small enough that index marks stay selective.

## Adaptive versus fixed granularity

The MergeTree docs define the two knobs together: index_granularity is the maximum row count of a granule (default 8192), and index_granularity_bytes bounds the byte size, with the number of rows in a granule ranging within [1, index_granularity] depending on row size; a single row larger than the byte setting forms its own granule. Adaptive sizing is the default behavior for modern MergeTree tables, with 0 disabling it. The rationale is read-amplification control: a granule is the atomic read unit, so a table of multi-kilobyte event rows with fixed 8192-row granules would read tens of megabytes even for a single granule touch — adaptive sizing closes granules earlier so that pruning by primary key or skip indexes actually reduces bytes read.

```sql
CREATE TABLE wide_events
(
    ts    DateTime,
    payload String,      -- several KB per row
    user_id UInt64
) ENGINE = MergeTree
ORDER BY (user_id, ts)
SETTINGS index_granularity = 8192, index_granularity_bytes = 10485760;
```

**Listing 1.** With 10 MB adaptive sizing, wide rows close granules well before 8192 of them accumulate.

## Why it matters for the whole index stack

Every upper structure is expressed in granules: the sparse primary index holds one mark per granule (per [[What is a sparse primary index in ClickHouse]]), skip indexes are declared with GRANULARITY in granules (per [[What data skipping indexes exist in ClickHouse]]), and EXPLAIN reports granules selected versus total, per [[How do you verify a ClickHouse index is used]]. If granules balloon in bytes, each mark covers too much data and every index's exclusion power drops proportionally; if granules shrink too far, mark count and per-granule overhead grow and scans lose batching efficiency. The byte knob is how you keep that balance when row width is extreme or uneven — the same underlying concern as the row-count default in [[What is a granule in ClickHouse]].

> [!warning] "Smaller granules are always more selective" ignores overhead
> Shrinking granules multiplies marks, per-granule metadata, and the number of files reads touch, which can hurt throughput more than the extra precision helps — the docs' granule-range note (up to index_granularity * 2 extra rows per block read) exists because some overshoot is cheaper than tiny granules. The other myth: that this setting alone fixes bad keys. If the WHERE does not match the ORDER BY, no granularity setting saves you.

> [!tip] Interview answer
> index_granularity_bytes is the adaptive side of granule sizing: a granule closes at about 10 MB by default or 8192 rows, whichever comes first, so wide-row tables get smaller granules and stay prunable. Since granules are the atomic read unit — for the sparse index marks, skip indexes, and EXPLAIN counters — this setting keeps the skip unit small on wide rows. Zero disables adaptivity and restores fixed row-count granules.
