<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How do you choose ORDER BY in ClickHouse

> [!abstract] Short answer
> Put the columns your hottest queries filter on as a left prefix of the sorting key, ordered from lower to higher cardinality typically, and end with a correlation-friendly column like time. The sorting key cannot be changed retroactively, so it follows the dashboard workload: (user_id, event_time) for per-user analytics, (date, service, ts) for log search by service within days.

## The selection logic

The MergeTree docs' guidance on selecting a primary key is the reference: including a column improves performance when queries filter on it, and each additional key column trades index breadth for pruning power. The practical recipe from the docs' best-practice guides: identify the filter and GROUP BY columns of the dominant queries; make them the leading columns of ORDER BY so the sparse index prunes granules; append a time column to keep data within a granule time-correlated, which benefits both range filters and compression. Cardinality ordering matters because a high-cardinality column first makes later columns nearly useless for pruning — the same leftmost-prefix logic as B-trees in [[What is the leftmost prefix rule for composite indexes]], applied to marks instead of rows.

```sql
-- analytics per user: filter by user, then time range
CREATE TABLE clicks
(
    user_id    UInt64,
    event_time DateTime,
    url        String
) ENGINE = MergeTree
ORDER BY (user_id, event_time);

-- log search: time bucket first, service second, keep ts correlation
CREATE TABLE logs
(
    ts      DateTime,
    service LowCardinality(String),
    message String
) ENGINE = MergeTree
ORDER BY (toDate(ts), service, ts);
```

**Listing 1.** Two canonical shapes: user-first for per-user analytics; coarse-time plus service for log dashboards.

## What the key cannot do, and the escape hatches

The sorting key helps only predicates on its prefix; filters on other columns (message contents, rare attributes) need data-skipping indexes or projection-based redesign, per [[What data skipping indexes exist in ClickHouse]] and [[What are projections in ClickHouse]]. The skip-index guide's advice on correlation — batching inserts so related values land in the same granules — is also an ORDER BY-adjacent lever. Because ORDER BY is fixed at table creation (changing it requires recomputing data, e.g. via a new table + INSERT SELECT), the cost of a wrong key is high: the guide's own example shows a no-key table reading 8.87 million rows where a keyed one reads a few granules. Verification of the chosen key's effect is the granule accounting in [[How do you verify a ClickHouse index is used]].

> [!warning] "ORDER BY is just a default sort" and "partition key speeds queries" are the twin errors
> The sorting key is the indexing mechanism, not cosmetic ordering — and the docs explicitly warn that partitioning does not speed up queries (in contrast to the ORDER BY expression) and should not be more granular than by month, nor done by client identifiers. Over-partitioning creates many small parts that hurt merge and query performance, the opposite of the intended optimization.

> [!tip] Interview answer
> I design the sorting key from the workload's hottest filters: leading columns are the equality or GROUP BY filters, typically low to high cardinality, with a time column last for correlation and compression. The key is fixed at creation and is the main pruning mechanism, so it follows the dashboards. Filters outside the key go to skip indexes or projections, and I verify pruning with EXPLAIN indexes = 1.
