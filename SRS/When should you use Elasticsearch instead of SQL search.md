<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/NoSQL/Elasticsearch #SRS

# When should you use Elasticsearch instead of SQL search

> [!abstract] Short answer
> Stay in SQL (PostgreSQL FTS, trigram, GIN indexes) when the corpus is modest, consistency with transactional data matters, ranking needs are simple, and operating one system beats operating two. Move to Elasticsearch when you need relevance tuning, facets and aggregations, near-real-time ingestion at high volume, distributed horizontal scale, or fuzzy language features that the database would serve poorly.

## What the database gives you, and when it stops being enough

PostgreSQL full-text search gives stemming, ranking, boolean and phrase operators over a GIN-indexed tsvector transactionally consistent with your tables, per the mechanics in [[How does full-text search work in PostgreSQL]]; pg_trgm covers fuzzy substring work per [[How does a trigram index help SQL search]]. For a product with tens of millions of rows, a few text columns, and a search box, that stack removes an entire subsystem from your architecture — no synchronization pipeline, no second consistency model, no cluster to run. The costs are real, though: GIN index maintenance on hot write paths, ranking limited to ts_rank-style scoring, and an analyzer ecosystem far smaller than Lucene's.

## What Elasticsearch adds, concretely

Elasticsearch is a distributed, inverted-index-first engine: analyzers per field with tokenizers and filters, BM25 relevance scoring with per-field tuning, aggregations for facets and analytics, suggesters and fuzzy matching, and horizontal sharding with near-real-time refresh — a feature surface the database deliberately does not chase. The price is architectural: your data now lives in two places, so you must design the sync (CDC, outbox, or double-write with its consistency caveats), reconcile deletions and updates, and run and monitor a cluster. The trade is worth it when search is the product — catalogs, logs, content platforms — and unjustified when search is a widget on one table, where [[When should you use full-text search instead of LIKE]] already answered the need.

```d2
direction: right
oltp: "OLTP database\nsource of truth" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
sync: "Sync pipeline\nCDC / outbox" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
es: "Elasticsearch\nsearch-optimized copy" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
oltp -> sync -> es```

**Fig. 1.** Adopting Elasticsearch introduces a second store and the sync between them; that pipeline is the true cost of the feature surface.

> [!warning] "Search is slow, add Elasticsearch" skips the diagnosis
> The common failure is adopting a second engine to hide an unindexed database query: a '%term%' scan becomes fast with a trigram or FTS index at a fraction of the operational cost, per [[How do you optimize substring search in SQL]]. Conversely, PostgreSQL FTS at genuine scale (hundreds of millions of documents, heavy concurrent search) hits planner and maintenance walls that Elasticsearch's architecture exists for. Decide from measured query profiles and data volume, not from fashion.

> [!tip] Interview answer
> I keep search in SQL when the corpus fits, consistency with the transactional data matters, and ranking needs are modest — GIN-indexed tsvector plus trigram covers a lot. I move to Elasticsearch when search is a core product surface: BM25 relevance tuning, facets, fuzzy and suggester features, and horizontal scale with high ingest. The deciding cost is the sync pipeline and second store, so I need the feature surface to justify it.
