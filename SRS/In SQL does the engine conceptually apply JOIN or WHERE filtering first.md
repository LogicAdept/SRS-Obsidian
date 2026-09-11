<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# In SQL does the engine conceptually apply JOIN or WHERE filtering first?

> [!abstract] Short answer
> Conceptually the engine applies **`FROM`/`JOIN` first, then `WHERE`** — joins build the row source, and `WHERE` filters that source afterwards. That is why a filter on the right table of a `LEFT JOIN` behaves differently in `ON` (applied during the join, unmatched left rows survive with `NULL`s) than in `WHERE` (applied after the join, and `NULL`-extended rows are dropped).

Microsoft's published logical processing order puts `FROM` (1), `ON` (2), and `JOIN` (3) ahead of `WHERE` (4). The practical payoff is the outer-join case: a condition belongs in `ON` when it selects *matching partners*, and in `WHERE` when it filters the *joined result*. Inner joins make the placement irrelevant — `ON` plus `WHERE` are logically interchangeable there — so the question is really about outer joins ([[How does LEFT JOIN differ from INNER JOIN in SQL]], [[What is the logical order of SQL SELECT execution]]).

The same "joins first" logic explains two related traps. A `WHERE` filter on the right table's column usually converts your `LEFT JOIN` into an inner join, because `NULL`-extended rows fail any ordinary predicate. And predicates on the *left* table in `ON` do nothing for a `LEFT JOIN` — every left row is kept regardless, so such conditions only select which right rows match.

```sql
CREATE TABLE emp (id INTEGER, name TEXT, dept_id INTEGER);
CREATE TABLE dept (id INTEGER, name TEXT);
INSERT INTO emp VALUES (1,'Ada',1),(2,'Bo',NULL);
INSERT INTO dept VALUES (1,'Core');

-- Filter inside ON: applied while matching partners.
SELECT e.name, d.name FROM emp e
LEFT JOIN dept d ON d.id = e.dept_id AND d.name = 'Core';
-- Ada|Core
-- Bo|None      <- left row survives, no partner matched

-- Same filter in WHERE: applied to the joined result.
SELECT e.name, d.name FROM emp e
LEFT JOIN dept d ON d.id = e.dept_id WHERE d.name = 'Core';
-- Ada|Core
-- (Bo is gone: its NULL-extended row failed the WHERE predicate)
```

**Listing 1.** Verified on SQLite 3.53.1 (NULL shown as `None` by the Python driver). The `ON`-placed filter keeps the unmatched employee; the `WHERE`-placed filter silently turns the query into an inner join.

```d2
direction: right
from: "FROM\ncartesian pairs" {width: 170; height: 80}
on: "ON\nkeep matching pairs" {width: 190; height: 80}
join: "JOIN type\nadd NULL-extended rows" {width: 230; height: 80}
where: "WHERE\nfilter joined rows" {width: 190; height: 80}
from -> on -> join -> where
```

**Fig. 1.** `ON` selects partners during the join; the outer-join type decides which unmatched rows are re-added with `NULL`s; `WHERE` sees only the finished result — too late to keep anything it drops.

> [!warning] "Conceptually first" does not mean the engine runs it first
> Physically the optimizer pushes `WHERE` predicates into the join and the scan whenever that is safe: for inner joins the plans are identical, and even for outer joins a `WHERE` predicate on the left table can be applied early. The order is a correctness contract for the *result*; `EXPLAIN` shows what the plan actually does ([[How do you use EXPLAIN ANALYZE in SQL]]).

> [!tip] Interview answer
> Logically, FROM and JOIN run before WHERE: the join builds the row source and WHERE filters it afterward. For inner joins the placement does not matter, but for a LEFT JOIN it changes the meaning — a right-table filter in ON picks partners and keeps unmatched left rows with NULLs, while the same filter in WHERE drops those NULL rows and effectively becomes an inner join. Physically the optimizer reorders all of this, so the order is about semantics, not execution.
