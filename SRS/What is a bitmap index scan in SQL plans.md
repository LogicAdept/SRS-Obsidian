<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A **bitmap index scan** (PostgreSQL) combines the cheap seeking of indexes with the sequential read pattern of a table scan: each qualifying index produces a **bitmap of row locations**, bitmaps are ANDed/ORed for combined predicates, then the heap is visited **in physical order**, one row at a time with a recheck of the condition. EXPLAIN shows it as `Bitmap Index Scan` feeding a `Bitmap Heap Scan`.

PostgreSQL's documentation describes the mechanism exactly: the system scans each needed index, "prepares a bitmap in memory giving the locations of table rows" matching each index's conditions, ANDs and ORs the bitmaps, then visits rows in physical order. Two payoffs: combined predicates (`WHERE a = 1 OR b = 2`) each use their own index and merge cheaply, and heap access becomes sequential rather than random, which matters enormously on spinning disks and still wins on SSDs by prefetch locality. Two costs: the bitmap loses index ordering (an explicit sort replaces it), and on huge match sets the bitmap degrades from exact to **lossy** (one bit per page plus a recheck of every row on the page — visible in EXPLAIN as `Heap Blocks: exact=... lossy=...`). The anti-pattern it prevents: a plain index scan on a million matching rows does a million random heap hops; the bitmap visits pages in order. SQLite has no bitmap heap scan; its optimizer solves the same OR problem with `MULTI-INDEX OR` — it runs each index, deduplicates rowids, and merges (verified in the demo) ([[How does OR across columns affect index use]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE INDEX idx_city ON customers(city);
CREATE INDEX idx_name ON customers(name);

EXPLAIN QUERY PLAN
SELECT * FROM customers WHERE city = 'Berlin' OR name = 'Alice';
-- QUERY PLAN
-- |--MULTI-INDEX OR
-- |  |--INDEX 1
-- |  |  `--SEARCH customers USING INDEX idx_city (city=?)
-- |  `--INDEX 2
-- |     `--SEARCH customers USING INDEX idx_name (name=?)
-- (PostgreSQL plans this as Bitmap Index Scan x2 -> BitmapOr -> Bitmap Heap Scan)
```

**Listing 1.** Verified on SQLite 3.53.1: the MULTI-INDEX OR plan — each predicate drives its own index, results merged. PostgreSQL's bitmap machinery is the documented equivalent: per-index bitmaps combined with BitmapOr, then heap rows visited in physical order with a recheck.

```d2
direction: right
i1: "index on city
row locations" {width: 180; height: 70}
i2: "index on name
row locations" {width: 180; height: 70}
bm: "bitmaps AND / OR
one bit per row or page" {width: 230; height: 80}
h: "heap visited in
physical order + recheck" {width: 240; height: 80}
i1 -> bm
i2 -> bm
bm -> h
```

**Fig. 1.** Bitmap scanning converts index output from "rows" to "a map of where rows live", letting several maps merge before any table access happens.

> [!warning] Bitmaps buy locality at the price of order and precision
> The heap pass is physical, so an ORDER BY needs a separate sort, and large match sets turn lossy — every page's rows rechecked. If the query filters down to a handful of rows, a plain index scan is cheaper; bitmaps shine when *many* rows match but must be fetched in heap order ([[What is Index Cond versus Filter in EXPLAIN]]).

> [!tip] Interview answer
> A bitmap scan is PostgreSQL combining index cheapness with sequential heap access: each index builds a bitmap of matching row locations, bitmaps get ANDed or ORed, then the heap is read in physical order with a recheck. It wins for broad matches or multi-index OR conditions, avoids a million random heap hops — but loses index ordering, forcing a sort, and can degrade to lossy pages on very large sets. SQLite solves the same OR case with MULTI-INDEX OR plans; the trade-offs are the same.
