<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `SELECT *` moves every column's bytes even when the consumer needs three; it **defeats covering indexes** (any column outside the index forces the table row fetch); it fetches large values (TEXT/BLOB) nobody displays; and it couples the query to the schema — adding a column silently changes every `*` consumer. The plan-level proof: the same query with and without the wide projection plans as covering-index scan versus table scan ([[How do you identify slow or non-performant SQL queries]]).

The verified demo isolates the covering-index mechanism on SQLite: with an index on `amount`, `SELECT amount FROM orders` plans as `SCAN orders USING COVERING INDEX idx_amount` — the answer comes from the index structure alone; `SELECT *` plans as a plain `SCAN orders` — every row must be fetched from the table because the rest of the columns exist nowhere else. PostgreSQL documents the same mechanism as index-only scans with the visibility-map caveat, and names the enabling condition: the query's columns must all be in the index. Beyond plans, the costs are concrete: width multiplies network and memory (a 40-column row for a 3-column report is a 13x data tax), ORM row-materialization cost scales with column count, and large-object columns travel whether or not anyone reads them. The coupling cost is the operational one: `SELECT *` into a logger or cache silently changes behavior when the schema evolves ([[What harmful SQL patterns or pitfalls do you know]]). The fair exception: ad-hoc interactive inspection and genuinely whole-row consumers (ETL staging) — the rule is a default, not a dogma ([[Why is SELECT DISTINCT expensive]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
CREATE INDEX idx_amount ON orders(amount);

EXPLAIN QUERY PLAN SELECT amount FROM orders;
-- QUERY PLAN
-- `--SCAN orders USING COVERING INDEX idx_amount
EXPLAIN QUERY PLAN SELECT * FROM orders;
-- QUERY PLAN
-- `--SCAN orders
```

**Listing 1.** Verified on SQLite 3.53.1. The narrow projection reads the answer from the index itself; `SELECT *` must visit every table row because the remaining columns exist only there — one SELECT-list token, two different data paths.

```d2
direction: right
q1: "SELECT amount
-> covering index only" {width: 220; height: 80}
q2: "SELECT *
-> index + table row per hit" {width: 230; height: 80}
c1: "narrow I/O, schema-agnostic consumer" {width: 250; height: 80}
c2: "wide I/O, byte tax, schema coupling" {width: 250; height: 80}
q1 -> c1
q2 -> c2
```

**Fig. 1.** The projection list decides the data path: covered columns live in the index; the asterisk drags the whole row across the boundary every time.

> [!warning] The asterisk also changes application behavior on schema evolution
> Column order, width and types shift under `*`-consumers when a column is added or reordered — position-based consumers (old JDBC accessors, CSV exports) break or corrupt silently. Named columns are a contract; the asterisk is an open bet ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> SELECT star is a performance problem because it moves every column and defeats covering indexes: my demo shows the same query planning as a covering-index scan for one column versus a full table walk for the star, and on PostgreSQL it is exactly the index-only scan precondition. Add the width tax on the wire, big columns nobody reads, ORM materialization cost, and silent schema coupling for positional consumers. I default to named columns and treat star as an interactive-inspection tool, not application code.
