<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SystemDesign/Performance #SRS

# Why is denormalization recommended in ClickHouse?

> [!abstract] Short answer
> Joins are the most expensive relational operation for a distributed columnar engine: they shuffle data across threads and shards at query time. ClickHouse therefore encourages flattened, denormalized tables — related rows stored as arrays, nested structures, JSON, or pre-joined wide rows — so that hot queries scan one sorted table instead of joining several, moving join cost from every query to insert time.

## The reasoning

Denormalization "reverses the normalization process": data that a normalized schema would split across parent-child tables is stored together — comments as an array of objects on the post row, dimension attributes copied onto the fact row — "effectively moving joins from query time to insert time." Reads on wide, denormalized tables hit one column stream set, prune with one sort key, and aggregate without shuffle; the price is write-side complexity: duplicated attributes must be refreshed deliberately (via ReplacingMergeTree upserts, [[What are mutations in ClickHouse]] batch corrections, or re-ingestion), and storage grows with redundancy — usually acceptable because columnar compression ([[How does ClickHouse compress data]]) shrinks repeated values dramatically.

```sql
-- normalized: query-time join per dashboard view
SELECT p.title, count() AS views
FROM posts p JOIN users u ON p.author_id = u.id
WHERE u.country = 'DE' GROUP BY p.title;

-- denormalized: country stored on the event row
SELECT title, count() AS views
FROM post_views_denorm
WHERE country = 'DE' GROUP BY title;
```

**Listing 1.** The join disappears from the read path because the dimension attribute was flattened onto events at insert.

## The toolkit and its limits

Arrays and [[What is ARRAY JOIN in ClickHouse]] (plus Nested structures — [[How do you search Map or Nested fields in ClickHouse]]) store one-to-many children inline; materialized views ([[How do materialized views work in ClickHouse]]) maintain aggregates so "wide" means pre-summarized; dictionaries ([[What is a ClickHouse dictionary]]) serve the remaining point lookups without JOINs; and projections ([[What are projections in ClickHouse]]) pre-sort wide tables per query shape. When JOINs are genuinely needed, hash joins over small right sides or co-located sharding keep them sane — the anti-pattern is large ad-hoc joins across sharded tables at dashboard frequency. This design stance is shared with the serving-oriented OLAP engines ([[What is the difference between ClickHouse Druid and Pinot]]), and it is the analytical mirror of normalization discipline in OLTP systems like PostgreSQL ([[What is the difference between PostgreSQL and ClickHouse]]).

> [!warning] Denormalization is a read-path bet, not a default schema style
> Duplicated attributes can drift from their source: a user's country changes and a billion event rows keep the old value until corrected by design (append newer versions via [[What is ReplacingMergeTree]] and read with [[What is FINAL in ClickHouse]]), not by accident. Denormalize the attributes your queries actually filter and group by; flattening everything produces unmaintainable wide tables whose refresh cost exceeds the join cost you removed.

> [!tip] Interview answer
> Because query-time joins shuffle data that columnar scans aggregate for free, ClickHouse favors moving the join to insert time: store events with dimension attributes inlined, children as arrays or Nested, aggregates in materialized views, and point lookups in dictionaries. Redundancy is cheap under columnar compression; the cost shifts to write-path consistency, which versioned engines and deliberate refreshes handle.
