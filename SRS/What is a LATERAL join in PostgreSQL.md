<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS

# What is a LATERAL join in PostgreSQL?

> [!abstract] Short answer
> LATERAL lets a subquery in FROM reference columns of FROM items that appear before it — a parameterized left-to-right dependency, like a for-each loop in SQL. JOIN LATERAL re-computes the subquery per row of the left side; it powers per-row top-N, table-function calls, and correlated computations that subqueries in the SELECT list cannot express efficiently.

## The dependency direction

Normally a FROM item cannot see the others; LATERAL lifts that ban for items to its left. The right side may then use left-side columns — so the planner can drive it with an index lookup per left row (a nested-loop with a parameterized inner index scan).

```sql
SELECT c.id, top.total, top.created_at
FROM customers c
JOIN LATERAL (
  SELECT o.total, o.created_at
  FROM orders o
  WHERE o.customer_id = c.id          -- references the left side
  ORDER BY o.created_at DESC
  LIMIT 3                             -- per-customer top-3
) top ON true;
```

**Listing 1.** The signature use: top-N per row. With an index on (customer_id, created_at DESC) each lateral execution is a cheap index peek, and the whole query streams ([[How do you avoid a sort with an index]]).

```d2
left: "Left rows\ncustomers" {width: 220; height: 70}
lat: "LATERAL subquery\nre-planned per row\nuses c.id" {width: 280; height: 80}
res: "Join result\n0..N rows per left row" {width: 300; height: 70}
left -> lat: "one execution per row"
lat -> res
```

**Fig. 1.** Semantics of a correlated nested loop expressed in plain FROM syntax.

## What it replaces and enables

- Replaces the "window function filter" idiom for top-N ([[What are window functions in PostgreSQL]]) when an index can drive it — often cheaper because it touches exactly N rows per group instead of ranking all rows.
- Enables calling set-returning functions per row: `JOIN LATERAL jsonb_to_recordset(payload) AS t(k text) ON true`.
- Works with LEFT JOIN LATERAL ... ON true as "if the subquery is empty, keep the left row" — the lookup-with-defaults pattern.
- Correlated subqueries in SELECT have the same dependency but can only return one value; LATERAL returns a whole rowset to join ([[What is a correlated subquery and why can it be slow]] — LATERAL is often the fast rewrite).

> [!warning] LATERAL multiplies: watch the cardinality
> A lateral subquery without LIMIT against a big left side is a correlated join in disguise — the per-row cost times the left cardinality. The plan node to expect is Nested Loop with a parameterized inner index scan; if you see a materialized subplan or a seq scan inside the lateral for every row, the index that should drive it is missing ([[Why might PostgreSQL choose a sequential scan instead of an index]]).

> [!tip] Interview answer
> LATERAL makes a FROM subquery see the columns of preceding FROM items — a per-row parameterized join. It is the idiomatic top-N-per-group with index-driven nested loops, the way to call set-returning functions per row, and LEFT JOIN LATERAL ON true gives lookup-with-default. Think for-each in SQL, priced as a nested loop.
