<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# What is a sparse primary index in ClickHouse?

> [!abstract] Short answer
> The primary index of a MergeTree part is an uncompressed flat array (`primary.idx`) with one entry — a mark — per granule, not per row. It is called sparse because it indexes every 8192th row; that keeps it small enough to stay permanently in main memory, while binary search over the marks selects the granules a query must read.

## Why sparse works here

Rows inside a part are physically ordered by the key, so "find rows with key in [a, b]" reduces to "find the granule range whose marks straddle a and b". A B-tree would need per-row nodes and pointers to every row; the sparse index instead accepts reading up to one granule of extra rows and lets the engine filter afterward. In the official sparse-index walkthrough, a 8.87-million-row table produces 1083 marks in about 97 KB — the index is memory-resident, and it exists per [[What is a data part in ClickHouse]] (merged together on part merge, just like the rows).

```sql
SELECT name, primary_key_size, marks
FROM system.parts_columns  -- per-part statistics live in system.parts too
WHERE table = 'uk_price_paid' AND active;
-- primary.idx: one mark per granule, granule = 8192 rows
```

**Listing 1.** Index size scales with granule count, not row count: rows/8192 marks per part.

## Lookup mechanics

For `WHERE UserID = 7432` on a `(UserID, URL)` key, ClickHouse binary-searches the mark array for the first and last granules that can contain the value, reads the corresponding mark files, and streams those granules' column files — no pointers are chased, no rows are addressed individually. A key column appearing with an equality filter is the ideal case; filters on expressions of key columns can still use the index when the expression is monotonic. What the primary index cannot do is skip granules for non-key predicates — that job belongs to [[What data skipping indexes exist in ClickHouse]] or [[What are projections in ClickHouse]].

```d2
marks: "primary.idx\nmark 0 | mark 1 | ... | mark N\nkey values of granule starts" {
  width: 380
  height: 100
  style.fill: "#e3f2fd"
}
bs: "Binary search over marks\n -> granule range [i, j]" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
read: "Stream granules i..j\nvia column mark files" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
filter: "Evaluate WHERE on rows\ninside those granules" {
  width: 300
  height: 80
  style.fill: "#f3e5f5"
}
marks -> bs
bs -> read
read -> filter
```

**Fig. 1.** The sparse index narrows the search to a granule range; row-level filtering happens after the granules are read.

> [!warning] Sparse does not mean "partial coverage"
> Every granule is indexed — "sparse" refers to one entry per *group* of rows, not to indexing some rows and not others. The related myth is that the index returns rows: it returns granule positions, so an equality filter still reads and scans the granule it selects. See [[What is a granule in ClickHouse]] for the read-unit consequences.

> [!tip] Interview answer
> A MergeTree primary index is a memory-resident flat array with one mark per 8192-row granule, built per part over the sorted key. Queries binary-search the marks to pick candidate granules, then stream and filter those granules. Sparse means group-per-entry rather than row-per-entry — that is how the index stays tiny at petabyte scale.
