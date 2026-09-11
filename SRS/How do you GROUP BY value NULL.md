<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How do you GROUP BY value NULL?

> [!abstract] Short answer
> The standard toolkit for a NULL grouping key: **surface it explicitly** with `COALESCE`/`ISNULL` labels (`COALESCE(city, 'unknown')`), **exclude it** with `WHERE key IS NOT NULL` when the NULL bucket is not a business category, or **keep it NULL** when the report must distinguish "no value" from any real value. `NVL`/`IFNULL` are engine aliases of the same idea.

Grouping NULLs is settled semantics ([[How does GROUP BY handle NULL in SQL]]); the question is what the *report* should mean. Labeling with COALESCE is the default choice — but it must be applied in both the SELECT list and the GROUP BY (group by the same expression, or group by the bare column and COALESCE only in projection — both work, and grouping the expression makes the key match the label). Excluding with `IS NOT NULL` changes denominators: per-city percentages computed over non-NULL cities no longer sum to 100 — worth stating out loud in an interview. Keeping NULL distinguishes "address unknown" from "city is ''" only if the schema does not conflate empty strings with NULLs. One portability nuance: SQLite's native GROUP_CONCAT skips NULLs, PostgreSQL's string_agg skips NULLs, but a *label* row still exists; and `ORDER BY` places the NULL group differently on SQLite (first, ascending) versus PostgreSQL (last, ascending) — pin it explicitly with `NULLS LAST`/`NULLS FIRST` where supported ([[What is the difference between SQL WHERE and HAVING clauses]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris',NULL),
 (3,'Carla','Berlin'),(4,'Dmitri','Paris'),(5,'Elena','Tokyo'),(6,'Fedor',NULL);

SELECT COALESCE(city, 'unknown') AS city_label, COUNT(*) AS n
FROM customers GROUP BY COALESCE(city, 'unknown') ORDER BY n DESC;
-- Berlin|2
-- unknown|2
-- Tokyo|1
-- Paris|1
SELECT city, COUNT(*) FROM customers
WHERE city IS NOT NULL GROUP BY city ORDER BY city;
-- Berlin|2
-- Oslo|1
-- Paris|1
-- Tokyo|1
```

**Listing 1.** Verified on SQLite 3.53.1. The labeled form reports "unknown|2" as a first-class bucket (Boris and Fedor); the excluded form drops them entirely — four cities, four rows, denominator changed from six to four.

```d2
direction: right
n: "NULL key group
Boris, Fedor" {width: 170; height: 80}
l: "label
COALESCE -> unknown" {width: 190; height: 70}
x: "exclude
WHERE IS NOT NULL" {width: 200; height: 70}
k: "keep NULL
distinguish from real values" {width: 220; height: 80}
n -> l
n -> x
n -> k
```

**Fig. 1.** Three deliberate fates for the NULL group — rename it, remove it, or preserve it — each with different meaning for whoever reads the report.

> [!warning] Labeling hides the distinction between NULL and the label string
> After `COALESCE(city, 'unknown')`, a customer genuinely named in city "unknown" is indistinguishable from a missing value, and the original NULL can no longer be recovered from the output. If downstream consumers need the distinction, keep the NULL column alongside the label or filter instead of renaming ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> NULLs form one group, and what I do with it is a reporting decision: label it with COALESCE(key, 'unknown') applied consistently in GROUP BY and SELECT, exclude it with WHERE key IS NOT NULL — accepting that percentages no longer sum to 100 — or keep it NULL when "no value" must stay distinguishable. I also pin NULL ordering explicitly, because SQLite sorts NULLs first ascending and PostgreSQL last by default, so a shared report can render the bucket in different places.
