<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/NoSQL/Elasticsearch #SRS

# When should you use a ClickHouse text index instead of Elasticsearch

> [!abstract] Short answer
> Use the ClickHouse text index when your data already lives in ClickHouse and the search is token-level filtering inside analytics — logs and events where you filter by tokens, then aggregate at billions of rows. Choose Elasticsearch when you need a dedicated search product's surface: BM25 relevance ranking, complex query DSL, fuzzy matching and suggesters, and horizontal scale for search-first workloads.

## The case for staying in ClickHouse

The text index is a real inverted index integrated into the MergeTree storage model: tokenized lookups resolve through the index while the rest of the query — aggregations, GROUP BY over user_id, time-windowed analytics — runs in the same engine at columnar speed, per [[What is a text index in ClickHouse]]. For observability and log platforms this is decisive: the query pattern is "which services logged 'connection refused' in the last hour, grouped by customer" — a filter-plus-aggregation, not a ranked document search. Keeping it in ClickHouse removes a sync pipeline and a second cluster, and the docs' own guidance for log search design (ORDER BY shaping plus skip/text indexes) lives in [[How do you search logs in ClickHouse]]. The deprecated bloom-based predecessors and the migration story are in [[What is ngrambf_v1 versus tokenbf_v1]].

```sql
-- filter by tokens, aggregate at scale: one engine, one copy of the data
SELECT service, count()
FROM logs
WHERE hasAnyTokens(message, ['timeout', 'refused'])
  AND ts >= now() - INTERVAL 1 HOUR
GROUP BY service;
```

**Listing 1.** The typical win: token filtering feeding aggregation, with no second system in the path.

## The boundary where Elasticsearch earns its cluster

Elasticsearch exists for search-first workloads: relevance-ranked results over documents (BM25 with per-field tuning), rich analyzers per language, fuzzy and phrase-suggest features, pagination through large result sets, and sharding tuned for query concurrency rather than aggregation throughput. If the product is "users search the corpus and get ranked documents", building it on a granule-skipping index is a category error, the same boundary as the SQL-versus-ES decision in [[When should you use Elasticsearch instead of SQL search]]. The honest middle answer names the operational asymmetry: ClickHouse's text index adds one index definition to a system you already run; Elasticsearch adds a cluster, a sync path, and a consistency model — justified by search being the product, not by substring speed.

> [!warning] "ClickHouse has a text index now, so drop Elasticsearch" over-corrects
> The text index skips granules and feeds aggregations; it does not provide relevance scoring, pagination over ranked documents, or the analyzer ecosystem. Conversely, keeping Elasticsearch only because "someone said FTS is slow" while queries are aggregations over logs wastes an entire subsystem, per [[When should you use full-text search instead of LIKE]]. The decision is workload-shaped: ranked document retrieval versus token-filtered analytics.

> [!tip] Interview answer
> I stay in ClickHouse when search is a filter inside analytics over data already there — log lines, events, token predicates feeding aggregations — because the text index does that in one system at columnar speed. I choose Elasticsearch when search itself is the product: BM25 ranking, fuzzy matching, suggesters, and horizontal search scale. Adding ES means a sync pipeline and a second cluster, so the feature surface has to justify it.
