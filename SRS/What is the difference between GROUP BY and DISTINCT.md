<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> Both `GROUP BY` and `DISTINCT` collapse duplicate rows, and on the same column list they return the same set of rows. The difference is purpose: **DISTINCT only dedups**; **GROUP BY partitions** and therefore enables per-group aggregates. `GROUP BY x` plus a bare `SELECT x` is a verbose DISTINCT; `SELECT DISTINCT x, COUNT(*)` is a syntax error.

Because the outputs coincide, engines frequently produce identical plans for the dedup-only forms — SQLite shows `USE TEMP B-TREE FOR DISTINCT` versus its grouping machinery, and PostgreSQL maps both to a HashAggregate when no index helps. The meaningful distinction is downstream capability: after `GROUP BY`, each group's aggregates are computable (COUNT, SUM), HAVING can filter groups, and multi-column grouping keys come free. DISTINCT has none of that: it answers "which values exist" and stops ([[Why is SELECT DISTINCT expensive]]). The demo shows identical city sets from both spellings and the one-row-per-city with counts only GROUP BY can add. In interviews the sharp version of the question is about *fan-out*: people "fix" a multiplied join by adding DISTINCT when the real answer is EXISTS or pre-aggregation — GROUP BY is not a join-bandage either, it is a reducer with its own cost ([[What is a semi-join in SQL]], [[Why can a JOIN multiply your row count]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris',NULL),
 (3,'Carla','Berlin'),(4,'Dmitri','Paris'),(5,'Elena','Tokyo');

SELECT DISTINCT city FROM customers ORDER BY city;
-- (empty row for NULL)
-- Berlin
-- Oslo
-- Paris
-- Tokyo
SELECT city FROM customers GROUP BY city ORDER BY city;
-- (empty row for NULL)
-- Berlin
-- Oslo
-- Paris
-- Tokyo
SELECT city, COUNT(*) FROM customers GROUP BY city ORDER BY city;
-- |1
-- Berlin|2
-- Oslo|1
-- Paris|1
-- Tokyo|1
```

**Listing 1.** Verified on SQLite 3.53.1. DISTINCT and GROUP BY return the identical four-row city set (NULL included as one value); only GROUP BY can carry the per-city counts alongside.

```d2
direction: right
d: "DISTINCT
dedup only
which values exist" {width: 190; height: 90}
g: "GROUP BY
dedup + partition
values AND their aggregates" {width: 220; height: 100}
r: "same row set
when no aggregates" {width: 190; height: 80}
d -> r
g -> r
```

**Fig. 1.** The two operators share the dedup outcome but not the capability: GROUP BY retains the partition as a context for aggregation, DISTINCT forgets it immediately.

> [!warning] Reaching for GROUP BY when DISTINCT was meant (or vice versa) changes the question
> `GROUP BY` with a stray non-key column either errors (standard) or picks arbitrary values (SQLite, MySQL) — a silent correctness hazard; DISTINCT cannot be "extended" with a count. Choose by question: "what exists" is DISTINCT, "what exists and how much" is GROUP BY ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> On the same column list they produce the same rows — both are dedup, both treat NULLs as equal. The difference is capability: GROUP BY partitions, so it unlocks aggregates, HAVING and multi-key grouping, while DISTINCT only answers which distinct rows exist. Plans are often identical without aggregates. The trap I watch for: neither belongs in a query to patch join fan-out — that is a semi-join or pre-aggregation problem, and DISTINCT there hides the cost instead of fixing the cause.
