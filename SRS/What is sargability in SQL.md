<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is sargability in SQL?

> [!abstract] Short answer
> A predicate is **sargable** (Search ARGument-able) when the engine can apply it directly to an index search: comparisons of a bare indexed column against a constant or parameter (`col = ?`, `col > ?`, `col LIKE 'abc%'`). Wrapping the column in a function or expression (`UPPER(col) = ?`, `col + 1 = ?`) makes it non-sargable — the index is unusable and the plan degrades to a full scan ([[Why does a function on a column prevent index use]]).

The mechanism is structural, not a planner weakness: a B-tree stores keys in order; a seek works by comparing the search key against ordered keys. `WHERE amount = 25` asks "where would 25 be?" — one descent. `WHERE amount + 0 = 25` asks a question about a *computed* value that exists nowhere in the index; the engine cannot navigate to it and must read every row, compute, and test. The verified demo shows the plan flip on identical data: `amount = 25` is `SEARCH ... USING INDEX idx_amount (amount=?)`, `amount + 0 = 25` is `SCAN orders`. Every engine has the same rule with its own folklore version: MySQL calls it sargability, SQL Server "index seek versus scan", PostgreSQL the same. The escape hatches when the query genuinely needs the function: an **expression index** (PostgreSQL `CREATE INDEX ON t(UPPER(col))`, SQLite `CREATE INDEX ON t(substr(name,1,1))` — verified in the demo of the function-on-column card), a generated column that stores the computed value, or rewriting the predicate into range form ([[Why does a function on a column prevent index use]], [[What is sargability in SQL]]).

```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount NUMERIC);
CREATE INDEX idx_amount ON orders(amount);
INSERT INTO orders VALUES (101,1,120),(102,1,80),(103,2,45.5),(104,3,45.5),
 (105,3,300),(107,4,25),(108,3,25),(109,5,150),(110,5,150);

EXPLAIN QUERY PLAN SELECT * FROM orders WHERE amount = 25;
-- QUERY PLAN
-- `--SEARCH orders USING INDEX idx_amount (amount=?)
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE amount + 0 = 25;
-- QUERY PLAN
-- `--SCAN orders
```

**Listing 1.** Verified on SQLite 3.53.1. Adding `+ 0` changes nothing mathematically but changes everything structurally: the predicate now targets a computed value absent from the index, and the SEARCH becomes a SCAN.

```d2
direction: right
b: "B-tree keys
25 25 45.5 45.5 80 ..." {width: 230; height: 70}
s1: "col = 25
seek into ordered keys" {width: 200; height: 80}
s2: "col + 0 = 25
compute per row, test" {width: 210; height: 80}
b -> s1
b -> s2
```

**Fig. 1.** The index can answer questions about stored keys only: a bare-column comparison navigates the tree, a computed comparison forces a row-by-row evaluation.

> [!warning] Sargability is also lost implicitly — by conversion, not just by visible functions
> `WHERE text_col = 12345` (type mismatch), datetime columns truncated with CAST for "date comparison", and string concatenations inside predicates all break seeks without looking like function calls. The checklist: bare column on one side, constant or parameter on the other, types aligned ([[How does implicit type conversion hide an index]], [[Why does LIKE with a leading wildcard not use a B-tree index]]).

> [!tip] Interview answer
> Sargable means the predicate can drive an index search: bare indexed column compared to a constant or parameter. Wrap the column in a function or arithmetic — UPPER(col), col + 1, CAST — and the value being compared exists nowhere in the index, so the plan falls back to a scan; SQLite shows SEARCH becoming SCAN. When the function is genuinely needed I index the expression itself, use a generated column, or rewrite to a range predicate — and I also watch for implicit type conversion, which breaks sargability invisibly.
