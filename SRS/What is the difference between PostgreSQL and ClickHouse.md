<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/OLAP/ClickHouse #SRS

# What is the difference between PostgreSQL and ClickHouse?

> [!abstract] Short answer
> Row store versus column store: PostgreSQL is an OLTP generalist — MVCC row updates, transactions, constraints, rich secondary indexes; ClickHouse is an OLAP columnar engine — data compressed per column, processed by vectors, aggregated over billions of rows fast, with a deliberately weak update and transaction story (no full-fledged transactions, per the project's own feature list). They frequently coexist: OLTP in Postgres, replication of events into ClickHouse for analytics.

## The architecture split

| Dimension | PostgreSQL | ClickHouse |
|---|---|---|
| Storage | row-oriented heap pages | column-oriented parts, compressed |
| Optimized for | point reads/writes, transactions | aggregations and scans over many rows |
| Updates/deletes | first-class (MVCC) | mutations are heavy rewrites; ReplacingMergeTree dedup patterns |
| Transactions | full ACID | no full-fledged transactions |
| Indexing | B-tree, GIN, GiST, BRIN | sparse primary key + data-skipping indexes |
| Joins | mature planner | strong, but large-join semantics differ (hash, on-disk limits) |
| Consistency | per-statement/tx snapshots | eventual parts merging |

ClickHouse's own documentation names the essentials: a true column-oriented DBMS, vectorized processing, data compressed by columns, physically sorted by primary key for fast range extraction — and explicitly lists no full-fledged transactions among the features it does not provide.

```d2
oltp: "PostgreSQL\nOLTP: many small reads/writes,\nconstraints, updates" {width: 330; height: 90}
olap: "ClickHouse\nOLAP: scans, aggregations,\nappend-heavy time series" {width: 330; height: 90}
cdc: "Event flow\nCDC / inserts" {width: 240; height: 60}
oltp -> cdc -> olap: "pipeline"
```

**Fig. 1.** The common production shape: Postgres as source of truth, ClickHouse as analytical engine fed by events ([[What is change data capture with Kafka]], [[How do you ingest Kafka into ClickHouse]]).

## Consequences that surprise each side

- Coming from Postgres: updates and deletes are mutations — plan append-only designs or MergeTree dedup ([[How do you drop old data quickly in ClickHouse]]); there are no foreign keys; eventual consistency across parts.
- Coming from ClickHouse: PostgreSQL's per-row indexes and transactions are exactly why it cannot match columnar scan throughput — different physics ([[What is a column-store index and when would you use one]] for the columnar idea inside row engines).
- Search and text: each has its own acceleration ([[How does ClickHouse accelerate LIKE and substring search]] versus [[How does full-text search work in PostgreSQL]]).

> [!warning] "Just put it in Postgres until it grows" has a sharp edge
> Analytical workloads degrade a row-store OLTP engine non-linearly: wide scans evict the buffer cache ([[What are shared_buffers and work_mem in PostgreSQL]]), aggregates fight with OLTP latency, and by the time it hurts, the schema is deeply relational. The honest design names the analytics path from day one — even if the first year it runs in Postgres.

> [!tip] Interview answer
> PostgreSQL is a row-oriented OLTP engine: MVCC updates, full ACID, rich per-row indexes. ClickHouse is a column-oriented OLAP engine: compressed columns, vectorized scans, sparse primary indexes, blazing aggregations — and intentionally weak updates, deletes and no full transactions. They complement: OLTP in Postgres, event-fed analytics in ClickHouse, usually via CDC or direct inserts.
