<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> An **anti-join** returns rows of the left table that have **no** match on the right. Idioms: `NOT EXISTS (correlated subquery)`, `LEFT JOIN ... WHERE right.key IS NULL`, or — only when the subquery column cannot contain NULL — `NOT IN`. The first is the default recommendation: NULL-safe, plan-efficient, and unambiguous.

Anti-joins are everywhere in real systems: unsubscribed users, orders without invoices, departments with no employees. The three idioms differ in exactly one dimension — NULL handling — and that difference has burned entire production datasets. `NOT IN (subquery)` uses the three-valued `IN` semantics: if the subquery returns a single NULL, every comparison becomes UNKNOWN and the whole result is empty ([[Why is NOT IN dangerous with NULL]]). `NOT EXISTS` asks a correlated question per left row ("does any match exist?") whose answer is simply false — no NULL trap. `LEFT JOIN ... IS NULL` exploits NULL padding from the outer join and is equally safe, though it looks like an accident to readers, so a comment helps ([[How does LEFT JOIN differ from INNER JOIN in SQL]]). Engines know the pattern: PostgreSQL plans both NOT EXISTS and LEFT JOIN IS NULL as a hash or merge anti-join, and SQLite shows a correlated search per outer row in the query plan — semantics identical, mechanics differ.

```sql
CREATE TABLE departments (id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO departments VALUES (1,'IT'),(2,'HR'),(3,'Research');
INSERT INTO employees VALUES (1,'Greta',1),(2,'Julia',2);

SELECT d.title FROM departments d
WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);
-- Research
SELECT d.title FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id WHERE e.id IS NULL;
-- Research
SELECT title FROM departments WHERE id NOT IN (SELECT dept_id FROM employees);
-- Research
```

**Listing 1.** Verified on SQLite 3.53.1. All three idioms agree here because `dept_id` contains no NULL; the NOT IN form would silently return zero rows the moment one employee row carried a NULL `dept_id`.

```d2
direction: right
d: "departments
IT HR Research" {width: 180; height: 80}
e: "employees
IT HR only" {width: 160; height: 80}
a: "anti-join
rows with NO match:
Research" {width: 210; height: 90}
d -> a
e -> a
```

**Fig. 1.** The anti-join is the complement of the semi-join: it keeps exactly those left rows whose match set is empty, still discarding right-side columns.

> [!warning] NOT IN with a nullable column returns an empty set, not an error
> One NULL in the subquery result makes every `x NOT IN (...)` evaluate to UNKNOWN — the query "works", returns nothing, and dashboards just look oddly empty. Ban `NOT IN` against subqueries in code review; use NOT EXISTS or add `WHERE col IS NOT NULL` with a comment explaining why ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> An anti-join selects left rows with no match on the right, spelled as NOT EXISTS, as LEFT JOIN with IS NULL, or as NOT IN. NOT EXISTS is my default: per-row existence check, no NULL semantics. LEFT JOIN IS NULL is equivalent and plan-friendly on most engines. NOT IN is the dangerous one — a single NULL in the subquery empties the whole result because of three-valued logic, so I only accept it with an explicit IS NOT NULL filter and a comment.
