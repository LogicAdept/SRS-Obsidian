<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A **view** is a stored named query: `CREATE VIEW cheap AS SELECT ...` — no data is stored, and every reference executes the defining query against *current* data. Uses: security (expose a column subset), convenience (name a complex join once), encapsulation (change physical schema behind a stable interface), and compatibility shims during migrations ([[How would you explain VIEW vs MATERIALIZED VIEW]]).

The verified demo demonstrates the defining property: the view reflects an INSERT into its base table immediately — because a view is a macro-like rewrite, not a snapshot; SQLite's documentation states views are "ephemeral" tables materialized fresh at each use, and PostgreSQL's chapter words it the same way. The uses translate directly to production stories. Security: grant SELECT on a view exposing `name, city` but not `salary` — the row-and-column filter is the boundary (PostgreSQL adds row-level security for per-user filters; SQL Server has the same grant-on-view model). Encapsulation: an application reads `v_orders_enriched` while the underlying schema reshapes across migrations — consumers never change. Convenience: naming the standard join once so ten report queries stay consistent. The limits matter as much: views add no performance by themselves (some engines push predicates into the view — SQLite's push-down optimization — but there is no caching), they cannot be indexed directly (index the base tables), and updatable views are engine-limited (simple single-table views auto-updatable; PostgreSQL allows `INSTEAD OF` triggers; complex views are read-only) ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE items (id INTEGER PRIMARY KEY, title TEXT, price NUMERIC);
INSERT INTO items VALUES (1,'a',10),(2,'b',20);
CREATE VIEW cheap AS SELECT title, price FROM items WHERE price < 15;

SELECT * FROM cheap;
-- a|10
INSERT INTO items VALUES (3,'c',12);
SELECT * FROM cheap;
-- a|10
-- c|12
-- (the new row appears instantly: a view runs its query live)
```

**Listing 1.** Verified on SQLite 3.53.1. One insert into the base table, and the view's next execution includes it — the proof that a view stores a query, not rows.

```d2
direction: right
c: "consumer
SELECT * FROM view" {width: 190; height: 80}
v: "view
stored query definition" {width: 200; height: 80}
b: "base tables
current data, indexed" {width: 180; height: 80}
c -> v -> b
```

**Fig. 1.** Every view reference is rewritten to the base query: the view is a named lens over live tables, adding abstraction but no storage.

> [!warning] A view is an API — changing its definition is a schema change
> Consumers bind to the view's column list and semantics; redefining "harmlessly" (adding a column, changing a filter) breaks readers the way a table change would. Version views (v2 alongside v1) during transitions and deprecate explicitly, exactly as with table contracts ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> A view is a stored query with no storage of its own — every use re-runs the definition against current data, which my demo shows by inserting into the base table and seeing the view change. I use views for security boundaries, to name a canonical join once, and to insulate consumers from schema migrations. The limits: no performance of their own, indexes live on base tables, and updatability is limited to simple views unless the engine supports INSTEAD OF triggers — for precomputed, refreshable results there is the materialized view.
