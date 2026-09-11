<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is a sparse primary index in ClickHouse

> [!abstract] Short answer
> ClickHouse's primary index is a sparse index: one entry — a mark with the primary key value of the first row — per granule of 8192 rows, instead of one entry per row. It stays small enough to live in memory, binary search or exclusion search over the marks narrows reads to candidate granules, and the matching granules' columns are then scanned.

## What sparse means and why it exists

The sparse-primary-index guide contrasts the designs directly: an RDBMS primary index holds one entry per row (8.87 million entries in its example), which supports row-level lookups but costs memory and insert overhead; ClickHouse instead stores one index entry per group of rows — a granule — a technique it calls a sparse index. Each data part has its own primary index, and parts carry their marks with them through merges. A query filtering on a prefix of the key searches the marks (the guide and EXPLAIN describe generic exclusion search), selects candidate granule ranges, and reads those ranges' columns; the index never points to individual rows.

```d2
direction: down
rows: "Sorted rows in a part\n8.87M rows" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
gr: "Granules of 8192 rows\n~1083 granules" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
idx: "Sparse primary index\none mark per granule" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
rows -> gr
gr -> idx: "1 mark each"```

**Fig. 1.** The index is two orders of magnitude smaller than a per-row index because it addresses granules, not rows.

## What it is not, and what compensates

It is not unique, not per-row, and not an OLTP lookup structure: multiple rows share key values freely, and there is no mechanism to fetch a single row by key without reading its granule. Queries that filter on non-key columns get nothing from the primary index — their acceleration comes from data-skipping indexes that also operate on granules, per [[What data skipping indexes exist in ClickHouse]], with the primary-key-versus-skip division explained by [[What is the difference between PRIMARY KEY and ORDER BY in ClickHouse]]. The design's payoff is visible in the guide's own numbers: pruning turns an 8.87-million-row read into a few granule ranges. Verification is mechanical — EXPLAIN indexes = 1 reports granules selected versus total per index, per [[How do you verify a ClickHouse index is used]], and key choice is the design lever in [[How do you choose ORDER BY in ClickHouse]].

> [!warning] "Sparse index" does not mean "sometimes missing" or "weak index"
> The word sparse refers to one entry per group of rows, not to gaps in coverage or to an optional index. The confusion also runs the other way: calling it "just like a clustered B-tree" ignores that leaves hold marks, not rows, and that seeks end at granule boundaries. ClickHouse is unapologetic about this: the design targets analytic scans at petabyte scale, and point-lookup workloads are simply not its contract.

> [!tip] Interview answer
> A sparse primary index stores one mark per 8192-row granule instead of one entry per row, so it is tiny and memory-resident. A query on a key prefix searches the marks, selects candidate granule ranges, and ClickHouse scans those granules' columns — there is no row-level seek. It is the foundation every other index works on: skip indexes drop further granules within the same model.
