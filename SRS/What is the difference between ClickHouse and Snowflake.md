<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/OLAP/Snowflake #SystemDesign/Performance #SRS

# What is the difference between ClickHouse and Snowflake?

> [!abstract] Short answer
> Snowflake is a fully managed cloud data warehouse: storage is micro-partitioned files in cloud object storage, compute is separately billed virtual warehouses, and there is no user-managed indexing — pruning comes from micro-partition metadata plus optional clustering keys. ClickHouse is an open-source engine (also offered as a cloud service) with user-designed layouts — sort keys, skip indexes, projections — engineered for second-scale queries over billions of rows at the lowest storage+compute cost.

## Storage and indexing models

Snowflake stores table data in compressed columnar micro-partitions (contiguous units typically holding ~16 MB compressed) and records min/max metadata per partition; queries prune on that metadata, and deliberate re-clustering (via clustering keys) is a background service rather than a DDL decision. ClickHouse hands layout control to the user: `ORDER BY` defines physical order per part ([[What is the difference between PRIMARY KEY and ORDER BY in ClickHouse]]), sparse primary indexes prune granules ([[What is a sparse primary index in ClickHouse]]), and skipping indexes/projections add secondary paths ([[What data skipping indexes exist in ClickHouse]]) — more design surface, more potential speed, more responsibility. Snowflake's separation of compute (virtual warehouses, per-second billing) suits elastic team workloads; ClickHouse's model suits always-on ingestion-serving pipelines with tight cost-per-query goals.

```sql
-- ClickHouse: layout is explicit and query-visible
CREATE TABLE events
(
    ts DateTime,
    user_id UInt64,
    country LowCardinality(String)
)
ENGINE = MergeTree
ORDER BY (country, ts);   -- decides pruning for every query
```

**Listing 1.** In ClickHouse, the operator owns the physical design that Snowflake's service manages automatically.

## Positioning

Snowflake wins on zero-ops elasticity, ecosystem breadth (Time Travel, data sharing, Iceberg tables), and SQL-warehouse familiarity — the default for cloud-native BI at organizational scale. ClickHouse wins on latency and throughput per dollar for real-time analytics: streaming ingestion ([[What are async inserts in ClickHouse]]), sub-second aggregations over event data, observability and clickstream serving, plus self-hosting freedom. The ClickHouse docs even ship a Snowflake migration guide — the migration direction is usually "snowballed warehouse costs or serving latency" pushing teams to bring hot analytical serving into ClickHouse while Snowflake keeps lakehouse-scale warehousing.

> [!warning] "No indexes" is not "no tuning" — and vice versa
> Snowflake's automatic clustering hides physical design but bills for it (clustering credits, warehouse time); ClickHouse exposes ORDER BY but shifts the cost of a bad key onto every query ([[When should you not use ClickHouse]]). Interview answers that frame Snowflake as "unoptimizable" or ClickHouse as "requires a DBA for everything" miss that both spend the same budget — automatically versus explicitly.

> [!tip] Interview answer
> Snowflake is a managed warehouse: micro-partitioned columnar storage in cloud object storage, elastic virtual warehouses, pruning by partition metadata and background clustering — zero physical design. ClickHouse is an open-source engine where you design the layout — sort keys, skip indexes, projections — for sub-second analytics over streaming data at minimal cost. Managed elasticity versus engineered speed-per-dollar.
