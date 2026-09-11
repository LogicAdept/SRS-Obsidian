<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# What is Index Skip Scan

> [!abstract] Short answer
> Skip scan lets a query use a composite index even when its leading column is not constrained: the engine probes each distinct value of the leading column and runs a range scan on the remaining columns within each probe. It relaxes the leftmost prefix rule when the leading column has few distinct values.

## MySQL's definition and conditions

MySQL 8.0 introduced Skip Scan as a range access method, and the manual's example is the honest baseline: without conditions on the first key part, a plain index scan reads every entry; skip scan instead gets each distinct value of the first part, builds a range including the predicate on the second part, and scans that subrange, repeating per distinct value. The manual lists its preconditions: a compound index where the query references only index columns, no GROUP BY or DISTINCT, equality predicates with constants on the prefix parts, a range condition on the skipped-over column's successor, and a conjunctive WHERE. In `EXPLAIN` it shows as `Using index for skip scan` in Extra, it is controlled by the `skip_scan` optimizer switch (on by default), and an `ANALYZE TABLE` beforehand matters because distinct-value estimates drive the plan.

```sql
CREATE TABLE t1 (f1 INT NOT NULL, f2 INT NOT NULL, PRIMARY KEY(f1, f2));
EXPLAIN SELECT f1, f2 FROM t1 WHERE f2 > 40;
-- Extra: Using index for skip scan
```

**Listing 1.** The manual's own shape: no predicate on the leading column `f1`, yet the index on `(f1, f2)` serves `f2 > 40` by probing distinct `f1` values.

## Oracle's earlier skip scan and PostgreSQL 18

Oracle implemented index skip scan much earlier and describes the same principle: a leading column with few distinct values can be skipped by logically splitting the index into subindexes per value. PostgreSQL added B-tree skip scan in version 18: its docs describe using a multicolumn index for a query that constrains later columns by probing each value of the unconstrained leading column, working best when the leading column has no more than a few hundred distinct values. That changes some classic advice where a separate index on the trailing column was the only good option, but the cost grows with leading-column cardinality, so for a truly high-cardinality prefix the separate index still wins, and the base rule remains in [[What is the leftmost prefix rule for composite indexes]].

> [!warning] "Skip scan makes column order irrelevant" is the overreach to refuse
> Skip scan is a fallback with conditions, not a permission to design composite indexes randomly. Each distinct prefix value is a separate range scan, so a leading column with millions of values degrades to repeated scans that can be slower than a sequential scan or a purpose-built index. The optimizer also needs fresh statistics to even consider it, tying it to [[How do stale statistics hurt a query plan]].

> [!tip] Interview answer
> Skip scan handles queries that filter later columns of a composite index without constraining the leading one: the engine probes each distinct value of the leading column and range-scans the rest within it. MySQL 8.0 formalized it with `Using index for skip scan` in EXPLAIN and specific preconditions, Oracle has had index skip scan for years, and PostgreSQL added B-tree skip scan in 18. It pays off only when the leading column has few distinct values and stats are fresh.
