<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# When should you use Elasticsearch instead of SQL search?

> [!abstract] Short answer
> Reach for Elasticsearch (or similar search engines) when the requirements leave SQL's search model: *relevance-ranked* results, *fuzzy* matching (typos, edit distance), *analytical aggregations* over text (facets, histograms), horizontal scaling of search-specific load, and rich text analysis (stemming, synonyms, custom analyzers). Stay in SQL when the query is exact, structured, transactional, or small — B-tree seeks, FTS, and trigram indexes cover a vast middle ground natively ([[How does a trigram index help SQL search]], [[When should you use full-text search instead of LIKE]]).

The verified demo shows SQL's search *ceiling* — the point where SQL says "this is what I have": FTS5's bm25 ranking is real relevance ordering over an inverted index, and the same query supports boolean composition — but everything beyond (edit-distance tolerance, per-field boosts tuned by hand, synonym dictionaries, aggregation pipelines over search results) is outside SQL's contract. The cost side is why "always Elasticsearch" is an anti-answer: a second datastore with its own storage, memory, and failure modes; an indexing pipeline whose lag and consistency must be designed (document freshness, sync failures, reindex strategies); and a second query language where joins and transactions do not exist — the source of truth remains the relational database, and every answer Elasticsearch gives is as good as its last sync ([[What harmful SQL patterns or pitfalls do you know]]). The senior formulation: SQL keeps truth and serves exact/structured access; the search engine serves fuzzy/relevance/aggregation-heavy access; the boundary is a product decision, not a performance fashion — and the same BM25 machinery inside the database (FTS) often delays the boundary crossing by years ([[How do you optimize COUNT star on a large table]]).

```sql
CREATE VIRTUAL TABLE articles USING fts5(title, body);
INSERT INTO articles VALUES ('SQL', 'sql sql sql basics'),
 ('Java', 'java and sql integration'),
 ('Cookbook', 'pasta and sauces');

SELECT title, bm25(articles) AS score FROM articles
WHERE articles MATCH 'sql' ORDER BY score;
-- SQL|-1.6716417910447762e-06
-- Java|-9.71608832807571e-07
-- (SQL's ceiling: inverted-index token search WITH relevance ranking.
--  Beyond this -- fuzzy typo matching, synonym-aware scoring, search-side
--  aggregations at horizontal scale -- is the search engine's territory.)
```

**Listing 1.** Verified on SQLite 3.53.1 (FTS5). Ranked token search inside SQL — everything above this line (fuzzy, synonyms, search-analytics at scale) is what a dedicated engine buys, at the price of a second system to keep in sync.

```d2
direction: right
s: "structured / exact /
transactional queries" {width: 220; height: 90}
d: "relevance, fuzzy,
facets, text analytics" {width: 210; height: 90}
sq: "SQL
B-tree, FTS, trigram
source of truth" {width: 200; height: 90}
es: "search engine
index pipeline,
no joins/transactions" {width: 210; height: 90}
s -> sq
d -> es
```

**Fig. 1.** The workload splits by query nature: exact and transactional stay where truth lives; fuzzy and analytical search cross to the engine — along with a sync pipeline.

> [!warning] The search engine's answers are only as fresh as its index — and it cannot join
> "Deleted the product but search still shows it" is an indexing-lag story; "cannot filter by user permission" is a no-joins story. Design the sync (events, dual writes, periodic reindex) and resolve permissions against the relational store before promising features ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> I move to Elasticsearch when the requirements leave SQL's model: relevance ranking users tune, fuzzy matching over typos, synonym handling, search-side aggregations like facets, and horizontal scaling of search load. I stay in SQL for exact, structured, transactional queries — B-trees, FTS and trigram indexes cover a lot; my demo shows ranked BM25 search inside SQL, which is the ceiling before the engine earns its keep. The costs I always name: a second datastore, an indexing pipeline with lag, no joins or transactions — so the relational store stays the source of truth and permissions resolver.
