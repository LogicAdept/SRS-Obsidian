<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is a query plan in a relational database?

> [!abstract] Short answer
> A **query plan** is the engine's chosen execution strategy for one SQL statement: an ordered tree of operations (scan this table, seek that index, join these inputs, sort, aggregate). The same SQL can have many plans; the **planner** picks one from statistics and available indexes. `EXPLAIN` prints the plan without running it ([[How do you use EXPLAIN ANALYZE in SQL]]).

SQL is declarative — the statement says *what*, the plan says *how*. The PostgreSQL documentation presents EXPLAIN output as a tree of plan nodes (Seq Scan, Index Scan, Hash Join...) each with cost estimates; SQLite's EXPLAIN QUERY PLAN prints the same idea as an indented list of scan and search operations. The demo's plan reads: scan the orders table once, and for each order seek the customers primary key by rowid — a nested-loop shape that SQLite's optimizer chose because the inner probe is a one-hop B-tree descent ([[What is the difference between Nested Loop Hash Join and Merge Join]]). Reading plans is the skill that separates "I rewrote the query" from "I made it faster": every optimization claim (index helps, LIMIT avoids sort, EXISTS beats JOIN) is a plan-level claim and is checked there ([[How do you systematically diagnose a slow SQL query]]). A plan is also a *contract document* for interviews: being able to say "this line means the engine probes an index per row; this one means a full table read" demonstrates mechanism knowledge, not vocabulary ([[How does a database query run]]).

```sql
EXPLAIN QUERY PLAN
SELECT c.name, o.amount FROM customers c
JOIN orders o ON o.customer_id = c.id WHERE c.city = 'Berlin';
-- QUERY PLAN
-- |--SCAN o
-- `--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

**Listing 1.** Verified on SQLite 3.53.1. Two operations: a full scan of orders (no useful index on the filter) and, per order row, a primary-key search into customers. The join order and access paths are the plan's actual decisions.

```d2
direction: right
sql: "SQL text
declarative: what" {width: 180; height: 80}
p: "planner
statistics + indexes" {width: 190; height: 80}
pl: "plan
tree of operations: how" {width: 210; height: 80}
e: "executor
runs the tree" {width: 160; height: 70}
sql -> p -> pl -> e
```

**Fig. 1.** The planner is the translation layer between declarative SQL and a concrete operator tree; EXPLAIN exposes that tree before execution.

> [!warning] A plan is a decision for one moment, not a property of the query
> Data volumes, statistics freshness and new indexes change the plan for identical SQL. Caching a plan decision ("this query always uses the index") in documentation or code is how stale-performance folklore spreads; re-read EXPLAIN after growth or after migrations ([[How do stale statistics hurt a query plan]]).

> [!tip] Interview answer
> A query plan is the engine's chosen tree of operations for a statement — access paths like scan or index seek, join order and algorithm, sort and aggregate nodes. SQL is declarative, so the planner picks the plan from statistics and indexes, and EXPLAIN shows it before running. I read plans as the ground truth for every performance claim: the plan tells me whether a predicate really uses an index, how the join executes, and where rows are counted or sorted.
