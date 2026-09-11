<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you optimize ORDER BY with a filter?

> [!abstract] Short answer
> Combine the filter and the sort into **one composite index**: equality predicates as the leading columns, ORDER BY columns as the trailing ones. `WHERE category = 'books' ORDER BY price` seeks `(category, price)` once — rows arrive already filtered and ordered, no separate filter pass, no sort. Both the WHERE and the ORDER BY are satisfied by a single key layout ([[How do you avoid a sort with an index]]).

The composite does double duty because of how B-tree keys are laid out: within one `category` value, entries are sorted by `price`, so the equality prefix narrows the search to a contiguous run that is already in output order. The verified demo: the single-column `(category)` index forces a post-filter sort (`USE TEMP B-TREE FOR ORDER BY`); the composite `(category, price)` plans as one SEARCH with no sort node. The same principle extends to `LIMIT`: with the composite, `LIMIT 3` reads exactly three index entries — "top-3 cheapest books" becomes a 3-row read instead of "fetch all books, sort, take 3" ([[How does LIMIT interact with ORDER BY and indexes]]). PostgreSQL documents this as the planner dropping both the Filter and Sort nodes when the index provides the constraint and ordering. Design limits to state: equality columns must genuinely be equalities (a range prefix pins the index and the ORDER BY beyond a range column cannot use the index order); DESC ordering rides backward scans; and every composite added for one query is a write-amplification decision — measure the query's frequency first ([[How do you optimize ORDER BY with a filter]], [[What is the difference between Nested Loop Hash Join and Merge Join]]).

```sql
CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT, category TEXT, price NUMERIC);
CREATE INDEX idx_cat_price ON products(category, price);

EXPLAIN QUERY PLAN
SELECT title FROM products WHERE category = 'books' ORDER BY price;
-- QUERY PLAN
-- `--SEARCH products USING INDEX idx_cat_price (category=?)
EXPLAIN QUERY PLAN
SELECT title FROM products WHERE category = 'books' ORDER BY price DESC LIMIT 3;
-- QUERY PLAN
-- `--SEARCH products USING INDEX idx_cat_price (category=?)
```

**Listing 1.** Verified on SQLite 3.53.1. Ascending and descending top-N variants both plan as a single index seek — the equality pins the prefix, the order rides the tail, and LIMIT reads only the first (or last, backward) entries.

```d2
direction: right
k: "index key (category, price)
books|5, books|30, books|35 ..." {width: 280; height: 70}
w: "WHERE pins category
one contiguous run" {width: 190; height: 80}
s: "run is price-sorted
LIMIT reads its edge" {width: 200; height: 80}
k -> w -> s
```

**Fig. 1.** The composite key's layout is the query's shape: filter and order are two readings of the same sorted run, and LIMIT is just where you stop walking it.

> [!warning] A range predicate before the ORDER BY column breaks the trick
> `WHERE price > 10 ORDER BY price` works (same column), but `WHERE price > 10 ORDER BY title` on `(price, title)` cannot use the index order — the range makes titles unordered within the matched set. Equality columns first, range last, ORDER BY in between only when equalities pin them ([[What is sargability in SQL]]).

> [!tip] Interview answer
> Filtering and ordering merge into one composite index: equality conditions as leading columns, ORDER BY columns as trailing ones — the equality pins a contiguous run that is already in the required order, so the plan is a single seek with no filter pass and no sort. With LIMIT it reads only the first entries of that run, backward for DESC. The caveat I name: a range predicate before the sort column breaks the ordering, and every such index is a write cost I justify by query frequency.
