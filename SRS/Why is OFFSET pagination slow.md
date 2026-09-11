<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `OFFSET n` makes the engine *produce and discard* n rows before returning the page: page 1000 with size 20 walks 20,000 rows. The work grows linearly with page depth even with perfect indexes — `LIMIT 20 OFFSET 100000` plans as a scan of 100,020 index entries. It is fine for shallow, fixed pages (top-N, admin views); it is the wrong tool for deep, unbounded feeds — keyset pagination replaces it ([[What is keyset pagination]]).

The verified demo shows both the correctness and the shape: `LIMIT 2 OFFSET 3` returns exactly rows 4 and 5 (the walk-and-skip semantics), and the plan reads `SCAN events USING COVERING INDEX idx_events_at` — the index supplies order cheaply, but the *count* of visited entries is offset plus limit; the engine cannot fast-forward a B-tree to "entry 100,003" because B-tree ranges are value-bounded, not position-bounded ([[What is keyset pagination]]). On PostgreSQL the same law holds with Seq Scan or Index Scan nodes: OFFSET is applied at the top of the plan after the rows flow; EXPLAIN ANALYZE makes the discarded-row count visible. The honest scope of the criticism: OFFSET at page depths users actually reach (1-10) costs almost nothing extra; the pathology is *unbounded* depth — infinite feeds, API crawlers, "load more" buttons that keep incrementing — where cost grows without bound and every page re-reads all previous data. The migration decision is product-shaped too: OFFSET supports jump-to-page navigation and stable page numbers under inserts only weakly (rows shift between pages — the "phantom row on page 3" bug); keyset gives next/prev with rock-stable boundaries ([[How does LIMIT interact with ORDER BY and indexes]], [[What harmful SQL patterns or pitfalls do you know]]).

```sql
SELECT id FROM events ORDER BY at, id LIMIT 2 OFFSET 3;
-- 4
-- 5
-- (walk 3 rows, discard them, return the next 2)
EXPLAIN QUERY PLAN
SELECT id FROM events ORDER BY at, id LIMIT 2 OFFSET 3;
-- QUERY PLAN
-- `--SCAN events USING COVERING INDEX idx_events_at
-- (bounded index walk -- but it visits offset+limit entries:
--  at OFFSET 100000 the walk is 100020 entries, same plan shape)
```

**Listing 1.** Verified on SQLite 3.53.1. Correct results with a growing hidden cost: the plan never says "OFFSET", it just visits offset+limit entries — which is why deep pages degrade without any plan change to point at.

```d2
direction: right
d1: "page 1
walk 20" {width: 130; height: 70}
d2: "page 50
walk 1000" {width: 140; height: 70}
d3: "page 5000
walk 100000" {width: 160; height: 70}
k: "keyset page k
walk 20, always" {width: 170; height: 70}
d1 -> d2 -> d3
d1 -> k
```

**Fig. 1.** OFFSET's cost is the distance walked: every page re-traverses everything before it. The keyset alternative walks one page's worth, always.

> [!warning] OFFSET pages also shift under concurrent inserts
> A row inserted before your offset pushes every subsequent row down a page — the classic "I saw this row already" / "this row vanished" bug in feeds. Keyset boundaries are values, not positions, so inserts before the cursor do not move the pages already seen ([[What is keyset pagination]]).

> [!tip] Interview answer
> OFFSET makes the engine produce and discard the skipped rows: LIMIT 20 OFFSET 100000 visits 100,020 index entries — linear cost in page depth, even with a perfect index, because B-tree ranges are value-bounded, not position-bounded. My demo shows the walk-and-skip semantics and the plan that hides the cost. I keep OFFSET for shallow fixed pages — top-N lists, admin tables — and switch to keyset seeks for deep unbounded feeds, which also fixes the page-shifting bug under concurrent inserts.
