<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `NULL` in SQL means **"value unknown or absent"** — not zero, not empty string, not false. Comparisons with NULL yield **UNKNOWN** (three-valued logic), so `= NULL` never matches; the dedicated operators are `IS NULL` / `IS NOT NULL`. Aggregates skip NULLs, concatenation propagates them, and the NOT IN subquery trap follows directly ([[Why is NOT IN dangerous with NULL]]).

Three-valued logic is the mechanic to present: every predicate evaluates to TRUE, FALSE, or UNKNOWN, and WHERE keeps only TRUE. `city = 'Berlin'` on a NULL city is UNKNOWN — the row disappears from both `= 'Berlin'` and `<> 'Berlin'` results; `NOT (city = 'Berlin')` is still UNKNOWN (NOT of UNKNOWN), which the demo proves: 2 matches, 3 non-matches, and the NOT form still 3 — the NULL row returns under neither. `IS NULL` is the only spelled-out way to reach it (1 row). Propagation rules complete the picture: arithmetic and concatenation with NULL yield NULL (`name || '/' || city` prints empty for Boris), aggregates except COUNT(*) ignore NULL inputs, and set operators treat NULL rows as duplicates of each other ([[How does GROUP BY handle NULL in SQL]], [[What are the main SQL aggregate functions]]). Design-wise, NULL means "missing" with many flavors — not yet known, not applicable, deliberately withheld — and schemas that use '' or 0 as fake-NULLs lose the distinction. Constraints control presence: NOT NULL forbids it; CHECK (col <> '') forbids the empty-string fake ([[How do you forbid NULL or empty values in a database column]]).

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
INSERT INTO customers VALUES (1,'Alice','Berlin'),(2,'Boris',NULL),
 (3,'Carla','Berlin'),(4,'Dmitri','Paris'),(5,'Elena','Tokyo');

SELECT COUNT(*) FROM customers WHERE city = 'Berlin';
-- 2
SELECT COUNT(*) FROM customers WHERE city <> 'Berlin';
-- 3
SELECT COUNT(*) FROM customers WHERE NOT (city = 'Berlin');
-- 3
SELECT COUNT(*) FROM customers WHERE city IS NULL;
-- 1
SELECT name || '/' || city FROM customers WHERE id = 2;
-- (empty: NULL propagated through concatenation)
```

**Listing 1.** Verified on SQLite 3.53.1. Five customers: two in Berlin, three outside, zero matched by NOT(= 'Berlin') beyond the same three — the NULL row is invisible to both sides of the comparison and reachable only via IS NULL.

```d2
direction: right
t: "predicate evaluates" {width: 180; height: 60}
tr: "TRUE -> row kept" {width: 170; height: 60}
fa: "FALSE -> row dropped" {width: 180; height: 60}
un: "UNKNOWN -> row dropped
(NULL comparison)" {width: 210; height: 70}
t -> tr
t -> fa
t -> un
```

**Fig. 1.** WHERE keeps only TRUE; UNKNOWN — the third truth value born from comparing with NULL — behaves like FALSE for filtering but like TRUE for NOT IN's poison effect.

> [!warning] UNKNOWN is not FALSE: negation does not rescue it
> `NOT (x = NULL)` is still UNKNOWN — the row stays excluded — which is exactly why "I added NOT" does not fix empty NOT IN results. Only IS NULL / IS NOT NULL and COALESCE-style handling turn UNKNOWN back into a boolean decision ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> NULL means unknown or absent, and it poisons ordinary comparisons: x = NULL is UNKNOWN, never true, so WHERE drops the row on both the equals and the not-equals side — only IS NULL reaches it. NULL propagates through arithmetic and concatenation, aggregates ignore it except COUNT(*), and two NULL rows count as duplicates for DISTINCT and UNION. The practical rules I follow: IS NULL for checks, COALESCE for defaults, NOT NULL constraints where a value is mandatory, and never NOT IN against a nullable subquery.
