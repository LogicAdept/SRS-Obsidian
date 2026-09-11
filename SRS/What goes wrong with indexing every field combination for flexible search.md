<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SystemDesign/Tradeoffs #SRS

# What goes wrong with indexing every field combination for flexible search

> [!abstract] Short answer
> A flexible search endpoint over N fields implies up to 2^N index combinations; creating them all multiplies write amplification on every DML, bloats storage and cache pressure, confuses the planner with overlapping statistics, and most of the indexes end up unused. The workable designs are few purpose-built composites for measured shapes plus combination or skip scan for the tail, or a dedicated search structure.

## The combinatorics and the write bill

Optional filters compose: five searchable fields produce tens of meaningful orderings, and each composite index is a full structure the engine must update for every INSERT, DELETE, and UPDATE touching any indexed column. MySQL's optimization manual advises the opposite shape explicitly: do not create a separate secondary index for each column; prefer a small number of concatenated indexes for the actual query combinations, because each query can use one index and every index taxes writes. Storage and cache follow: every index is key-plus-locator copies of the data, so the buffer pool serves more index pages and fewer data pages, and bulk loads slow proportionally — the general cost accounting in [[When are database indexes a bad idea]].

```d2
direction: right
q: "5 searchable fields" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
idx: "all combinations\n10+ composite indexes" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
few: "measured shapes\n2-3 composites + tail via combination" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
q -> idx: "scattergun"
q -> few: "measured"```

**Fig. 1.** The scattergun path buys 2^N maintenance for shapes nobody queries; the measured path covers hot shapes and lets the tail ride combination.

## What actually breaks at runtime

Beyond writes: the planner chooses among many overlapping indexes, and stale or thin statistics make it pick awkward ones — the estimate fragility in [[How do stale statistics hurt a query plan]]; unused indexes accumulate (audit them per [[How do you find unused indexes in PostgreSQL]]) and even hide plan regressions when an overlapping index silently wins. The flexible-search tail is better served structurally: bitmap combination of a few single-column indexes for ad hoc AND shapes, per [[How do you combine several indexes in one query]]; skip scan when a composite's leading column has few distinct values, per [[What is Index Skip Scan]]; and for genuinely free-form text, a materialized searchable field or an external search engine, per [[How do you optimize a search query over several columns]] and [[When should you use Elasticsearch instead of SQL search]]. The per-endpoint discipline that prevents the trap in the first place is in [[How do you design indexes for a search API]].

> [!warning] "Storage is cheap" does not pay the write bill
> The storage-is-cheap argument ignores that every index is recomputed per DML row, not just stored: insert throughput, replication lag, and vacuum/maintenance pressure all scale with index count. The second trap: index bloat is invisible until the buffer pool starts thrashing or a bulk migration times out. The failure is architectural, not a tuning detail — the fix is the workflow in [[How do you decide which database indexes to create]].

> [!tip] Interview answer
> Indexing every combination is 2^N structures, each taxing every write, bloating storage, and cluttering the planner — and most end up unused. I index the measured hot shapes with few well-ordered composites, cover the ad hoc tail with bitmap combination or skip scan, and move genuinely free-form search to a searchable field or an external engine. The audit loop — unused indexes get dropped — is what keeps the set honest.
