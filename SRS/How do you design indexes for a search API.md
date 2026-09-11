<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SystemDesign/Performance #SRS

# How do you design indexes for a search API

> [!abstract] Short answer
> Enumerate the API's actual filter and sort combinations first, then build one composite index per frequent combination — equality filters in order, sort column last — plus partial indexes for stable hot subsets and a text structure (trigram or full-text) for the search-term parameter. Ad hoc combinations ride bitmap combination or skip scan, not new indexes.

## From endpoints to index shapes

The design input is the API contract, not the table: list the query parameters each endpoint accepts, mark which are equality (status, tenant_id, category), which are ranges (created_at), which is the sort key, and which is free text. The equality-plus-sort pattern becomes a composite with the sort column after the equality prefix, per [[How do you optimize ORDER BY with a filter]]; pagination via cursor needs that sort to be deterministic with a unique tiebreaker, per [[What is keyset pagination]]. The free-text parameter routes to pg_trgm GIN for substring-style search or tsvector GIN for word-level search, per [[How do you optimize substring search in SQL]] and [[When should you use full-text search instead of LIKE]]; rare-but-critical filters (is_deleted, tenant scoping) often fit a partial index, per [[What is a partial index in PostgreSQL]].

```sql
-- endpoint: GET /orders?status=&customer_id=&sort=created_at&page=
CREATE INDEX idx_orders_cust_created
    ON orders (customer_id, created_at DESC) INCLUDE (total);

-- endpoint: GET /orders?status=open (hot subset)
CREATE INDEX idx_orders_open
    ON orders (created_at DESC) WHERE status = 'open';

-- endpoint: GET /products?q=<term>
CREATE INDEX idx_products_name_trgm
    ON products USING gin (name gin_trgm_ops);
```

**Listing 1.** One index per real query shape: equality+sort with payload, partial for the hot status, trigram for the search box.

## The discipline that keeps it sane

Cap the index budget by measured traffic: not every parameter combination deserves an index; the rare ad hoc shapes fall back to bitmap combination of existing indexes, per [[How do you combine several indexes in one query]], or skip scan when a composite's leading column has few distinct values, per [[What is Index Skip Scan]]. Covering decisions follow the endpoint's SELECT list — APIs usually render a fixed column set, which makes INCLUDE design unusually effective — and the write-side cost of every index is paid on every POST/PUT, the budget argument in [[When are database indexes a bad idea]]. Finally, verify per endpoint with real plans and keep the audit loop from [[How do you decide which database indexes to create]]: API workloads shift, and indexes follow traffic, not intentions.

> [!warning] "Add an index for every filterable field" is the API back-end's classic mistake
> Flexible search endpoints accumulate optional parameters; indexing every field and every pair is the combinatorial trap dissected in [[What goes wrong with indexing every field combination for flexible search]]. The subtler failure: forgetting the sort column, so the composite serves the WHERE but the API paginates through a full sort every page — the LIMIT interaction in [[How does LIMIT interact with ORDER BY and indexes]].

> [!tip] Interview answer
> I derive indexes from the API contract: for each endpoint, equality filters become the composite prefix, the sort column goes last with a unique tiebreaker for cursors, stable hot subsets get partial indexes, and the free-text parameter gets a trigram or FTS index. Combinations without dedicated indexes ride bitmap combination or skip scan. Every candidate must be justified by a measured plan, because each index taxes every write.
