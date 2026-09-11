<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# What is a granule in ClickHouse?

> [!abstract] Short answer
> A granule is the smallest indivisible chunk of rows ClickHouse reads from a data part — 8192 rows by default (`index_granularity`). The primary index stores one mark per granule, so queries prune and read data at granule granularity, never row granularity; that is what keeps the index tiny while scans stay fast.

## How granules relate to everything else

Rows in a part are sorted by the key, then sliced into granules; the first row of each granule gets a mark in the part's primary index file, and per-column mark files map each granule to byte ranges in the compressed column files. A `WHERE` on key columns descends the mark array by binary search ([[What is a sparse primary index in ClickHouse]]) and selects ranges of granules; filters on non-key columns then use skipping-index blocks built from groups of granules ([[What data skipping indexes exist in ClickHouse]]). Even EXPLAIN reports progress in granules — `Granules: 12 of 120` means 108 granules were pruned, not 108 rows.

```sql
CREATE TABLE t (d Date, k UInt32, v UInt64)
ENGINE = MergeTree ORDER BY k
SETTINGS index_granularity = 8192;      -- fixed 8192-row granules

CREATE TABLE t2 (d Date, k UInt32, v UInt64)
ENGINE = MergeTree ORDER BY k
SETTINGS index_granularity_bytes = 10485760;  -- adaptive: ~10 MiB granules
```

**Listing 1.** Fixed versus adaptive granularity: the same table, two ways to size granules — see [[What is index_granularity_bytes in ClickHouse]].

```d2
part: "Data part\nsorted by key" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
g1: "Granule 0\n8192 rows" {
  width: 190
  height: 70
  style.fill: "#e8f5e9"
}
g2: "Granule 1\n8192 rows" {
  width: 190
  height: 70
  style.fill: "#e8f5e9"
}
g3: "Granule 2\n8192 rows" {
  width: 190
  height: 70
  style.fill: "#e8f5e9"
}
idx: "primary.idx\n1 mark per granule" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
part -> g1
part -> g2
part -> g3
g1 -> idx: first row values
g2 -> idx
g3 -> idx
```

**Fig. 1.** One index mark per granule keeps `primary.idx` small enough for main memory; the granule itself is the unit a query either reads or skips.

> [!warning] A granule match is not a row match
> The index only says a granule *could* contain matching rows. ClickHouse then streams and filters every row of the selected granules, so a query returning one row can still decompress a full granule per column — the root of why point lookups are weak ([[When should you not use ClickHouse]]). Oversized granules from wide rows also inflate that overhead.

> [!tip] Interview answer
> A granule is ClickHouse's read unit — 8192 sorted rows by default, or ~10 MiB with adaptive granularity. The primary index keeps one mark per granule and skips whole granules by binary search, while per-column mark files map each granule into compressed files. Row-level access is deliberately not the design goal.
