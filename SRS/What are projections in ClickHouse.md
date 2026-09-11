<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# What are projections in ClickHouse?

> [!abstract] Short answer
> A projection is a hidden, part-level copy of the table data — a `SELECT` with its own column set, `GROUP BY`, and `ORDER BY` stored inside each data part. The optimizer rewrites eligible queries to read the projection instead of the base table, giving you a second sort order or pre-aggregation with automatic usage and part-level consistency.

## Mechanics

Defined inline at table creation (`PROJECTION name (SELECT ... GROUP BY ...)`), a projection lives inside each part like an attached mini-table; background merges keep base and projection rows in sync, so both are always consistent — unlike standalone materialized views, where source and target drift between inserts. Queries don't mention projections: the optimizer detects one that answers the query cheaper and substitutes it, which you verify with `EXPLAIN indexes = 1` (the plan names the projection). Guardrails exist: projections don't work with `FINAL`, and `force_optimize_projection` can make the optimizer require one — the standard enforcement in dashboards that depend on a pre-aggregation.

```sql
CREATE TABLE visits
(
    UserID UInt64,
    EventDate Date,
    URL String,
    PROJECTION by_user
        (
            SELECT UserID, count(), uniqExact(URL)
            GROUP BY UserID
        ),
    PROJECTION by_url
        (
            SELECT * ORDER BY (URL, EventDate)
        )
)
ENGINE = MergeTree ORDER BY (EventDate, UserID);

ALTER TABLE visits MATERIALIZE PROJECTION by_url;  -- backfill existing parts
```

**Listing 1.** Two projections — a per-user pre-aggregation and a second sort order — plus the backfill mutation for existing data.

## Projections versus materialized views

Both give second access paths; the trade is consistency and scope. Projections inherit the base table's shard/replication, update atomically per part, and need zero pipeline maintenance, but they multiply storage and merge work inside the table and cannot span tables. Materialized views ([[How do materialized views work in ClickHouse]]) can join, fan out to different engines, and reduce the hot table's weight — at the cost of operating that pipeline. Compare [[What is the Kafka to ClickHouse materialized view pattern]] for the ingestion-side version of this choice.

> [!warning] Projections are not free storage
> Every projection is a full copy of the selected columns for every part, and merges write it too — tables with several heavy projections slow down inserts and balloon in size. They also can't serve `FINAL` reads. Use them for measured, repetitive query patterns; if the "projection" keeps growing more columns, it usually wants to be a separate materialized-view target table.

> [!tip] Interview answer
> Projections are part-level materialized views: an inner SELECT with its own aggregation or sort stored in every part, kept atomic with the base data by merges, and chosen automatically by the optimizer. They give a second sort key or pre-aggregation without pipeline plumbing, paid for in storage and write amplification.
