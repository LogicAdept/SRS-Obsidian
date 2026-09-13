<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #SRS

# What is sixth normal form and where does per-attribute decomposition pay off

> [!abstract] Short answer
> **6NF means every join dependency is trivial: each table is a key plus at most one non-key attribute.** No further lossless split is possible. The niche where it pays off today is temporal data — independent validity timelines per attribute — where one wide history table forces the cross product of all timelines, and the theoretical endpoint beyond it is DKNF.

## The two-timelines problem

An employee's salary changes on its own schedule (3 periods in a year), the title on another (2 periods). A history table holding both facts with two (valid_from, valid_to) pairs cannot express two independent timelines: the only faithful encoding pairs every salary period with every title period. Measured on SQLite 3.53.1: 3 × 2 = **6 rows store 5 facts**; renaming the title touched **3** rows in the wide table. In 6NF — emp_salary(emp, amount, valid_from, valid_to) and emp_title(emp, title, valid_from, valid_to) — the same history is 3 + 2 = **5 rows**, the rename is close-one-interval plus insert-one, and a point-in-time query joins the per-attribute tables with the date filters and returns exactly one row (`120 | dev` at 2026-04-15).

```sql
CREATE TABLE emp_salary (emp TEXT, amount INT,
  valid_from TEXT, valid_to TEXT, PRIMARY KEY (emp, valid_from));
CREATE TABLE emp_title  (emp TEXT, title TEXT,
  valid_from TEXT, valid_to TEXT, PRIMARY KEY (emp, valid_from));

SELECT s.amount, t.title
FROM emp_salary s JOIN emp_title t
  ON t.emp = s.emp
 AND '2026-04-15' >= s.valid_from AND '2026-04-15' < s.valid_to
 AND '2026-04-15' >= t.valid_from AND '2026-04-15' < t.valid_to;
```

**Listing 1.** One table per attribute, each with its own validity interval. Verified on SQLite 3.53.1: 5 rows store what the wide table needed 6 for, and the point-in-time join returns a single row.

```d2
direction: right
wide: "emp_wide\nsalary timeline x title timeline\n6 rows, 5 facts" {
  width: 260
  height: 100
  style.fill: "#ffebee"
}
s: "emp_salary\nkey + one fact\n3 rows" {
  width: 170
  height: 90
  style.fill: "#e3f2fd"
}
t: "emp_title\nkey + one fact\n2 rows" {
  width: 170
  height: 90
  style.fill: "#e8f5e9"
}
wide -> s
wide -> t
```

**Fig. 1.** 6NF decomposition along attributes: each timeline gets its own relation, so each write touches exactly one fact's rows and no period pair is invented by storage.

## Where it is real, and where it is not

Legitimate uses: interval-stamped histories and audit trails (salary, pricing, position, configuration), bitemporal designs where valid time and record time both matter, anchor-modeling-style warehouses where attributes appear and disappear independently, and the physical analogy of columnar engines that store values per attribute anyway. The costs are symmetrical: every read of "the whole row" becomes a join across per-attribute tables, every insert of a coherent fact touches several tables, and cross-attribute constraints ("salary exists only while hired") leave the world of PK/FK enforcement. Overlap protection inside one timeline also needs an exclusion constraint (a PostgreSQL feature) or application checks — a plain PK on (emp, valid_from) does not forbid overlapping intervals.

> [!warning] Two popular misreadings
> First: "6NF my OLTP schema" is the anti-pattern — the write path already enforces 3NF/BCNF facts; per-attribute splitting multiplies joins on every read for no anomaly removed. 6NF earns its cost only when the timeline **is** the data. Second: "columnar store = 6NF" is only an analogy — a columnar engine compresses and scans per column but the logical schema still sits wherever you designed it; physical storage format and normal forms live on different levels.

One step beyond sits DKNF: every constraint of the schema is a logical consequence of domain constraints (the allowed values per column) and key constraints alone — no separate table-level rules left to state. It is a definition of "fully self-enforcing design" rather than a rung engines let you certify; a 6NF temporal schema with typed intervals and keyed periods is the closest practical shape. In interview terms: name 6NF as the per-attribute endpoint of decomposition, and reach for it when histories with independent timelines are the workload — not as the next rung after 5NF by default.

The rung below: [[What is fifth normal form and when does a three-way decomposition matter]]; what skipping decomposition breeds: [[What can violating database normalization lead to]]; the deliberate reverse trade: [[What is database denormalization for]]; the ladder from the start: [[What is normalization]].

> [!tip] Interview answer
> 6NF is full per-attribute decomposition: key plus at most one non-key column per table, every join dependency trivial. The working case is temporal data with independent validity periods — measured: two timelines in one wide table needed 6 rows for 5 facts and a title rename touched 3 rows; in 6NF the same history is 3 + 2 rows, the rename is one close plus one insert, and a point-in-time query is a dated join. Beyond it, DKNF asks that every constraint follow from domains and keys alone — a design goal, not an engine feature.
