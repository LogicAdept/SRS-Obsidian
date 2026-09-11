<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/SQL #SRS

# How do database indexes work at a high level

> [!abstract] Short answer
> An index stores its keys in a searchable structure and, for each key, a pointer to the row. The planner decides per query whether that structure is cheaper than a scan. For a B-tree, a lookup walks from root to leaf, picks up the row pointers, and optionally fetches the rows; the same ordering also serves ranges, sorts, and prefixes of compound keys.

## The path from predicate to rows

When a query has `WHERE user_id = 42`, the planner first asks what access paths exist. If a B-tree index exists on `user_id`, the engine can seek into the tree: it compares keys page by page, descending a few levels, then scans the leaf range where `user_id = 42` holds. Each leaf entry carries a locator; PostgreSQL leaves hold heap TIDs, SQL Server nonclustered leaves hold a row locator, and InnoDB secondary leaves hold the primary key that is then looked up in the clustered index. If the predicate does not match the index's opclass or shape, the plan falls back to a scan, which is the boundary described in [[What is sargability in SQL]].


```d2
direction: down
root: "B-tree root\nkeys + downlinks" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
inner: "Internal pages\none downlink per child range" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
leaf: "Leaf pages\nkey + heap pointer (TID)" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
heap: "Heap table\nrows in arbitrary order" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
root -> inner: "descend on key"
inner -> leaf: "descend on key"
leaf -> heap: "fetch matching TIDs"
```

**Fig. 1.** A B-tree lookup descends from root to leaf, then follows the leaf pointers into the heap. The tree is shallow, so the walk costs a handful of page reads, not a scan of every row.

## Why ordering is the real superpower

Sorted leaves mean the engine gets ranges, sorting, and MIN/MAX for free. A composite B-tree on `(a, b, c)` is sorted by `a`, then `b`, then `c` within equal `a` values, which is the leftmost prefix property behind [[What is the leftmost prefix rule for composite indexes]]. It also means `ORDER BY` can be answered by scanning the index in order, and `LIMIT 10` can stop after ten rows, an interaction explained in [[How does LIMIT interact with ORDER BY and indexes]].

## The cost side and the check

Every write to the table touches each index that contains the changed columns, so insert-heavy workloads feel index count directly. Engines therefore expose tooling to audit indexes: PostgreSQL has `pg_stat_user_indexes.idx_scan` and `EXPLAIN`, MySQL has `EXPLAIN` plus the `sys` schema, and ClickHouse shows granules skipped per index in `EXPLAIN indexes = 1`. The reading path for PostgreSQL plans, including the difference between Index Cond and Filter, is covered in [[How do you read EXPLAIN ANALYZE in PostgreSQL]].

> [!warning] "It has an index" is not "it uses the index"
> The planner only uses an index when the predicate shape, the operator class, and the cost model agree. Functions on the column, leading wildcards, type mismatches, or a plan that already touches half the table will all produce a scan despite the index existing. Always check the plan, not the DDL.

> [!tip] Interview answer
> An index is a sorted key-to-pointer structure. A lookup descends the B-tree to the leaf range, collects row pointers, and fetches rows if needed. Because keys are ordered, the same structure serves equality, ranges, ordered output, and leftmost prefixes of compound keys. The planner uses it only when it is cheaper than a scan, and every write must maintain it, so indexes are a measured trade-off, not a default.
