<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #Databases/NoSQL/Elasticsearch #SRS

# When should you use a ClickHouse text index instead of Elasticsearch?

> [!abstract] Short answer
> Choose the ClickHouse text index when text search is one predicate among many over analytical data you already keep in ClickHouse — filter, aggregate, and time-window the same table without moving data. Choose Elasticsearch when you need a search product: relevance ranking, analyzers per language, distributed scoring, or free-text as the primary access path. The systems increasingly overlap on full text, but they optimize different workloads.

## Where the text index wins

ClickHouse compresses log/analytical columns far better than a document store and evaluates the rest of the query (aggregations, joins, window functions, time buckets) natively; the inverted text index ([[What is a text index in ClickHouse]]) prunes granules for token predicates with no false positives, and the surrounding machinery — sparse primary index, MinMax pruning, projections — handles everything else in the same scan. When the workload is "find error bursts last Tuesday, then aggregate by service", duplicating the corpus into a second system doubles storage and forces a two-hop join at query time; keeping it in ClickHouse with a text index avoids that entirely ([[How do you search logs in ClickHouse]]).

```sql
-- one query, one system: token search + aggregation + time bucket
SELECT toStartOfHour(timestamp) AS hour, service, count()
FROM logs
WHERE hasToken(lower(msg), 'timeout')
  AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY hour, service
ORDER BY hour;
```

**Listing 1.** The shape of query that favors staying in ClickHouse: search is a filter, the aggregation is the point.

## Where Elasticsearch stays the right answer

Elasticsearch is built around inverted indexes per shard with analyzers, scoring (BM25), fuzzy matching, synonyms, and rich per-language tokenization; relevance-ordered results and search-product features (completion suggesters, highlight, kNN) are not things the ClickHouse text index aims to provide. Elasticsearch's own docs describe it as an analytical search store with columnar doc-value modes — but for pure OLAP aggregation at compression ratios ClickHouse typically wins, so the "which is faster" framing is workload-shaped, not absolute. A pragmatic split: Elasticsearch for user-facing search, ClickHouse for analytics over the same events via streaming ingestion ([[How do you ingest Kafka into ClickHouse]]).

> [!warning] "Elasticsearch is only for search, ClickHouse only for analytics" is out of date
> Each system has been eating the other's edges: Elasticsearch added columnar analytic modes, ClickHouse added a real inverted index. The decision criteria that remain stable are: who owns the data of record, whether relevance ranking is required, and whether the text predicate feeds aggregations or returns documents. Migrating because "we need search" without checking which side of that line the workload sits on is the costly mistake.

> [!tip] Interview answer
> If text search is a filter over data I already analyze in ClickHouse, its text index gives inverted-index pruning with zero data movement and full SQL on top — that's the logging-observability sweet spot. If I need relevance scoring, language analyzers, fuzzy, or a search-first product, that's Elasticsearch. Overlap is real; the decision is workload shape, not fashion.
