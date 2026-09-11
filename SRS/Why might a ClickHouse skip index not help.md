<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# Why might a ClickHouse skip index not help?

> [!abstract] Short answer
> Skip indexes only pay off when a predicate is selective at the block level and the engine can actually apply them. They silently do nothing when the query expression doesn't match the index expression, when the data distribution makes every block a candidate, when the predicate is a range on an unordered index type, or when the primary key already pruned the same granules — and each index still costs write time and storage.

## The failure modes

The docs' tutorial dedicates a section to "the index is being applied but not helping": the most common cause is non-selectivity — if 90% of blocks contain the searched value, the filters can't prune and the query pays the index overhead anyway. Beyond that: `minmax` fails when the indexed column is uncorrelated with the sort key or when values per block span a wide range; `set`/`bloom_filter` types are unordered and cannot serve range predicates; `ngram`/`token` filters only match predicates expressible in their split model; and the planner only applies an index when the WHERE condition is exactly the indexed expression (an index on `lower(url)` does not serve `url LIKE ...`). Finally, `use_skip_indexes` may be off, and old parts never built the index unless you [[How do you materialize a skip index on existing ClickHouse data]].

```sql
-- predicate must match the indexed expression
ALTER TABLE logs ADD INDEX lc_ix lower(msg) TYPE tokenbf_v1(1024, 3, 0) GRANULARITY 1;

SELECT count() FROM logs WHERE hasToken(msg, 'timeout');        -- index NOT used
SELECT count() FROM logs WHERE hasToken(lower(msg), 'timeout'); -- index used
```

**Listing 1.** Expression mismatch disables the index; the query must reference the same expression the index computes.

## Diagnose with EXPLAIN, fix with data design

Run the query with `EXPLAIN indexes = 1` and compare granule counts before/after each index ([[How do you verify a ClickHouse index is used]]): an index line that filters nothing is dead weight. Structural fixes follow the diagnosis: move the column into the sort key if it filters most queries ([[How do you choose ORDER BY in ClickHouse]]), pre-aggregate with [[What are projections in ClickHouse]] when the pattern is a fixed aggregation, or accept the index and remove it. Cardinality checks (`uniq()`) and selectivity checks before creating any index avoid most of this churn.

> [!warning] An unused skip index is not free
> Every insert and merge must build and carry the index blocks even when no query ever prunes with them. Interviewers probe the cost side: "we added a bloom index and nothing changed" usually means either non-selective data or expression mismatch — and meanwhile writes got slower. Remove unused indexes as deliberately as you add them.

> [!tip] Interview answer
> A skip index helps only when the predicate matches the indexed expression and actually selects few blocks per part. Non-selective distributions, range predicates on unordered types, expression mismatches like missing lower(), or pruning already done by the primary key all neutralize it — while the index still taxes writes. EXPLAIN indexes=1 before/after granule counts is how I verify.
