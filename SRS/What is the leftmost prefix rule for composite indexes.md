<!--
reps: 0
priority: 0
-->
#Databases/Indexes/Composite #SRS

# What is the leftmost prefix rule for composite indexes

> [!abstract] Short answer
> A composite B-tree on (a, b, c) is sorted by a, then b within equal a, then c within equal (a, b). Therefore only a leading prefix — a, a+b, or a+b+c — can be used for seeks; a predicate on b or c alone cannot jump into the middle of the sort order. Skip scan, where available, is the exception that probes each distinct prefix value.

## Why the rule exists

The rule is a direct consequence of lexicographic ordering. In the sort order of (a, b, c), knowing `a = 5` confines you to a contiguous range, and adding `b = 7` narrows it again; that is what makes a tree seek possible. Knowing only `b = 7` does not describe any contiguous range — matching rows are scattered across every distinct `a` — so the engine must either read the whole index or fall back to a scan. PostgreSQL's multicolumn docs state it as: the index can be used when the leading columns are constrained by equality or ranges, and a query on later columns alone cannot use it. MySQL's multiple-column index docs express the same idea with the exact same consequence for ORDER BY: sorting by the second column alone does not benefit from the index.

```sql
CREATE INDEX idx_cust_date ON orders (customer_id, created_at);
-- seek works:    WHERE customer_id = 42
-- seek works:    WHERE customer_id = 42 AND created_at >= '2026-01-01'
-- cannot seek:   WHERE created_at >= '2026-01-01'          (no leading column)
-- cannot seek:   WHERE created_at >= '2026-01-01' AND customer_id IS NULL
```

**Listing 1.** The index on (customer_id, created_at) serves predicates only down the leftmost prefix chain.

## Practical consequences

Column order in the DDL is a workload decision, not a style choice: equality predicates first, the range or sort column last, because a range on an earlier column stops using deeper columns for seeking — a subtlety covered in [[How do you optimize ORDER BY with a filter]]. Within-prefix ORDER BY is also answered for free, per [[How do you avoid a sort with an index]]. If the trailing column is payload rather than a predicate target, INCLUDE keeps it out of the key, as in [[How would you explain Covering index]]. And where a query filters only on the trailing column, the modern escape hatches are the separate index or, in MySQL 8+ and PostgreSQL 18, the probe-each-prefix-value strategy described in [[What is Index Skip Scan]].

> [!warning] "The index contains b so it will be used for b" is the popular lie
> A composite index containing a column does not make that column seekable in any position. The exception is real but conditional: skip scan needs few distinct values in the leading column and fresh statistics. There is also the planner-side sibling: combining two single-column indexes with a bitmap OR/AND can answer a query without the composite, as in [[How do you combine several indexes in one query]].

> [!tip] Interview answer
> A composite B-tree is sorted lexicographically by its columns in order, so seeks work only along a leftmost prefix: (a), (a, b), (a, b, c). Predicates on later columns alone cannot define a contiguous range and fall back to scans unless skip scan probes each distinct prefix value. Design order follows the workload: equality columns first, then the range or sort column.
