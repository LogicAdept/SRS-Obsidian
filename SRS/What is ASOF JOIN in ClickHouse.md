<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/SQL #SRS

# What is ASOF JOIN in ClickHouse?

> [!abstract] Short answer
> ASOF JOIN matches each left row with the *closest* right row on an ordered column — the standard "as-of price" join: no exact match required. It needs equality conditions plus exactly one closest-match condition (`>`, `>=`, `<`, `<=`) over an asof column of Int, UInt, Float, Date, DateTime, or Decimal type, and is supported by the hash and full_sorting_merge join algorithms.

## Semantics

The ON form is `ASOF [LEFT] JOIN t2 ON equi_cond AND closest_match_cond` — any number of equality conditions and exactly one inequality; the USING form lists equi columns with the asof column always last, defaulting the match direction to `t1.asof >= t2.asof` (the most recent right-side record at or before the left event). Equal timestamps are closest when available; a right row that fails the inequality matches nothing unless the join is LEFT (which null-fills). The classic example: user events at 12:00 and 13:00 join to price snapshots at 11:59 and 13:00, while a 12:30 snapshot matches neither.

```sql
SELECT e.user_id, e.ev_time, p.price
FROM trades AS e
ASOF LEFT JOIN quotes AS p
ON e.user_id = p.user_id AND p.t <= e.t;
-- latest quote at or before each trade, per user
```

**Listing 1.** Per-entity latest-lookup: equality on `user_id`, closest match on timestamps with `<=`.

## Where it fits

Market-data lookups, configuration/version state at time T, CDC "value as of event time" enrichment ([[What is the Kafka to ClickHouse materialized view pattern]] is the ingestion side of that) — anywhere a temporal nearest-neighbor replaces a full sort-merge, and point-in-time lookups that a [[What is a ClickHouse dictionary]] cannot answer because history matters. It is a hash-join-friendly pattern, but the asof column cannot be the *only* join condition under the hash algorithm, and NaN values break ordering comparisons (filter them on both sides). This is one of the join types ClickHouse supports alongside ANY/SEMI/ANTI [[What is GLOBAL JOIN in ClickHouse]] covers the distributed dimension: on sharded tables, ASOF JOIN needs the right side co-located or GLOBAL-broadcast, with the same cost trade-offs.

> [!warning] ASOF is not "JOIN with an approximate match on anything"
> The match is strictly on one ordered column with one inequality — adding a second fuzzy condition is a syntax error, and unordered columns cannot be asof columns. Common bug: forgetting that the inequality direction is fixed per join (USING defaults to `>=` from the left row), which silently flips "price known before the trade" into "price known after" — a difference that matters enormously in finance-shaped workloads.

> [!tip] Interview answer
> ASOF JOIN finds the nearest right-side record on an ordered column per equality key — trades joined to the latest quote at or before them. You give equality conditions plus exactly one inequality on a comparable asof column, and it runs on hash or full_sorting_merge algorithms. It's the temporal nearest-match join ClickHouse ships natively.
