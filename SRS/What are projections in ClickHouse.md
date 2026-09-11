<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What are projections in ClickHouse

> [!abstract] Short answer
> A projection is a hidden, automatically maintained transform of a table's data — typically a different ORDER BY, or an aggregate grouped by some key — stored alongside the table. The planner can choose a projection when it matches the query, so one table serves several access orders without hand-built materialized views.

## What they are and how they are declared

Projections are declared in the table DDL (or added with ALTER TABLE ADD PROJECTION) with a SELECT that either reorders columns — an ordinary projection with its own ORDER BY — or aggregates — a projection with GROUP BY producing pre-aggregated state. The engine maintains them during inserts and merges, so they stay consistent with the base parts without a separate refresh job; queries simply name the table, and the planner reads the projection when its shape serves the query better. Conceptually they are the managed generalization of "build a second table sorted differently and keep it in sync" — the pattern the skip-index best practices name alongside materialized views when an index cannot fix a workload, per [[Why might a ClickHouse skip index not help]].

```sql
CREATE TABLE visits
(
    user_id UInt64,
    ts      DateTime,
    country LowCardinality(String),
    viewed  UInt32,
    PROJECTION by_country
    (
        SELECT country, sum(viewed)
        GROUP BY country
    ),
    PROJECTION by_user_time
    (
        SELECT * ORDER BY (user_id, ts)
    )
) ENGINE = MergeTree
ORDER BY (toDate(ts), user_id);
```

**Listing 1.** One table, two access shapes: pre-aggregated per country, and user-time order regardless of the base key.

## Where they fit relative to indexes

The base ORDER BY and skip indexes prune granules on one physical layout; projections provide additional physical layouts with their own ordering or aggregation. That makes them the tool when the hottest query filters on a column that cannot be the sorting key — the trade-off is storage and write amplification, since every insert updates the base parts and every projection. They also subsume some skip-index use cases entirely: if queries aggregate by country, a grouped projection answers them by scanning far less data than any index would. The interplay with the primary key design is in [[How do you choose ORDER BY in ClickHouse]], the index menu they complement is in [[What data skipping indexes exist in ClickHouse]], and their effect is visible in EXPLAIN plans reading the projection's parts rather than the base table, verified per [[How do you verify a ClickHouse index is used]].

> [!warning] "Projection = materialized view" is the fuzzy version of the truth
> The functional overlap is real, but the mechanics differ: projections live inside the table, update transactionally with parts, and are chosen automatically by the planner; materialized views are separate tables with explicit refresh behavior and independent lifecycle. The cost trap is the same as any denormalization: each projection multiplies storage and slows ingestion, and unused projections are pure write tax — audit them like unused indexes.

> [!tip] Interview answer
> Projections are table-internal derived layouts: an ordinary projection reorders data under a different ORDER BY, an aggregate projection stores pre-grouped sums, and the engine maintains and picks them automatically. They shine when the main sorting key cannot serve a hot query shape — you add a second physical order instead of a second table. The cost is storage and write amplification, so they complement, not replace, a well-chosen ORDER BY.
