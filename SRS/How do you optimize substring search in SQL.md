<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# How do you optimize substring search in SQL

> [!abstract] Short answer
> Pick the structure that indexes substrings or tokens: pg_trgm with a GIN/GiST index for '%like%' and similarity queries, PostgreSQL full-text search with a tsvector GIN index for word-level matching with stemming and ranking, or an external search engine when relevance, scale, or ranking outgrow the database. A plain B-tree cannot help '%term%' at all.

## pg_trgm: trigrams over arbitrary substrings

pg_trgm splits strings into three-character groups (padding each word with spaces, ignoring non-alphanumerics) and indexes them with GIN or GiST, which makes LIKE, ILIKE, and similarity operators seekable for contains-style patterns. The module's docs define the trigram model and its index support explicitly: GIN for read-heavy (faster lookups), GiST for write-heavy (faster updates), with `gin_trgm_ops`/`gist_trgm_ops` in the DDL. Thresholds are settable (pg_trgm.similarity_threshold drives the % operator). This is the standard fix when a dashboard filter became '%term%' and the plan went to a seq scan.

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_products_name_trgm
    ON products USING gin (name gin_trgm_ops);
SELECT * FROM products WHERE name ILIKE '%wrench%';
```

**Listing 1.** After the trigram GIN index, ILIKE '%wrench%' reads candidate rows via the index instead of scanning the table.

## Full-text search and the external-engine boundary

When the search unit is a word or phrase — documents, descriptions, logs with terms — tsvector plus tsquery with a GIN index gives stemming per language configuration, ranking with ts_rank, and boolean composition; the mechanics are in [[How does full-text search work in PostgreSQL]], and the LIKE-versus-FTS decision factors in [[When should you use full-text search instead of LIKE]]. ClickHouse solves the same problem with its text (inverted) index and hasToken-style functions rather than trigrams, as in [[How does ClickHouse accelerate LIKE and substring search]]. The upgrade path to Elasticsearch is a workload decision, not a default, per [[When should you use Elasticsearch instead of SQL search]]. And if the columns are JSON rather than text, the same GIN machinery applies with jsonb_ops, covered in [[How do you search JSON fields efficiently in SQL]].

> [!warning] Trigram indexes are not free and are not FTS
> A trigram GIN index is sizable (every three-character group per row) and slows writes; on very short patterns (one or two characters) it degrades because there are few trigrams to discriminate. It also does not understand language: no stemming, no ranking, no stopwords. Choosing trigram when the requirement is relevance-ranked document search misses the point the same way choosing FTS for exact-code lookup overkill.

> [!tip] Interview answer
> For '%term%' I stop expecting the B-tree and match the structure to the need: pg_trgm GIN or GiST for substring and similarity including ILIKE, full-text search with tsvector and GIN for word-level language queries, and Elasticsearch when ranking or scale demand it. Suffix search gets the reversed-string trick. Cost side matters too: trigram indexes are large and add write overhead, so measure before sprinkling them everywhere.
