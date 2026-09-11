<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/SQL #SRS

# How do you count unique users in ClickHouse?

> [!abstract] Short answer
> Three functions, one trade-off: `uniq(user_id)` is the default approximate counter (adaptive sampling over a 65536-hash state, docs recommend it in almost all scenarios); `uniqCombined(user_id)` uses array→hash table→HyperLogLog with an error-correction table — several times less memory and several times more accurate than `uniq`, slightly slower; `uniqExact(user_id)` is the exact `COUNT(DISTINCT)` with unbounded memory — use it for small cardinalities or when the number must be defensible.

## The precision-memory ladder

`uniq` hashes values and keeps a sample of up to 65536 hash values (adaptive sampling); it is CPU-cheap and composable — states from many shards merge ([[What are aggregate function combinators in ClickHouse]]). `uniqCombined` switches implementations by cardinality and is deterministic in result; note the 32-bit hash for non-String types — for cardinalities beyond a few tens of billions use `uniqCombined64`. `uniqExact` keeps every distinct value: memory grows with distinct count, so counting uniques across billions of rows is exactly the query that OOMs a cluster. All three support multiple arguments (tuples) and are distributed-aware, merging partial states rather than raw rows.

```sql
SELECT
    uniqCombined(user_id)        AS approx_fast,   -- dashboards
    uniq(user_id)                AS approx_default,
    uniqExact(user_id)           AS exact          -- finance queries only
FROM events
WHERE ts >= today() - 1;
```

**Listing 1.** The three counters side by side; differences shrink or explode with cardinality.

## Choosing in practice

Dashboard metrics, alerting, and A/B readouts use `uniq`/`uniqCombined` — the error (roughly sub-percent) is stable and documented, and pre-aggregated states via `-State` combinators or [[What are projections in ClickHouse]] make them nearly free at query time. `uniqExact` is reserved for small, verifiable numbers (billing, SLA reports) or bounded windows where the distinct count is provably modest. If uniques must be counted incrementally over streaming data, the same functions appear in materialized-view targets as `uniqCombinedState` ([[How do materialized views work in ClickHouse]]).

> [!warning] "uniq" results are not stable across engines or configurations
> Approximate counters can differ between runs, engines, and result-caching layers — quoting `uniq()` as an exact number in a report is the classic mistake. Conversely, `uniqExact` on a billion-row table is not "slow", it is memory-bound by design. State which counter a number came from when it matters who consumes it.

> [!tip] Interview answer
> Default to uniq — adaptive-sampling approximate, cheap, recommended by the docs; uniqCombined when you need tighter accuracy with less memory (HyperLogLog-based, mind the 32-bit hash at extreme cardinalities); uniqExact only for exactness requirements with bounded cardinality. All three merge partial states, so they fit distributed and pre-aggregated setups.
