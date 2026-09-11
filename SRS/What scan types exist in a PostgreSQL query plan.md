<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes #SRS

# What scan types exist in a PostgreSQL query plan?

> [!abstract] Short answer
> The core four: Seq Scan reads the whole table; Index Scan uses an index and fetches matching rows from the heap; Index Only Scan answers from the index alone when the visibility map allows; Bitmap Heap Scan first builds a bitmap of matching pages via one or more Bitmap Index Scans, then visits those pages once. Plans also show joins, sorts and node types like TID Scan or CTE Scan, but the table-access story is those four.

## The four table-access nodes

```d2
seq: "Seq Scan\nread every page; cheap per page" {width: 320; height: 80}
is: "Index Scan\nB-tree descent, then heap per row" {width: 330; height: 80}
ios: "Index Only Scan\nindex alone, VM permits" {width: 300; height: 80}
bit: "Bitmap Index Scan -> Bitmap Heap Scan\npages first, then one pass" {width: 360; height: 80}
```

**Fig. 1.** Scan nodes in EXPLAIN output; the bitmap family decouples index order from heap access order.

- **Seq Scan** — wins for large fractions of the table or tiny tables; supports no ordering.
- **Index Scan** — random heap visits per row; wins for small selective results, and preserves index order (kills a sort node — [[How do you avoid a sort with an index]]).
- **Index Only Scan** — no heap visits on all-visible pages ([[What is an index-only scan in PostgreSQL]]).
- **Bitmap scans** — the index pass produces a bitmap of pages; multiple bitmaps combine with BitmapAnd/BitmapOr (how OR across indexed columns gets served — [[How does OR across columns affect index use]]). Loses row order; lossy mode (work_mem too small) marks whole pages and rechecks ([[What is a bitmap index scan in SQL plans]] has the deeper dive).

```sql
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100;
-- Bitmap Heap Scan ... -> Bitmap Index Scan (Index Cond: unique1 < 100)
EXPLAIN SELECT * FROM tenk1 WHERE unique1 = 42;
-- Index Scan ... Index Cond: unique1 = 42
```

**Listing 1.** Small range: bitmap beats index scan by avoiding random per-row heap trips; single row: plain index scan.

## How the planner decides

Cost model again: selectivity estimate decides whether reading everything (seq) beats descending the index plus random heap visits ([[How does the PostgreSQL query planner choose a plan]], [[Why might PostgreSQL choose a sequential scan instead of an index]]). The practical reading workflow is in [[How do you read EXPLAIN ANALYZE in PostgreSQL]].

> [!warning] Bitmap does not mean slow, and Index Scan does not mean fast
> A Bitmap Heap Scan over 0.1 percent of pages can beat an Index Scan's random reads; an Index Scan returning 500 thousand rows in index order can lose catastrophically to a Seq Scan with a sort. Node names are mechanics, not verdicts — compare actual time and buffers.

> [!tip] Interview answer
> Four access nodes: Seq Scan for full reads, Index Scan for selective ordered lookups with heap fetches, Index Only Scan when the index covers everything and pages are all-visible, and Bitmap scans that combine multiple indexes and turn random I/O into one ordered page pass. The planner picks by estimated selectivity and cost.
