<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> The optimization catalog, in the order they pay off: (1) **index** the predicate and join columns — the largest single win; (2) **make predicates sargable** so those indexes get used; (3) **refresh statistics** so the planner chooses correctly; (4) **shape the query** — semi-joins over DISTINCT-bandages, pre-aggregation, LIMIT with supporting index, keyset pagination; (5) **reduce data movement** — select needed columns, batch N+1s. Each is verified by a plan change, not by faith ([[What is sargability in SQL]], [[How do you systematically diagnose a slow SQL query]]).

The verified demo is the smallest complete story of the catalog: `WHERE customer_id = 3` without an index plans as a table `SCAN`; after `CREATE INDEX idx_o_cust ON orders(customer_id)` it is `SEARCH ... USING INDEX idx_o_cust (customer_id=?)` — one statement, one plan change, order-of-magnitude consequences at real table sizes. Every catalog item follows the same evidence pattern (before-plan, after-plan): sargability fixes turn scans back into seeks when an index exists but the predicate computes on the column ([[Why does a function on a column prevent index use]]); statistics refresh fixes estimate-driven join-order mistakes ([[How do stale statistics hurt a query plan]]); query shaping replaces multiplied-join-plus-DISTINCT with EXISTS ([[Why is SELECT DISTINCT expensive]]) and replaces OFFSET walks with keyset seeks ([[Why is OFFSET pagination slow]]). What the catalog deliberately omits: hardware and tuning knobs — they multiply the current plan's efficiency but cannot fix a wrong access path; plan-first, knobs-last is the senior ordering. The catalog is also bounded: an index for a once-a-year report is a write tax with no reader — frequency justifies each item ([[How do you optimize COUNT star on a large table]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),
 (105,3,300),(107,4,25),(108,3,25),(109,5,150),(110,5,150);

EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 3;
-- QUERY PLAN
-- `--SCAN orders
CREATE INDEX idx_o_cust ON orders(customer_id);
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 3;
-- QUERY PLAN
-- `--SEARCH orders USING INDEX idx_o_cust (customer_id=?)
```

**Listing 1.** Verified on SQLite 3.53.1. The canonical before/after: full table read versus B-tree descent to the matching rows. Every other catalog item is this same experiment with different vocabulary.

```d2
direction: right
o1: "index the hot predicates" {width: 220; height: 70}
o2: "keep predicates sargable" {width: 210; height: 70}
o3: "statistics fresh" {width: 170; height: 70}
o4: "shape: semi-join, pre-aggregate, keyset" {width: 250; height: 70}
o5: "move less data: columns, batches" {width: 230; height: 70}
o1 -> o2 -> o3 -> o4 -> o5
```

**Fig. 1.** The catalog is an ordered pipeline: make the access path right, then the estimates right, then the query shape right — each layer assumes the previous one.

> [!warning] Each optimization has a write-side price and a failure mode
> Indexes slow writes and clutter plans when unused; statistics refreshes cost I/O; denormalized counters drift. The senior move is not maximizing the catalog but *justifying* each item with the query's frequency and verifying the plan actually changed ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> My ordered catalog: index the hot predicate and join columns first — the biggest single lever; keep predicates sargable so those indexes are actually used; keep statistics fresh so the planner chooses well; then shape queries — EXISTS over DISTINCT bandages, pre-aggregate before joins, keyset over OFFSET pagination; and finally move less data — named columns, batched N+1s. Every item is proven by a before/after plan change, and each has a write-side cost justified by query frequency.
