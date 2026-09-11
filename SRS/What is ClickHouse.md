<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is ClickHouse?

> [!abstract] Short answer
> ClickHouse is an open-source, column-oriented OLAP database management system built for real-time analytical queries over billions of rows. Data is stored, read, and compressed column by column, which makes wide-table aggregations and scans orders of magnitude faster than row-store databases, at the cost of weak single-row point access and limited transactions.

It began at Yandex as the engine behind Yandex.Metrica (custom reports over trillions of web hits) and was open-sourced in 2016 under the Apache 2.0 license. It is a DBMS, not a library: it ships its own SQL dialect, its own storage engines, and a distributed cluster mode. Tables are typically served by the [[What is the MergeTree engine in ClickHouse]] family, whose LSM-like design accepts millions of rows per second in append-heavy workloads. Common deployments ingest event, log, and metrics streams — for example through [[How do you ingest Kafka into ClickHouse]] — and serve dashboards or ad-hoc analytics on top. The engine is [[What is the MergeTree engine in ClickHouse]]-family storage under a vectorized SQL layer, which is the root of both its strengths and its limits ([[When should you not use ClickHouse]]).

## Columnar and vectorized

Rows stay intact in a row store; in a column store each column lives in its own compressed file, so a query touching 3 columns out of 200 reads 3 column streams instead of whole rows. On top of that, the query layer processes data in batches (blocks of granules), uses SIMD instructions, and runs one execution lane per CPU core. These mechanisms are the subject of [[Why is ClickHouse fast for analytical queries]].

```sql
SELECT
    UserID,
    count() AS hits
FROM events
WHERE EventDate >= today() - 30
GROUP BY UserID
ORDER BY hits DESC
LIMIT 10;
```

**Listing 1.** A typical analytical query: filter, aggregate, rank. A row store reads every row's every column; ClickHouse reads two column streams and evaluates it in parallel lanes.

> [!warning] Not a drop-in OLTP replacement
> ClickHouse has no full-fledged transactions, no high-rate low-latency row updates or deletes (there are only batch operations such as [[What are mutations in ClickHouse]]), and its [[What is a sparse primary index in ClickHouse]] is not designed to fetch single rows by key. The official docs list these as deliberate disadvantages, so "replace PostgreSQL" is a wrong deployment goal — keep OLTP in a row store and move analytics to ClickHouse, as [[What is the difference between PostgreSQL and ClickHouse]] explains.

> [!tip] Interview answer
> ClickHouse is a column-oriented OLAP DBMS: it stores each column separately, compresses it, and runs vectorized, parallel query execution. It shines on append-heavy analytics over huge tables — event logs, metrics, user behavior — and is weak at single-row lookups, frequent small updates, and multi-statement transactions, so it complements rather than replaces an OLTP database.
