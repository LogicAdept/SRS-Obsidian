<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# How does OR across columns affect index use

> [!abstract] Short answer
> A single index scan cannot serve predicates ORed across different columns, so the engine must either combine several index scans (bitmap OR in PostgreSQL, Index Merge union in MySQL) or scan the table. The combination is costed and loses row order; one non-sargable branch drags the whole predicate toward a scan.

## Why OR breaks the single-index path

PostgreSQL's docs state the boundary precisely: a single index scan can only use clauses that reference the index's own columns joined with AND — `WHERE a = 5 AND b = 6` fits an (a, b) index, `WHERE a = 5 OR b = 6` does not, because no contiguous range of one index contains the answer. The remedy at plan time is combination: scan each index into a bitmap of matching rows, OR the bitmaps, and read the surviving rows in physical order. MySQL's equivalent is Index Merge with Using union(...) in EXPLAIN. Two consequences follow: row order from the indexes is gone (ORDER BY needs a sort), and every branch must still be indexable — a function on a column or a leading wildcard in one OR branch makes that branch a scan-shaped cost, per [[Why does a function on a column prevent index use]] and [[Why does LIKE with a leading wildcard not use a B-tree index]].

```sql
EXPLAIN SELECT * FROM events WHERE user_id = 42 OR source = 'mobile';
-- BitmapOr: two Bitmap Index Scans -> Bitmap Heap Scan (no ordering)

SELECT * FROM events WHERE user_id = 42
UNION
SELECT * FROM events WHERE source = 'mobile';
```

**Listing 1.** The engine's OR path and the rewrite that restores per-branch seeks.

## Design responses

If the OR pair is a frequent fixed shape, options in order of preference: a composite index when the predicates can be restructured as AND; per-column indexes plus bitmap combination accepted; or a query rewrite as UNION/UNION ALL of indexed branches, which turns each branch into a cheap seek at the price of dedup and pagination complexity, per [[How do you optimize a search query over several columns]]. For one search term across many columns, a materialized searchable field with its own FTS/trigram index removes the OR entirely. The planner's choice among these is cost-driven and estimate-sensitive, so stale statistics flip OR plans unpredictably, per [[How do stale statistics hurt a query plan]]; the combination machinery itself is detailed in [[How do you combine several indexes in one query]].

> [!warning] "OR disables indexes" and "OR is fine, the DB handles it" — both need the mechanism
> The absolute claim fails because BitmapOr/Index Merge exist; the dismissive claim fails because combination is expensive, unordered, and fragile against non-sargable branches. The precise statement: OR across columns forfeits single-index seeks and trades them for costed multi-index combination, whose quality depends on every branch being indexable and estimates being honest.

> [!tip] Interview answer
> OR across different columns cannot be served by one index scan, so the engine combines per-column index scans into a bitmap OR or Index Merge union, losing row order and paying per-index costs — or scans the table if estimates or non-sargable branches make combination unattractive. For hot shapes I restructure: composite where possible, UNION ALL of indexed seeks otherwise, or a materialized search field for single-term multi-column search.
