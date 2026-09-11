<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How do you sample data in ClickHouse?

> [!abstract] Short answer
> Table-level sampling is declared with `SAMPLE BY <expr>` at CREATE and used per query with `SAMPLE k` in the SELECT — a deterministic, index-free random subset keyed by the sampling expression. `SAMPLE 0.1` samples ~10% of rows, `SAMPLE 10000` an absolute count approximation, and `SAMPLE 0.1 OFFSET 0.2` selects a different (non-overlapping) slice.

## Mechanics

The sampling expression is evaluated per row and must be included in the primary key ([[What is a sparse primary index in ClickHouse]] explains how key pruning rides the sorted layout) — the canonical pattern is `SAMPLE BY intHash32(UserID) ORDER BY (CounterID, EventDate, intHash32(UserID))` — so sampling slices respect the sorted layout and skip granules rather than filtering rows one by one. Because results are keyed by the expression, the same query with the same SAMPLE fraction returns the same subset — deterministic and repeatable, unlike `LIMIT N WITH TIES`-style random draws — and increasing the fraction strictly adds rows (monotonicity), which makes sampled statistics composable. `SAMPLE k OFFSET m` moves the window through the hash space to draw disjoint samples for A/B buckets.

```sql
CREATE TABLE hits
(
    EventDate Date,
    UserID    UInt64,
    URL       String
)
ENGINE = MergeTree
ORDER BY (UserID, EventDate)
SAMPLE BY intHash32(UserID);

SELECT count(), uniq(UserID)
FROM hits
SAMPLE 0.1;                 -- ~10% deterministic subset
```

**Listing 1.** Declare the sampling key on a hashed user id, then approximate heavy statistics on a tenth of the data.

## What sampling buys and costs

Estimating aggregations (counts, uniques via [[How do you count unique users in ClickHouse]], distributions) on a fixed fraction scales linearly — a 1% sample answers exploratory queries in a hundredth of the time with measurable error. Absolute-value sampling (`SAMPLE 10000`) caps the row count for quick peeks. But sampling is only meaningful for *estimates*: results are a subset, so exact aggregates need the full data, and predicates unrelated to the sampling key can skew the subset's representativeness for conditional statistics.

> [!warning] SAMPLE is a fraction of rows, not a fraction of matching rows
> Sampling happens over the table (by hash slice), then your WHERE applies — so `WHERE country = 'DE' SAMPLE 0.1` gives 10% of *all* rows that happen to be German, not 10% of German rows, and rare-population estimates get noisy. There is also no sampling without the key: a table created without `SAMPLE BY` cannot add it post-hoc without a rewrite. For one-off random subsets of a non-sampled table, use `rand()`-based filtering and accept the scan.

> [!tip] Interview answer
> ClickHouse sampling is declarative and deterministic: SAMPLE BY hash-expression in the DDL (which must sit in the primary key), SAMPLE fraction-or-count per query, OFFSET to draw disjoint slices. It prunes by the hash key, so it's fast and repeatable — perfect for exploratory stats — but it estimates over the table, not over your filtered population.
