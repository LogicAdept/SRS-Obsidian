<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SystemDesign/Performance #SRS

# How do you search logs in ClickHouse?

> [!abstract] Short answer
> The observability stack pattern: one MergeTree table (or per-service tables) keyed by time and service, logs stored as typed columns plus a message string, a `text` index or Bloom-based string index on the message for token search, partitioning by day/month for retention, and aggregation of hot metrics into summary tables. Search is then a granule-pruned scan, not a full-table text crawl.

## The data layout

Logs want the same discipline as any analytics table: narrow types for the structured fields (severity, service, trace_id), and the message as a `String` column — optionally with structured extraction (`extract`/JSON parsing at insert) so most predicates never touch the text at all. `ORDER BY (service, timestamp)` gives the primary pruning path; `PARTITION BY toYYYYMM(timestamp)` handles retention via instant partition drops ([[What is PARTITION BY in ClickHouse]], [[How do you drop old data quickly in ClickHouse]]). ClickHouse ships a complete observability use-case guide around this schema, including OpenTelemetry ingestion pipelines.

```sql
CREATE TABLE logs
(
    timestamp DateTime,
    service   LowCardinality(String),
    severity  LowCardinality(String),
    trace_id  String,
    msg       String,
    INDEX msg_ix lower(msg) TYPE text(tokenizer = 'splitByNonAlpha') GRANULARITY 1,
    INDEX sev_ix severity TYPE set(100) GRANULARITY 1
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(timestamp)
ORDER BY (service, timestamp);

SELECT timestamp, msg FROM logs
WHERE service = 'payments' AND timestamp >= now() - 3600
  AND hasToken(lower(msg), 'timeout')
ORDER BY timestamp DESC LIMIT 100;
```

**Listing 1.** A production-shaped log table: structured columns carry most filters, the text index prunes message search.

## Search mechanics and tuning

The query above prunes by service and time first ([[What is a sparse primary index in ClickHouse]]), then the severity `set` index and message `text` index skip remaining blocks ([[What data skipping indexes exist in ClickHouse]]), and only surviving granules are scanned with SIMD string matching. Error hunting across everything ("where did 'timeout' appear last night?") is the case that justifies the text index; grep-like ad-hoc needles beyond token structure need n-gram Bloom filters ([[How does ClickHouse accelerate LIKE and substring search]]). For click-ops on trace ids, equality on `trace_id` prunes via a `bloom_filter` index; aggregations over logs (error rates per service) belong in materialized views ([[How do materialized views work in ClickHouse]]) so dashboards never rescan raw text.

> [!warning] Logs are not a heap you can just dump in
> The failure pattern is a single `String message` column with no key discipline: every search becomes a full scan, TTL deletes fight with tiny parts, and [[What causes Too many parts in ClickHouse]] fires from agent-style row-at-a-time inserts. Batching inserts (or [[What are async inserts in ClickHouse]]), typed columns for hot fields, and indexes only for the predicates you actually run are what keeps search fast a month later.

> [!tip] Interview answer
> Treat logs as a data-modeling problem: time-and-service sorted MergeTree with typed columns, monthly partitions for retention, a text index on the message for token search, Bloom indexes for trace ids, and MVs for hot aggregations. Search then prunes granules by key first and index second — full-text scans over petabyte log tables are a schema mistake, not a hardware one.
