<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #Databases/SQL #SystemDesign/Tradeoffs #SRS

# What is database denormalization for?

> [!abstract] Short answer
> Denormalization deliberately reintroduces redundancy — copied attributes, precomputed aggregates, flattened one-to-many structures — to buy read performance and simpler queries: joins that a normalized schema would run on every read move to insert or refresh time. It is a trade, not an upgrade: writes get more expensive and the engine no longer keeps the copies consistent for you, so every denormalized field needs a maintenance story ([[How many normal forms are commonly taught for relational databases]]).

## What normalization prevents, and what denormalization trades back

Normalization splits data across tables to minimize redundancy and the update anomalies that come with it — that is the discipline the normal forms encode. ClickHouse's denormalization guide describes the reverse move precisely: "denormalizing data involves intentionally reversing the normalization process", combining tables and duplicating data — "effectively moving any joins from query to insert time", which "reduces the need for complex joins at query time and can significantly speed up read operations". The bill arrives on the write side: the same guide warns that "a change in one source row potentially means many rows in ClickHouse need to be updated" — in composed schemas, "millions". The trade is not OLAP-specific: OLTP schemas denormalize selectively too, via materialized views that precompute and refresh aggregate or joined tables ([[How would you explain MATERIALIZED VIEW]], [[How would you explain VIEW vs MATERIALIZED VIEW]]), and via cache columns maintained by triggers or batch jobs. The analytical extreme of the same trade is [[Why is denormalization recommended in ClickHouse]].

```sql
-- normalized: the country lives only in authors
CREATE TABLE authors (id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE posts_norm (id INTEGER PRIMARY KEY,
  author_id INTEGER REFERENCES authors(id), title TEXT);
-- denormalized: the country is copied onto the read-optimized table
CREATE TABLE posts_denorm (id INTEGER PRIMARY KEY,
  author_country TEXT, title TEXT);

SELECT p.title, a.country FROM posts_norm p
  JOIN authors a ON p.author_id = a.id WHERE a.country = 'DE';
SELECT title, author_country FROM posts_denorm WHERE author_country = 'DE';
-- same rows -- but the second needs no join, one table, one predicate

UPDATE authors SET country = 'FR' WHERE id = 1;
SELECT author_country FROM posts_denorm WHERE id = 100;
-- 'DE'  -- the copy is already stale: sync is now your job
```

**Listing 1.** Verified on SQLite 3.53.1. Both reads return the same data today; the UPDATE proves the cost — the denormalized copy keeps the old value until a trigger, materialized-view refresh, or batch job propagates the change.

```d2
direction: right
n: "normalized
authors + posts
join at read time" {width: 210; height: 80; style.fill: "#e3f2fd"}
d: "denormalized
country copied onto posts" {width: 230; height: 80; style.fill: "#e8f5e9"}
r: "reads: no join,
one predicate, faster" {width: 210; height: 75; style.fill: "#e8f5e9"}
w: "writes: copy country,
then keep it in sync" {width: 220; height: 75; style.fill: "#ffebee"}
n -> d: "denormalize"
d -> r
d -> w
```

**Fig. 1.** Denormalization moves work across the read/write boundary: reads shed the join, writes acquire the copy plus the sync obligation — the arrow that ends in red is the price.

## When the trade pays

Denormalization pays when reads dominate and the normalized join is on the hot path: dashboards over wide fact tables, API responses that need one shape, aggregates recomputed on every page view. It loses when the underlying attribute changes often (the sync cost scales with churn), when storage multiplies beyond budget, or when consistency between copies is contractual rather than eventual — a domain where the normalized form keeps the engine doing the enforcement ([[What harmful SQL patterns or pitfalls do you know]] collects the failure shapes). The practical sequence in interviews and in code reviews alike: normalize first, measure the real query, then denormalize the specific hot path — with the refresh mechanism named before the copy is created.

> [!warning] A denormalized copy without a named refresh mechanism is a bug on a timer
> The verified listing showed the copy going stale after one UPDATE; in production the stale window is the design. Materialized views refresh on a schedule or on demand, triggers propagate inline at write cost, batch jobs reconcile eventually — each is a legitimate answer, and "we will remember to update it" is not. If no mechanism fits the churn rate, the attribute should stay normalized.

> [!tip] Interview answer
> Denormalization is buying read speed with redundancy: copies, aggregates and flattened structures remove joins and precompute answers, moving that cost to write and refresh time. I name the price before the benefit — slower writes, storage growth, and a sync obligation, because the engine stops keeping copies consistent for me. Normalize first, measure, then denormalize the hot path with the refresh mechanism (materialized view, trigger, or batch) chosen deliberately — that is the whole trade in one sentence.

