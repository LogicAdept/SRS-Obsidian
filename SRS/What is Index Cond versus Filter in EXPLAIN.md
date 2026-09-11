<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #Databases/Relational/PostgreSQL #SRS

# What is Index Cond versus Filter in EXPLAIN?

> [!abstract] Short answer
> `Index Cond` is the part of the WHERE clause the index itself evaluates — it determines which entries are read from the index. `Filter` is a condition evaluated afterwards on each row that came out of the scan. The difference is cost: an index condition prunes work; a filter rejects rows after reading them. `Rows Removed by Filter` quantifies the waste.

## Reading a plan line

```sql
EXPLAIN ANALYZE SELECT * FROM orders
WHERE customer_id = 42 AND total > 100;
-- Index Scan using orders_cust_idx on orders
--   Index Cond: (customer_id = 42)
--   Filter: (total > 100)
--   Rows Removed by Filter: 18422
```

**Listing 1.** Only `customer_id` is in the index; every row of customer 42 is read from the heap and 18422 of them fail the total check. A composite or INCLUDE index on (customer_id, total) would move the work into the Index Cond — [[What is the difference between a composite index and an INCLUDE covering index]].

```d2
cond: "Index Cond\nprunes inside the index:\nno pages read for rejects" {width: 330; height: 90}
filt: "Filter\nreads the row, then rejects\nRows Removed counts it" {width: 320; height: 90}
recheck: "Index Cond: Recheck\nlossy bitmap candidates verified" {width: 330; height: 80}
```

**Fig. 1.** Three evaluation places: inside the index, on the row after it, and the bitmap recheck variant.

## The nuances

- On a Bitmap Heap Scan the index line shows `Index Cond`, and the heap node may show `Rows Removed by Index Recheck` — that is lossy bitmap behavior when work_mem forced page-granular bitmaps ([[What is a bitmap index scan in SQL plans]]).
- `Filter` also appears on Seq Scans — there it is the normal place WHERE runs; the pathology is a huge removed count on an index scan that should have pruned.
- Implicit casts or functions can silently move a condition from Index Cond to Filter ([[How does implicit type conversion hide an index]]).

## Why it matters

The split is the fastest way to see whether an index actually serves a query or just finds rows that another condition then rejects. Where you see persistent `Rows Removed by Filter` in the thousands next to an Index Scan, the fix is usually an index whose key includes the filtering column — or accepting a Seq Scan for low selectivity ([[Why might PostgreSQL choose a sequential scan instead of an index]]).

> [!warning] Index Cond does not include every WHERE term
> Only columns usable by the index operator class appear there; the rest silently degrades to Filter. Plans chosen on estimates can look fine while 99 percent of rows are filtered post-index — the classic "index exists but the query is slow" trap. Always read the removed-rows counters in ANALYZE output ([[How do you read EXPLAIN ANALYZE in PostgreSQL]]).

> [!tip] Interview answer
> Index Cond is evaluated inside the index and prunes entries; Filter is checked on each row after retrieval, and Rows Removed by Filter shows how much work was wasted. When a filter removes thousands of rows after an index scan, the filtering column belongs in the index key or INCLUDE list.
