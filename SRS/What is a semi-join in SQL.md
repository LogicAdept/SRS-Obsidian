<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A **semi-join** returns rows of the left table that *have at least one match* on the right — without concatenating right-side columns and without left-side duplicates. Idioms: `EXISTS` (correlated), `IN (subquery)`, or `JOIN` + `DISTINCT`. The engine may implement any of them with the same semi-join plan.

The name matters because it names the *goal*: membership, not combination. SQL has no `SEMI JOIN` keyword, so the semantics live in the three idioms, and they differ only in corner cases ([[What is the difference between IN EXISTS and JOIN in SQL]]): `EXISTS` short-circuits on the first match and is NULL-safe; `IN` is NULL-sensitive in negated form; `JOIN` + `DISTINCT` computes all matches and then collapses them — correct but it does the work semi-joins skip. PostgreSQL's planner natively recognizes all three shapes and can use the same "unique-ify then join" strategy; its documentation describes the semi-join as a distinct join strategy for this reason. The demo shows the two producing idioms on departments that have employees: both return HR and IT exactly once, even though IT has three employees — no multiplication, no DISTINCT needed in the EXISTS form ([[What is an anti-join in SQL]]).

```sql
CREATE TABLE departments (id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO departments VALUES (1,'IT'),(2,'HR'),(3,'Research');
INSERT INTO employees VALUES (1,'Greta',1),(2,'Hans',1),(3,'Ivan',1),(4,'Julia',2);

SELECT d.title FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id) ORDER BY d.title;
-- HR
-- IT
SELECT DISTINCT d.title FROM departments d
JOIN employees e ON e.dept_id = d.id ORDER BY d.title;
-- HR
-- IT
```

**Listing 1.** Verified on SQLite 3.53.1. EXISTS yields each qualifying department once; the join would have returned IT three times, so the idiom needs DISTINCT to reach the same set. Semi-join semantics: left rows with at least one match, right columns discarded.

```d2
direction: right
d: "departments
IT HR Research" {width: 180; height: 80}
e: "employees
3 x IT, 1 x HR" {width: 180; height: 80}
s: "semi-join
departments WITH a match:
IT, HR (once each)" {width: 230; height: 100}
d -> s
e -> s
```

**Fig. 1.** The right side only *votes* (match exists or not); its rows and columns never appear in the output, and repeated matches do not duplicate left rows.

> [!warning] JOIN plus DISTINCT is the slowest correct spelling
> It materializes every match (three IT rows), then dedups — extra work growing with match count. For large child tables, EXISTS or IN lets the engine stop at the first match per outer row and often avoids the distinct pass entirely; check both plans before assuming ([[What is the difference between IN EXISTS and JOIN in SQL]], [[Why is SELECT DISTINCT expensive]]).

> [!tip] Interview answer
> A semi-join answers "which left rows have at least one match" and never copies right-side columns or duplicates left rows. SQL spells it with EXISTS, with IN, or as a join wrapped in DISTINCT. I default to EXISTS because it is NULL-safe and short-circuits per row, and I treat join-plus-DISTINCT as a readability fallback that can be measurably slower on high-fan-out children. The anti-join is its negated sibling and answers "left rows with no match".
