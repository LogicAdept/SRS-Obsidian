<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SystemDesign/Performance #SRS

# Why is ClickHouse fast for analytical queries?

> [!abstract] Short answer
> Speed comes from stacking several mechanisms: columnar storage reads only the columns a query touches; a sparse primary index plus [[What is a granule in ClickHouse]]-based pruning skips most data; secondary [[What data skipping indexes exist in ClickHouse]] and [[What are projections in ClickHouse]] prune further; compression shrinks I/O; and a vectorized execution layer processes batches with SIMD on all cores. Background merges move heavy work out of the query path entirely.

## Storage layer: read less data

Each `INSERT` creates a self-contained [[What is a data part in ClickHouse]] with one compressed column file per column, so a filter over two columns never touches the other 198. Within each part, rows are physically sorted by the primary key, which turns range filters into binary searches over a small in-memory index. Because writes are just part creation and all transformations — deduplication via [[What is ReplacingMergeTree]], pre-aggregation, TTL cleanup — happen during background merges, inserts stay lightweight and inserts do not synchronize with concurrent SELECTs.

## Query layer: parallel vectorized execution

Query operators pass intermediate data as batches, not single rows, which keeps CPU caches hot and lets the engine dispatch SIMD instruction variants chosen for the actual hardware. The plan is unfolded into multiple lanes, typically one per core, each processing a disjoint range of granules; if one node is not enough, the table is sharded and the same execution scales horizontally across the cluster. ClickHouse also maintains specialized versions of core algorithms — over 30 hash table variants used by joins and aggregations are selected per query and data distribution.

```d2
insert: "INSERT\nappend a new part" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
merges: "Background merges\nsort / dedup / TTL" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
prune: "Pruning\nprimary key + skip indexes\n+ projections" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
scan: "Read only needed columns\ncompressed (LZ4/ZSTD)" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
exec: "Vectorized engine\nSIMD, lanes per core" {
  width: 280
  height: 100
  style.fill: "#f3e5f5"
}

insert -> merges: offload work
merges -> prune
prune -> scan: only surviving granules
scan -> exec: batches of values
```

**Fig. 1.** The pipeline behind analytical speed: heavy work moves to merge time, queries prune first and read compressed columns, then execute vectorized in parallel.

> [!warning] "It reads everything fast" is the wrong mental model
> The design goal is to avoid reading data at all: the fastest read is the granule that was never touched. A ClickHouse table with a badly chosen sort key and no skip indexes can be slower than a tuned PostgreSQL install on the same hardware — speed is a property of the whole layout, not of columnar format alone. See [[How do you choose ORDER BY in ClickHouse]] and [[How do you debug a slow ClickHouse query]].

> [!tip] Interview answer
> ClickHouse is fast because it minimizes data movement end to end: columnar files read only relevant columns, the sorted-part layout plus sparse index and skip indexes let it skip most granules, compression cuts I/O, and vectorized parallel execution saturates all cores. Batch writes plus background merges keep the write path cheap. It is engineered for scans and aggregations, not point lookups.
