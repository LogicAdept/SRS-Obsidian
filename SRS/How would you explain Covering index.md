<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes/Covering #Databases/Indexes/Composite #SRS

# How would you explain Covering index?

> [!abstract] Short answer
> A covering index is an index that contains every column a query needs, so the engine answers it without touching the table at all — in PostgreSQL that means an Index Only Scan. You get coverage either by putting the columns in the composite key or, since PostgreSQL 11, by attaching them with the INCLUDE clause as leaf payload.

## The concept

The point of a covering index is not faster lookup of the matching rows — any index does that — but eliminating the second lookup: the random heap visit per row. For a query returning few columns over many rows, skipping the heap is often an order-of-magnitude win, limited by how well the visibility map marks pages all-visible ([[What is an index-only scan in PostgreSQL]]).

```sql
-- query: SELECT status, total FROM orders WHERE customer_id = 42;
CREATE INDEX orders_cust_covering ON orders (customer_id) INCLUDE (status, total);
```

**Listing 1.** `customer_id` is the key (searched), `status` and `total` ride along as INCLUDE payload (returned) — the mechanics are in [[What is the difference between a composite index and an INCLUDE covering index]].

```d2
q: "Query needs\ncustomer_id, status, total" {width: 280; height: 80}
idx: "Index (customer_id) INCLUDE (status, total)" {width: 340; height: 70}
ios: "Index Only Scan\n0 heap visits when pages all-visible" {width: 340; height: 80}
heap: "Heap: not visited" {width: 200; height: 60}
q -> idx -> ios
ios -> heap: "skipped"
```

**Fig. 1.** Coverage is about the SELECT list as much as the WHERE clause.

## Engineering the coverage

1. Look at the query shape: equality key first, then what the SELECT returns.
2. Decide key versus INCLUDE by whether the column filters, sorts, or is only returned.
3. Mind the visibility map: fresh writes destroy index-only-ness until vacuum ([[What is autovacuum in PostgreSQL]]).
4. Mind the write cost: every covered column widens the index on every insert and relevant update.

In planning terms, coverage interacts with everything else in [[How do you decide which database indexes to create]]; for search-heavy workloads a similar "cover the query shape" logic appears in [[How do you design indexes for a search API]].

## When not to bother

- The query returns many columns or wide text: the index becomes a second copy of the table ([[What goes wrong with indexing every field combination for flexible search]]).
- The table is write-hot and pages are rarely all-visible: Heap Fetches make the coverage theoretical ([[What is Heap Fetches in an EXPLAIN plan]]).
- The query is rare: an extra index costs every write for one report.

> [!warning] "Covering" is not a PostgreSQL index type
> There is no `USING covering` syntax; it is a property a B-tree (or GiST with INCLUDE) acquires. Saying "create a covering index" is fine as intent, but the real decision is which columns are keys and which are INCLUDE — and whether the planner will actually produce an Index Only Scan. Check with EXPLAIN, not with hope ([[How do you read EXPLAIN ANALYZE in PostgreSQL]]).

> [!tip] Interview answer
> A covering index has everything the query needs, so PostgreSQL can serve it with an Index Only Scan and skip the heap: keys for search, INCLUDE columns for the SELECT list, visible only on all-visible pages. It trades write amplification for read speed — measure Heap Fetches and index size before and after.
