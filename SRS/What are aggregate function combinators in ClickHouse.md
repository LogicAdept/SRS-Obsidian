<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/SQL #SRS

# What are aggregate function combinators in ClickHouse?

> [!abstract] Short answer
> Combinators are suffixes that programmatically derive new aggregate functions from existing ones: `-If` adds a condition, `-Array` maps over arrays, `-State`/`-Merge` expose and combine partial aggregation states, `-ForEach` applies a function per sub-column. They are the grammar behind incremental materialized views and conditional aggregation — `countIf`, `sumState`, `uniqMergeState` and friends.

## The suffix grammar

`-If` appends a condition argument — `sumIf(x, cond)` processes only rows passing `cond` (the standard way to build per-dimension counters from one pass). `-Array` distributes the aggregate over array elements — `sumArray(arr)` sums inside each row's array without `ARRAY JOIN`. `-State` returns the aggregation's intermediate state (an `AggregateFunction(...)` column) instead of the final value; `-Merge` combines such states into a final result; `-MergeState` combines states and returns a state again. These three are what make AggregatingMergeTree tables work (the additive cousin is [[What is SummingMergeTree]]): inserts write `countState()` rows, merges fold states, reads finish with `countMerge()` — the same machinery approximates uniques in [[How do you count unique users in ClickHouse]]. `-ForEach` applies the function element-wise to fixed-size arrays/tuples.

```sql
-- conditional aggregation in one pass
SELECT service, countIf(severity = 'ERROR') AS errors
FROM logs GROUP BY service;

-- state lifecycle across a materialized view
-- target: AggregateFunction(count) column in AggregatingMergeTree
INSERT INTO mv_target SELECT toDate(ts), countState() FROM raw GROUP BY toDate(ts);
SELECT day, countMerge(votes) FROM mv_target GROUP BY day;
```

**Listing 1.** `-If` in everyday queries; `-State`/`-Merge` across the insert-merge-read cycle.

```d2
base: "sum / count / uniq\nbase aggregate functions" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
suffixes: "suffix combinators\n-If  -Array  -ForEach\n-State  -Merge  -MergeState" {
  width: 380
  height: 100
  style.fill: "#fff3e0"
}
derived: "sumIf, sumArray,\nuniqState, uniqMerge..." {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
base -> suffixes
suffixes -> derived
```

**Fig. 1.** Combinators are a compositional naming system: one base function, many derived behaviors.

> [!warning] -State values are opaque blobs, not numbers
> A state column can only be read with its matching `-Merge`/`finalizeAggregation` — casting or summing an `AggregateFunction` column is a type error, and states from different aggregate functions are incompatible. The classic production bug is a materialized view target typed with `count()` instead of `AggregateFunction(count)`/`countState()` writes — rows overwrite instead of merging ([[How do materialized views work in ClickHouse]]).

> [!tip] Interview answer
> Combinators are suffixes that derive aggregate variants: -If filters rows, -Array aggregates inside arrays, -ForEach goes element-wise, and -State/-Merge expose partial aggregation states so results can be stored in AggregatingMergeTree tables and combined later — the machinery behind ClickHouse materialized views and incremental aggregation.
