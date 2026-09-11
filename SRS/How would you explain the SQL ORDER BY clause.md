<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you explain the SQL ORDER BY clause?

> [!abstract] Short answer
> `ORDER BY` sorts the result rows by one or more keys, each ASC (default) or DESC, and accepts expressions and collations. Two mechanics matter beyond syntax: **NULL placement** is engine-defined (SQLite: NULLs first ascending; PostgreSQL: NULLs last ascending, overridable with NULLS FIRST/LAST), and the sort is a *plan node* that disappears when an index already supplies the key order ([[What is filesort or an external merge in a plan]], [[How do you avoid a sort with an index]]).

The multi-key demo shows the full contract: `ORDER BY category ASC, price DESC` sorts products by category ascending and, within equal categories, price descending — lexicographic on the key tuple, with every listed key applied in order. NULL placement is verified on SQLite: ascending ORDER BY city lists the NULL-city row **first** (before Berlin), descending lists it **last** — SQLite treats NULL as smaller than every value; PostgreSQL defaults to the opposite on ascending (NULLs last) and exposes `NULLS FIRST`/`NULLS LAST` explicitly — a portability trap for shared reports ([[How does GROUP BY handle NULL in SQL]]). The plan dimension: ORDER BY is either free (an index scan in key order — verified in the sort-avoidance cards) or a blocking sort node ([[What is filesort or an external merge in a plan]]). Expressions sort by computed values (`ORDER BY price * qty`), with the sargability caveat on the index side. `ORDER BY` also binds last in the logical order — it may reference SELECT aliases (unlike WHERE), and with set operators it applies to the *combined* result, placed after the last operand ([[What is the logical order of SQL SELECT execution]], [[How would you explain the SQL SELECT statement]]).

```sql
CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT, category TEXT, price NUMERIC);
INSERT INTO products VALUES
 (1,'SQL Pocket Guide','books',30.0),(5,'Notebook','books',5.0),
 (3,'Monitor 27','electronics',250.0),(2,'USB Cable','electronics',10.0);

SELECT category, price, title FROM products
ORDER BY category ASC, price DESC LIMIT 4;
-- books|30|SQL Pocket Guide
-- books|5|Notebook
-- electronics|250|Monitor 27
-- electronics|10|USB Cable
SELECT city FROM customers ORDER BY city LIMIT 3;
-- (NULL row first: SQLite sorts NULLs before every value ascending)
SELECT city FROM customers ORDER BY city DESC LIMIT 3;
-- Tokyo
-- Paris
-- Oslo
-- (NULL last in DESC: the mirror of the ascending case)
```

**Listing 1.** Verified on SQLite 3.53.1. Tuple ordering (category up, price down within category) and NULL placement on both ends — the two behaviors engines actually disagree on.

```d2
direction: right
k1: "key 1 ASC
category" {width: 140; height: 70}
k2: "key 2 DESC
price within category" {width: 190; height: 70}
r: "rows in tuple order
(NULLs: engine-defined slot)" {width: 240; height: 80}
k1 -> k2 -> r
```

**Fig. 1.** Multi-key ORDER BY is lexicographic on the key tuple; each key's direction applies within the ties of all previous keys, and NULLs occupy one engine-chosen end.

> [!warning] ORDER BY with ties is not deterministic without a tiebreaker
> Rows equal on all sort keys may emerge in any order (and any order again after plan changes); paginating on such an order loses or duplicates rows at page boundaries. Add a unique column as the final key — `ORDER BY category, price, id` — whenever the order feeds pagination or stable exports ([[Why is OFFSET pagination slow]]).

> [!tip] Interview answer
> ORDER BY sorts by a key list, each ASC or DESC, applied lexicographically — later keys order the ties of earlier ones. It accepts expressions and aliases, binds last in the logical order, and with set operators sits after the last operand. The two mechanics I always mention: NULL placement is engine-defined — SQLite sorts NULLs first ascending, PostgreSQL last, both overridable — and the sort is a plan node that vanishes when an index supplies the order, so hot ordered queries deserve a matching index plus a unique tiebreaker.
