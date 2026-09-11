<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is SummingMergeTree?

> [!abstract] Short answer
> SummingMergeTree folds rows with the same sorting key during background merges: numeric columns get summed, collapsing many detail rows into one partial sum per key. It is a pre-aggregation storage trick — the query must still aggregate over the merged states, because a key's rows live in several parts and are only eventually combined.

## Mechanics

Declared as `SummingMergeTree` (or with explicit sum columns `SummingMergeTree((col1, col2))`). On merge, all rows sharing the sorting-key tuple collapse into one row: columns with numeric types are added together (only those listed if you name them; unspecified numeric columns are summed too when possible), while non-numeric columns resolve to an arbitrary surviving value. The crucial consequence: at any moment a key may exist as *several* partial sums across different parts, so `SELECT sum(v)` — not `SELECT v` — is the correct read pattern; the engine guarantees only that summing the partials equals the total.

```sql
CREATE TABLE page_views
(
    site  String,
    day   Date,
    views UInt64
)
ENGINE = SummingMergeTree
ORDER BY (site, day);

INSERT INTO page_views VALUES ('a', '2026-09-01', 10), ('a', '2026-09-01', 5);
-- after some merge: one row ('a','2026-09-01',15) — but not guaranteed yet

SELECT site, day, sum(views) FROM page_views GROUP BY site, day;  -- always correct
```

**Listing 1.** Detail rows fold into partial sums; the correctness of reads comes from `GROUP BY` + `sum`, never from reading the column raw.

## Design notes

The engine sums rows with the same *sorting key* tuple — so the key defines the rollup grain, and the target shape is one row per key once all parts merge. Keys with high row counts per value shrink the most; keys that are almost unique save nothing. Columns you do not name in the explicit column list behave by the numeric-or-arbitrary rule above, which is why explicit lists are preferred in production DDL. For uniques, quantiles, or averages the state-carrying alternative is `AggregatingMergeTree` with `-State`/`-Merge` combinators, usually fed by a materialized view ([[How do materialized views work in ClickHouse]]).

> [!warning] Averaging with SummingMergeTree is a trap
> The engine can only sum — it has no notion of "average so far". If you store `hits` and `duration` and later compute `sum(duration)/sum(hits)`, that is correct; storing a precomputed `avg` column that gets summed is nonsense. For non-summable aggregates (uniques, averages, quantiles) use `AggregatingMergeTree` with `-State`/`-Merge` combinators ([[What are aggregate function combinators in ClickHouse]]) — or a materialized view writing those states ([[How do materialized views work in ClickHouse]]).

> [!tip] Interview answer
> SummingMergeTree sums numeric columns across rows with the same sort key during merges, shrinking detail data into per-key partials. Because merging is asynchronous and partial, reads must re-aggregate — sum over GROUP BY — and the engine is only for additive measures. For anything non-additive, AggregatingMergeTree with state combinators is the right tool.
