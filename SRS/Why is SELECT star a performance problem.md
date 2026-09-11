<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# Why is SELECT star a performance problem

> [!abstract] Short answer
> SELECT * forces every column to be fetched, which disables index-only scans, widens rows beyond what the query needs, drags TOASTed or off-page values into memory, and couples application code to schema changes. Explicit column lists let the engine use the narrowest access path — often a covering index — and keep the plan stable as the schema grows.

## The index-only scan you silently lose

PostgreSQL can answer a query entirely from an index when the index contains every referenced column — the index-only scan, which skips the heap visit per row (subject to the visibility map). With SELECT *, the reference set is all columns, so no B-tree index can cover it and every row requires a heap fetch: the plan degrades from index-only scan to plain index scan or worse. The docs' covering-index guidance exists exactly for the fixed-column case — add the payload columns with INCLUDE and the query becomes heap-free, per [[How would you explain Covering index]]; SELECT * optically guarantees the optimization never fires. SQL Server's included-columns design serves the same pattern.

```sql
-- covering possible, but SELECT * forbids it
CREATE INDEX idx_orders_cust ON orders (customer_id) INCLUDE (total, created_at);

SELECT total, created_at FROM orders WHERE customer_id = 42;
-- Index Only Scan: answers from the index, no heap visits
```

**Listing 1.** The named columns make the covering index usable; the star version would fetch the full row for every match.

## The costs that survive even without covering

Wide rows mean more I/O and memory for data the caller discards — over a network that is pure waste, and inside the engine it evicts useful pages from cache. Large values (TEXT, JSONB, BYTEA) often live out-of-line in TOAST or overflow pages: SELECT * triggers detoasting work per row even though the consumer ignores those fields, while named columns keep the heavy attributes untouched. On the operational side, SELECT * breaks application assumptions when the schema evolves — new columns change wire formats and ORMs' expectations — and it obscures intent, making the covering analysis in [[How do you decide which database indexes to create]] impossible. It also interacts with join plans: wider intermediate rows change hash/merge costs, per [[What is the difference between Nested Loop Hash Join and Merge Join]], and make scans of large tables proportionally more expensive per [[When is a full table scan cheaper than using an index]].

> [!warning] "SELECT * is fine because the driver ignores extra columns" is wrong at the engine level
> The database, not the driver, materializes the row: extra columns are read from pages, potentially detoasted, and shipped — the cost is paid before the application drops them. The acceptable exception worth naming: ad hoc interactive queries and EXISTS-style probes where the row is never consumed; there the star is harmless. The other half-myth: naming columns helps only if the narrower set actually enables a narrower path — naming forty columns still cannot use a three-column covering index.

> [!tip] Interview answer
> SELECT * forces the widest possible reference set, which kills index-only scans — no index covers all columns — widens every fetch beyond what the caller needs, and pulls TOASTed heavy values for nothing. Named columns let me design covering indexes with INCLUDE and keep plans stable as the schema grows. For ad hoc exploration it is harmless; in application code it is a measurable performance and coupling problem.
