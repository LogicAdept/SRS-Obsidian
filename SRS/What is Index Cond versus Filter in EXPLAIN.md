<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> **Index Cond** is the predicate applied *inside* an index seek — the condition that narrowed the B-tree range. **Filter** (PostgreSQL: `Rows Removed by Filter`; SQLite shows a plain FILTER row or just counts) is everything checked *after* fetching the row: conditions the index could not serve. The ratio between them is the selectivity of your index design.

SQLite makes the distinction mechanical: `SEARCH ... USING INDEX idx (amount=?)` means the equality drove the B-tree descent; additional predicates on columns not in the index are evaluated per fetched row afterwards. The demo: `WHERE amount = 25 AND customer_id = 3` — the index serves `amount` only; two rows pass the index condition, one survives the post-fetch filter. PostgreSQL's EXPLAIN shows the same boundary as `Index Cond:` versus `Filter:` line items, and with ANALYZE adds `Rows Removed by Filter: N` — the number of rows the index fetched and threw away. That number is the cost of an incomplete index: an index condition matching 2 of 10 rows is a great seek; one matching 2 of 1,000,000 rows is a seek followed by a near-full table read. The design conclusions follow directly: extend the index with the filtered column (composite or INCLUDE), or accept the filter cost when the predicate is rare or too low-cardinality to index ([[What is sargability in SQL]], [[How do you optimize a search query over several columns]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
CREATE INDEX idx_amount ON orders(amount);
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),
 (105,3,300),(107,4,25),(108,3,25),(109,5,150),(110,5,150);

EXPLAIN QUERY PLAN SELECT * FROM orders WHERE amount = 25 AND customer_id = 3;
-- QUERY PLAN
-- `--SEARCH orders USING INDEX idx_amount (amount=?)
SELECT COUNT(*) FROM orders WHERE amount = 25;
-- 2
SELECT COUNT(*) FROM orders WHERE amount = 25 AND customer_id = 3;
-- 1
```

**Listing 1.** Verified on SQLite 3.53.1. The index condition is `amount=?` only; `customer_id = 3` is the post-fetch filter — 2 rows fetched by the index, 1 survives. PostgreSQL would print `Index Cond: (amount = 25)` and `Filter: (customer_id = 3)`.

```d2
direction: right
i: "Index Cond
narrows B-tree range
amount = 25" {width: 220; height: 80}
f: "Filter
checked per fetched row
customer_id = 3" {width: 230; height: 80}
r: "2 fetched -> 1 survives" {width: 210; height: 70}
i -> f -> r
```

**Fig. 1.** The index condition shrinks the search space; the filter discards fetched rows that other predicates reject — work the index could have avoided with a wider key.

> [!warning] A selective Index Cond followed by a huge Filter means the wrong column leads the index
> If `Rows Removed by Filter` dwarfs the output, the fix is index design: put the more selective predicate's column first, add the filtered columns as trailing keys or INCLUDEs, or drop the index — a seek that fetches half the table is a scan with extra steps ([[What is Index Cond versus Filter in EXPLAIN]], [[How do you optimize a search query over several columns]]).

> [!tip] Interview answer
> Index Cond is the predicate the index itself evaluated to pick the range; Filter runs after rows are fetched, for conditions the index could not serve. PostgreSQL names both in EXPLAIN and counts removed rows; SQLite shows SEARCH with the served columns. The number to watch is rows removed by filter — if the index fetches a thousand rows to return one, the index leads with the wrong column and I extend it into a composite key instead of accepting the waste.
