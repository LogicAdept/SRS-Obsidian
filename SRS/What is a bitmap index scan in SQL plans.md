<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/SQL #SRS

# What is a bitmap index scan in SQL plans

> [!abstract] Short answer
> A bitmap index scan builds an in-memory bitmap of table pages (or rows) that match an index condition, then reads the heap in physical order once. Its purpose is to cut random I/O and to combine several indexes with AND/OR of bitmaps before touching the table at all.

## The mechanism in PostgreSQL

PostgreSQL's plan shows Bitmap Index Scan, producing the bitmap, followed by Bitmap Heap Scan, visiting pages in ascending physical order. The docs' motivating case is that a single index scan can only use clauses joined with AND on its own columns; conditions like `WHERE a = 5 OR b = 6` cannot directly use one B-tree, but the system can scan one index per condition, OR (or AND) the per-index bitmaps together, and then visit the surviving table pages in physical order, which converts random row fetches into sequential-ish page reads. Because the bitmap discards row order from the indexes, any `ORDER BY` requirement needs an explicit sort step, and at high match rates the planner will instead pick a plain sequential scan, with the middle ground governed by selectivity as in [[What is selectivity and cardinality for indexes]].

```sql
EXPLAIN
SELECT * FROM events
WHERE user_id = 42 OR source = 'mobile';
-- Bitmap Heap Scan on events
--   Recheck Cond: ((user_id = 42) OR ((source)::text = 'mobile'::text))
--   ->  BitmapOr
--         ->  Bitmap Index Scan on events_user_id_idx
--         ->  Bitmap Index Scan on events_source_idx
```

**Listing 1.** `BitmapOr` runs two index scans, ORs their page bitmaps, and the heap scan then reads each qualifying page once.

## Related but distinct things

The bitmap here is a plan technique over ordinary B-tree indexes; it is not Oracle's bitmap index storage type, where each key value stores a bitmap over rows and is aimed at low-cardinality analytical columns. The loss of row order also matters for pagination: an ordered retrieval cannot come from a Bitmap Heap Scan, so top-N work relies on a plain ordered index scan as in [[How does LIMIT interact with ORDER BY and indexes]]. Planner statistics decide between plain index scan, bitmap scan, and seq scan, and skewed estimates push the planner to the wrong one, the failure mode in [[How do stale statistics hurt a query plan]].

> [!warning] "Bitmap scan = bitmap index" is the classic conflation
> In an interview, saying "bitmap index scan means bitmap indexes exist in PostgreSQL" is wrong: PostgreSQL has no stored bitmap index type; the bitmap is built at runtime from B-tree (or GiST/GIN/BRIN) scans. Oracle and SQL Server are where stored bitmap structures live, and they solve a different problem: indexing low-cardinality columns rather than combining existing index scans.

> [!tip] Interview answer
> A bitmap index scan converts each index's matching rows into a page bitmap; the planner ANDs or ORs bitmaps from several indexes, then a Bitmap Heap Scan reads surviving pages in physical order, cutting random I/O. It is PostgreSQL's way to use multiple indexes for AND/OR predicates, but it loses row ordering and stops paying off when the bitmap covers too much of the table, where a sequential scan wins.
