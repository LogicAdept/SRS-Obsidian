<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How does a database query run?

> [!abstract] Short answer
> Five stages: **parse** (text to a parse tree, checking syntax and names), **plan** (choose access paths, join order and algorithms from statistics), **optimize** (cost the alternatives, pick the cheapest), **execute** (run the plan tree, pulling rows through operators), and **fetch/return** (project columns, transmit). `EXPLAIN` inspects the plan stage without executing ([[What is a query plan in a relational database]]).

SQLite makes the executor stage literally inspectable: `EXPLAIN SELECT` emits the virtual-machine bytecode (opcodes like `OpenRead`, `Rewind`, `Column`, `Ne`, `ResultRow`, `Next`) — the verified demo shows a 12-opcode program for one filtered scan: open the table, rewind to the first row, compare the column, emit or skip, step. Seeing that the " declarative query" becomes a small program with jumps is the strongest mental model fix available: the engine is an interpreter for plans ([[What is a query plan in a relational database]]). The planner stage is where cost-based decisions happen — PostgreSQL's documentation describes the planner costing candidate paths using table and index statistics (pg_class sizes, per-column histograms in pg_stats); SQLite documents its planner heuristics in the query-planner overview, driven by sqlite_stat1 after ANALYZE. Caches sit on top: parsed trees, plan caches and buffer pools mean the second execution of the same statement skips most of the work — the reason prepared statements exist ([[How do you identify slow or non-performant SQL queries]]).

```sql
EXPLAIN SELECT c.name FROM customers c WHERE c.city = 'Berlin';
-- 0|Init|0|9|0||0|
-- 1|OpenRead|0|2|0|3|0|
-- 2|Rewind|0|8|0||0|
-- 3|Column|0|2|1||0|
-- 4|Ne|2|7|1|BINARY-8|82|
-- 5|Column|0|1|3||0|
-- 6|ResultRow|3|1|0||0|
-- 7|Next|0|3|0||1|
-- ... (12 opcodes total)
```

**Listing 1.** Verified on SQLite 3.53.1. The filtered scan compiles to: open the table cursor, rewind to the first row, load the column, compare (`Ne` jumps past output on mismatch), emit the row, advance (`Next` jumps back) — a plan is a program.

```d2
direction: right
p: "parse
text -> tree" {width: 130; height: 70}
pl: "plan + optimize
paths, order, cost" {width: 180; height: 80}
e: "execute
operator tree runs" {width: 160; height: 70}
r: "rows returned" {width: 140; height: 60}
p -> pl -> e -> r
```

**Fig. 1.** A statement's life: parse to a tree, plan and cost a strategy, then execute — EXPLAIN stops after planning, EXPLAIN ANALYZE instruments execution.

> [!warning] Errors happen at different stages — and that changes their timing
> A missing column or bad syntax fails at parse, before any work; a constraint violation fails at execute, possibly after thousands of rows were already written. Debugging by stage explains why some errors appear instantly on the client and others only under load or on specific rows ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> A statement goes parse, plan, execute: parse checks syntax and names; the planner picks access paths, join order and algorithms using statistics and costs them; the executor runs the chosen operator tree, usually pulling rows pipeline-style. SQLite even exposes the executor as bytecode opcodes via EXPLAIN. For performance work what matters is the plan stage — statistics drive it — and caches above it, which is why prepared statements skip most overhead on repeat executions.
