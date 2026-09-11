<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you optimize COUNT star on a large table?

> [!abstract] Short answer
> `COUNT(*)` is an O(N) walk in MVCC engines — there is no cached row count, because concurrent transactions make "the count" a function of the *snapshot*, not the table. Optimizations: keep the count on a **covering index** (smallest index wins — SQLite plans `SCAN ... USING COVERING INDEX`), accept **approximate** counts from catalog statistics (PostgreSQL `pg_class.reltuples`), or **maintain** the count yourself (counter table / cached value) when exact real-time counts are a business requirement ([[What is the difference between COUNT star and COUNT of a column]]).

Why no shortcut exists, told precisely: in PostgreSQL every row carries visibility metadata (xmin/xmax), so "how many rows exist for *me*" requires checking each row's visibility against the snapshot — the documentation's MVCC model forbids a stored total. SQLite is not MVCC but still scans: its verified plan shows COUNT(*) choosing the **smallest covering index** rather than the table — after `CREATE INDEX`, the plan switches from `SCAN order_items` to `SCAN order_items USING COVERING INDEX idx_oi_order`, reading only the narrow index. The three-step interview answer: (1) exact, cheap, real-time — pick two; (2) exact and real-time means maintaining the counter yourself (with transactional consistency costs); (3) approximate is usually fine for dashboards — `reltuples` from catalog stats costs nothing and is what most "row count" UIs actually need ([[How do stale statistics hurt a query plan]]). The anti-pattern: `SELECT COUNT(*) FROM t` inside a loop or per-request for a paginated total on a 100M-row table — that is a linear scan per page view ([[Why is OFFSET pagination slow]]).

```sql
CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, qty INTEGER, price NUMERIC);
INSERT INTO order_items VALUES (101,5,2,5.0),(101,1,1,30.0),(102,2,2,10.0);

EXPLAIN QUERY PLAN SELECT COUNT(*) FROM order_items;
-- QUERY PLAN
-- `--SCAN order_items
CREATE INDEX idx_oi_order ON order_items(order_id);
EXPLAIN QUERY PLAN SELECT COUNT(*) FROM order_items;
-- QUERY PLAN
-- `--SCAN order_items USING COVERING INDEX idx_oi_order
```

**Listing 1.** Verified on SQLite 3.53.1. COUNT(*) walks the narrowest available structure: no index means the whole table; a covering index shrinks the walk to the index pages — same exact result, fraction of the I/O.

```d2
direction: right
e1: "exact + indexed scan
covering index, O(N) but narrow" {width: 260; height: 80}
e2: "approximate
catalog stats, O(1)" {width: 190; height: 80}
e3: "maintained counter
exact, O(1), write cost" {width: 230; height: 80}
q: "COUNT(*) on big table — choose per requirement" {width: 300; height: 70}
e1 -> q
e2 -> q
e3 -> q
```

**Fig. 1.** Three honest strategies: make the exact scan narrow, make the answer approximate, or move the cost to writes — the impossible corner is exact and instant and free.

> [!warning] Approximate counts lie by design — say so in the product
> `reltuples`-style numbers can be off by minutes of churn; using them for "you have 3 items in your cart" breaks correctness guarantees while being fine for analytics tiles. The requirement ("exact? real-time? free?") decides the method, not the other way round ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> COUNT(*) on a big table is a linear walk because MVCC visibility means the count depends on the snapshot — there is nothing to cache. My options: keep the exact count on the smallest covering index, which SQLite plans explicitly and PostgreSQL does via index-only scans; take the approximate count from catalog statistics like reltuples, which is usually enough for dashboards; or maintain an exact counter table when the product needs real-time totals. Exact, instant and free do not all come together — I ask which two are required.
