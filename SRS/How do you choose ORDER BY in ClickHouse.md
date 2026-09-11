<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# How do you choose ORDER BY in ClickHouse?

> [!abstract] Short answer
> Pick the columns your hot queries filter on: columns compared with equality first, then range/sort columns, with lower-cardinality candidates earlier in the tuple. The sort key is the main query-optimization tool in ClickHouse — unlike partitioning — so a missed column costs granule reads on every query, but adding more columns bloats the index and slows writes.

## The selection algorithm

Start from the WHERE clauses of your frequent queries. A column filtered by `=` or `IN` belongs near the front; a column used for ranges or `GROUP BY` ordering follows it. The official guide's worked example puts `PostTypeId` first (cardinality 8, equality-filtered) and `toDate(CreationDate)` second, reasoning that date granularity is enough and a `Date` component keeps marks small. Columns that only occasionally filter, or that appear in aggregations, should *not* enter the key — cover them with skipping indexes ([[What data skipping indexes exist in ClickHouse]]) or a pre-aggregated [[What are projections in ClickHouse]]. For high-cardinality identifiers that alone would make a terrible leading key, the docs' counter-example is partitioning: never partition by client id — put client id first in ORDER BY instead ([[What is PARTITION BY in ClickHouse]]).

```sql
-- hot query shape: WHERE PostTypeId = 1 AND CreationDate >= '2026-01-01'
CREATE TABLE posts
(
    PostTypeId   LowCardinality(UInt8),   -- 8 distinct values
    CreationDate Date,
    OwnerUserId  UInt32,
    Title        String,
    Body         String
)
ENGINE = MergeTree
ORDER BY (PostTypeId, toDate(CreationDate), OwnerUserId);
```

**Listing 1.** Equality column, then range column, then an identifier: each key column is justified by a real predicate in the workload.

## Verify, don't guess

After creating the table, run the representative queries with `EXPLAIN indexes = 1` and compare `Granules: selected of total` — a key that selects a few percent of granules is doing its job ([[How do you verify a ClickHouse index is used]]). If two very different query shapes fight over one key, projections provide a second sorted copy of the data instead of compromising the primary layout. Remember the key is per-part sorted order, so [[What is the difference between PRIMARY KEY and ORDER BY in ClickHouse]] lets you trim the indexed prefix without changing sort order.

> [!warning] A wrong ORDER BY cannot be cheaply fixed
> The sort key is frozen at table creation; changing it later means `SELECT ... ORDER BY new_key` into a new table — a full data rewrite. That is why the key is chosen from measured access patterns, not from a hunch about "probably filtering by date", and why materialized views feeding differently-sorted target tables are the standard escape hatch for a second access path.

> [!tip] Interview answer
> I derive the key from hot query predicates: equality-filtered and low-cardinality columns first, then the range column — like `(PostTypeId, toDate(CreationDate))` in the docs example. More key columns cost index size and write amplification, so occasional filters go to skip indexes or projections instead, and I verify the choice with EXPLAIN granule counts before committing to it.
