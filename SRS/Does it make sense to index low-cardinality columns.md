<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# Does it make sense to index low-cardinality columns

> [!abstract] Short answer
> Alone, rarely: an index on a boolean or status column matches a large fraction of the table, so the planner prefers a scan. It earns its keep in a composite index where it partitions the key space, as a partial index excluding the dominant value, or as a bitmap index in engines built for low-cardinality analytics.

## Why a standalone index usually loses

The economics are selectivity-driven: a B-tree seek pays the tree walk plus one heap fetch per matching row, so when `status = 'active'` matches 40 percent of rows, a sequential scan's bulk reads win, per the crossover logic in [[When is a full table scan cheaper than using an index]]. MySQL's optimization manual says it outright: indexes on columns with only a few different values might not be helpful for any queries. That does not make the column unindexable — it makes the standalone single-column index on it usually pointless, which is a different claim, and the distinction from [[What is selectivity and cardinality for indexes]] is exactly what interviewers probe.

## Where low cardinality becomes valuable

Three standard plays. Composite leading column: an index on (status, created_at) turns the status value into a contiguous run ordered by created_at, which serves filtered, sorted queries that neither column alone could — the run logic in [[How do you optimize ORDER BY with a filter]]. Partial index: WHERE status = 'open' excludes the closed bulk entirely, keeping the index small and hot, per [[What is a partial index in PostgreSQL]]. Bitmap indexing: Oracle's bitmap indexes are designed exactly for low-cardinality columns in analytical, read-mostly schemas, storing a bitmap per key value and combining them with AND/OR — and PostgreSQL reaches a similar effect at plan time with bitmap scans over B-trees, per [[What is a bitmap index scan in SQL plans]]. In ClickHouse the analog is different again: low-cardinality values are compressed and marked LowCardinality, and filtering rides the sorting key, not B-trees, per [[What is a sparse primary index in ClickHouse]].

```sql
-- weak alone: matches 40% of rows, planner scans
CREATE INDEX idx_active ON users (is_active);

-- strong: hot subset only, small and always useful
CREATE INDEX idx_tasks_open ON tasks (created_at DESC)
    WHERE status = 'open';
```

**Listing 1.** Same column, opposite outcomes: standalone boolean index wasted, partial index on the hot status earning its keep.

> [!warning] "Low cardinality means never index" and "females/males index is useless, period" both overreach
> The refuted absolutes: a low-cardinality column can be the right leading column, the right partial predicate, or the right bitmap target. What is almost always useless is the standalone single-column B-tree on a column whose typical predicate matches a large fraction. And the engine matters: Oracle bitmaps make low cardinality a feature, while an OLTP-heavy table with constant status updates suffers from any index that must be maintained, per [[When are database indexes a bad idea]].

> [!tip] Interview answer
> By itself, usually not: the predicate matches too many rows and a scan wins. But the column still earns its place in three patterns — leading a composite so it forms ordered runs, defining a partial index that excludes the dominant value, or feeding a bitmap index in analytical engines. So the answer is about predicate selectivity and workload, not about the column's distinct count alone.
