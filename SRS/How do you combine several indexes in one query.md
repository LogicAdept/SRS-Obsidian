<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# How do you combine several indexes in one query

> [!abstract] Short answer
> Engines combine index scans mechanically when one index cannot serve the whole predicate: PostgreSQL builds per-index bitmaps and ANDs/ORs them before reading the heap; MySQL's Index Merge runs multiple range scans and unions or intersects their results. For a frequent fixed predicate pair, a composite index is usually better; combination is the flexible fallback for ad hoc shapes.

## PostgreSQL: bitmaps over the heap

PostgreSQL's combining-multiple-indexes page is the canonical description: a single index scan can only use clauses on its own columns joined with AND, so `WHERE x = 5 OR y = 6` cannot be served by either index alone. The system scans each relevant index into an in-memory bitmap of matching table rows, ANDs and ORs the bitmaps as the predicate requires, then visits the surviving rows in physical order — which is why the plan shows BitmapOr/BitmapAnd over Bitmap Index Scans feeding a Bitmap Heap Scan. The cost is that row order from the indexes is lost, so ORDER BY needs a sort, and each extra index scan adds time — the planner sometimes prefers one plain index scan even when more are available, per [[What is a bitmap index scan in SQL plans]].

```sql
EXPLAIN
SELECT * FROM events WHERE user_id = 42 OR source = 'mobile';
-- Bitmap Heap Scan
--   -> BitmapOr
--        -> Bitmap Index Scan on events_user_id_idx
--        -> Bitmap Index Scan on events_source_idx
```

**Listing 1.** Two single-column indexes cooperate through BitmapOr where neither alone could answer the OR.

## MySQL Index Merge and the design decision

MySQL's Index Merge accesses rows via multiple range scans on one table and merges them — intersection, union, or sort-union — visible in EXPLAIN as type index_merge with Using intersect(...) / Using union(...) / Using sort_union(...) in Extra; the manual notes its limits, including that it does not apply to full-text indexes. Design-wise, the choice between two single-column indexes plus combination versus one composite is workload-shaped: PostgreSQL's docs lay out the spectrum (two separate indexes relying on combination; a multicolumn index better for the pair but weaker for the trailing column alone; or all three) and add that B-tree skip scan in PG 18 can make a multicolumn index serve trailing-column searches when the leading column has few distinct values, per [[What is Index Skip Scan]]. The composite construction itself follows [[What is the leftmost prefix rule for composite indexes]], and the plan-level verification is the EXPLAIN discipline in [[How do you read EXPLAIN ANALYZE in PostgreSQL]].

> [!warning] "The DB will just use all needed indexes automatically" is half true and costed
> Combination exists but is not free: each component scan costs, bitmaps consume memory proportional to selectivity, and MySQL's sort-union exists precisely because plain union can blow up on large ranges. The planner compares combination against a single index plus filter or a seq scan — misestimates flip the choice, per [[How do stale statistics hurt a query plan]]. And no engine combines full-text indexes with B-tree merge; text predicates need their own structures.

> [!tip] Interview answer
> When one index cannot serve the predicate, engines combine scans: PostgreSQL builds bitmaps per index and ANDs or ORs them, then reads the heap in physical order; MySQL's Index Merge intersects or unions range scans. It is flexible for ad hoc predicates but loses ordering and adds per-index cost, so for a frequent fixed pair a composite index is usually the better answer, with skip scan as the modern middle ground.
