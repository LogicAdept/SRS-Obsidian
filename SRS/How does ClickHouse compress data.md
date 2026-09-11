<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How does ClickHouse compress data?

> [!abstract] Short answer
> Each column is compressed independently in blocks: LZ4 by default, or ZSTD when you need a better ratio. On top of the algorithm you can stack transformation codecs, and dictionary-encoded columns ([[What is LowCardinality in ClickHouse]]) compress on top of that — `Delta`/`DoubleDelta` for monotonic sequences, `Gorilla` for floating-point gauges, `T64` for scattered integers, `GCD` for coarse steps — declared per column with `CODEC(...)`. Column locality plus sorted rows is what makes the ratios (often 10x+) possible.

## Why columnar compresses so well

Values of one type and distribution sit next to each other, and sorting by the key places similar values adjacently — consecutive identical or slowly-changing values are exactly what LZ4 and ZSTD exploit. Compression is not only about disk: less I/O frequently means faster queries, since scans are throughput-bound — one of the compounding effects behind [[Why is ClickHouse fast for analytical queries]]. Decompression happens per granule via mark files, so reads touch only the compressed blocks they need.

```sql
CREATE TABLE metrics
(
    ts       DateTime CODEC(Delta, ZSTD(1)),      -- monotonic timestamps
    host     LowCardinality(String) CODEC(ZSTD(3)),
    cpu      Float32 CODEC(Gorilla),              -- gauge readings
    requests UInt64 CODEC(T64, ZSTD(1))           -- scattered integers
)
ENGINE = MergeTree ORDER BY (host, ts);
```

**Listing 1.** Typical codec choices: Delta over ZSTD for timestamps, Gorilla for gauges, T64 as a pre-pass for integers.

## Choosing codecs

The official guidance ranks the choices: ZSTD(1) as the safe default for common types; `Delta` when consecutive values have small deltas (timestamps, auto-increment ids) and `DoubleDelta` when even the deltas' deltas are small; `Gorilla` for gauge-like floats; `T64` for unknown integer patterns; LZ4 over ZSTD when both give similar ratios, because decompression is cheaper. Combining a transformation codec with ZSTD is normal — e.g. `CODEC(Delta, ZSTD(1))` — while stacking several generic algorithms rarely pays. The `compression-in-clickhouse` guide also shows how to measure per-column results in `system.parts` (`compressions`, `data_compressed_bytes`, `data_uncompressed_bytes`).

> [!warning] Heavy compression can slow queries
> ZSTD(19) may look tempting, but every granule read must decompress: extreme levels trade scan latency for disk savings, and the docs explicitly recommend against levels much above 3. For sorted-key columns, try better layout and codecs (`Delta`) before raising the ZSTD level — the sort order does more for compression than the level knob does.

> [!tip] Interview answer
> ClickHouse compresses each column separately in blocks — LZ4 by default, ZSTD for ratio — and gains because sorted columnar data is highly redundant. Per-column CODEC declarations add Delta, DoubleDelta, Gorilla, or T64 transformations before the generic algorithm, tuned per data shape: timestamps get Delta, gauges get Gorilla. Compression cuts both storage and scan I/O.
