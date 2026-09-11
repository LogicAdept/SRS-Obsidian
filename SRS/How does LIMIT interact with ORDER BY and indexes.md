<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/SQL #SRS

# How does LIMIT interact with ORDER BY and indexes

> [!abstract] Short answer
> When the ORDER BY matches an index and the filter allows a contiguous scan, the engine reads rows in order and stops after LIMIT rows — a top-N that costs N rows regardless of table size. When no index provides the order, the engine must sort all qualifying rows first (or keep a bounded top-N heap) and only then apply LIMIT.

## The cheap path: ordered scan with early termination

If the index key matches ORDER BY, walking the leaves yields sorted rows, and the LIMIT simply ends the walk. With an equality filter on a leading prefix, rows sit in one contiguous run and the stop happens inside it; this is the mechanism that makes "latest 10 items per user" queries constant-time, and it is the same property keyset pagination builds on in [[What is keyset pagination]]. MySQL's ORDER BY and LIMIT optimization docs describe the same design: if the ORDER BY can be resolved by an index, MySQL avoids a filesort and stops once the LIMIT rows are found, including for small OFFSET-free pages.

```sql
CREATE INDEX idx_feed ON posts (author_id, created_at DESC);
SELECT * FROM posts
WHERE author_id = 42
ORDER BY created_at DESC
LIMIT 10;
-- reads 10 index+heap rows, not "all posts, sorted"
```

**Listing 1.** Top-N rides the composite: seek the run, walk ten leaves, stop.

## The expensive path and the middle ground

Without an ordering index, the planner sorts all rows matching WHERE before applying LIMIT; PostgreSQL describes keeping only the top LIMIT rows in a bounded sort when N is small, which is still O(M log N) over M qualifying rows rather than O(N). A bitmap heap scan loses row order entirely and needs an explicit sort, per the combining-multiple-indexes page, so it cannot terminate early. Big OFFSETs are the classic abuse: OFFSET 100000 still reads and discards 100000 ordered rows, which is why keyset predicates replace deep offsets in hot paths. Verify the shape in the plan: an Index Scan with LIMIT directly above it is the good case, per [[How do you read EXPLAIN ANALYZE in PostgreSQL]].

> [!warning] "LIMIT makes it fast" without an ordering index
> LIMIT does not bound the work when the plan must sort or scan first: sorting 10 million rows to return 10 is not saved by the LIMIT — at best the sort is a bounded heap. Also, LIMIT interacts badly with ambiguous ORDER BY: equal keys can return different rows page to page unless a tiebreaker column makes the order deterministic, which is exactly the tiebreaker keyset pagination adds.

> [!tip] Interview answer
> LIMIT with an index-matched ORDER BY is a top-N stop: the engine walks the ordered index, optionally within an equality prefix, and quits after N rows. Without a matching index, the database must sort or scan everything qualifying before LIMIT applies. Deep OFFSET pages re-read everything skipped, so hot pagination uses the next-page predicate instead of OFFSET.
