<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How do you search logs in ClickHouse

> [!abstract] Short answer
> Shape the table around the filters: ORDER BY starting with a coarse time bucket or service and ending with the timestamp, partition by month at most, keep text in a column with a text index for token search, and verify granule pruning with EXPLAIN indexes = 1. That design makes "errors for service X in the last hour" a granule-range question instead of a full scan.

## The table design that does the work

The docs' log-search guidance converges on one shape: the sorting key should match the dominant filters — (service, ts) when searches are per-service, or (toDate(ts), service, ts) when dashboards jump to a day and then filter by service — with time as the final column so data inside granules stays time-correlated. Partitioning belongs at month granularity at most: the MergeTree docs explicitly warn that partitioning does not speed up queries in contrast to the ORDER BY expression and should never be too granular, and never by client identifiers. Low-cardinality attributes like service or level fit LowCardinality(String). This is the key-design logic of [[How do you choose ORDER BY in ClickHouse]] applied to the log workload.

```sql
CREATE TABLE logs
(
    ts      DateTime,
    service LowCardinality(String),
    level   LowCardinality(String),
    message String
) ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (toDate(ts), service, ts);

ALTER TABLE logs ADD INDEX msg_text message TYPE text(tokenizer splitByNonAlpha) GRANULARITY 4;
ALTER TABLE logs MATERIALIZE INDEX msg_text;
```

**Listing 1.** Monthly partitions, service-first sorting with time last, and a tokenized text index on message.

## Searching the text and verifying the plan

Word-level predicates go through the text index functions — hasAnyTokens, hasAllTokens, hasPhrase — which the docs recommend over the deprecated tokenbf_v1/ngrambf_v1 bloom filters, per [[What is a text index in ClickHouse]] and [[What is ngrambf_v1 versus tokenbf_v1]]; arbitrary substring LIKE remains a scan outside token shapes, per [[How does ClickHouse accelerate LIKE and substring search]]. Every layer is then verified the same way: EXPLAIN indexes = 1 shows Partition, PrimaryKey, and Skip stages with granules before/after, per [[How do you verify a ClickHouse index is used]], and granule-level usefulness still depends on correlation — a message token present in every granule defeats the index, per [[Why might a ClickHouse skip index not help]]. When the workload grows into ranked document search or needs ES-class query features, that is the boundary decision in [[When should you use a ClickHouse text index instead of Elasticsearch]].

> [!warning] "Partition by hour for faster search" is the classic ClickHouse footgun
> Over-partitioning floods the system with small parts, degrading merges, ingestion, and query performance — the docs warn directly against granular partitioning and against partitioning by client IDs, recommending month-level at most. The actual filter speed comes from the ORDER BY key and indexes, not from partition count. The sibling mistake: putting the timestamp first in ORDER BY, which prunes nothing for per-service queries.

> [!tip] Interview answer
> I design logs around the dashboard: partition by month, ORDER BY (toDate(ts), service, ts) so service-and-time filters prune granule ranges, LowCardinality for service and level, and a tokenized text index on message for word search via hasAnyTokens. I verify with EXPLAIN indexes = 1 granule counts. Full scans only remain for arbitrary substring patterns, and at that point the fix is usually query shape, not more partitions.
