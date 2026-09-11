<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `EXPLAIN` shows the planned strategy; `EXPLAIN ANALYZE` **additionally executes** the statement and annotates every plan node with *actual* measurements — real row counts, loops, and time. It is the only way to see where estimates diverge from reality. PostgreSQL spells it `EXPLAIN ANALYZE`; SQLite embeds the counts in `EXPLAIN ANALYZE` output of the CLI and exposes per-step counting through its bytecode `EXPLAIN`.

The workflow it enables is estimate auditing: the planner's `rows` guess versus the actual row count per node. PostgreSQL's documentation for EXPLAIN shows exactly this contrast — estimated and actual rows side by side (`rows=... loops=...`), plus true timing per node, with the warning that ANALYZE really runs the statement ([[What do cost rows and loops mean in EXPLAIN]]). The demo verifies the safe half on SQLite: the query plan (static) for the join; the ANALYZE half adds per-node actuals in engines where it runs. Safety rules matter and are part of the answer: ANALYZE executes — INSERT/UPDATE/DELETE really mutate (wrap in a transaction and roll back), SELECT runs at full cost, and timing measurements include overhead; on a busy system use the estimated plan (PostgreSQL: `EXPLAIN` without ANALYZE, or `auto_explain.log_analyze`) before escalating ([[How do you systematically diagnose a slow SQL query]]). The second reading skill: actual loops multiply per-node time — a nested-loop inner node that says `rows=1 loops=10000` did ten thousand index probes, which is the single most common "the plan looked fine" trap ([[What is the difference between Nested Loop Hash Join and Merge Join]]).

```sql
EXPLAIN QUERY PLAN
SELECT c.name, o.amount FROM customers c
JOIN orders o ON o.customer_id = c.id WHERE c.city = 'Berlin';
-- QUERY PLAN
-- |--SCAN o
-- `--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
-- (EXPLAIN ANALYZE would re-print this plan with actual row counts
--  and per-node time appended; on PostgreSQL: cost + real rows/loops)
```

**Listing 1.** Verified on SQLite 3.53.1 for the plan itself; per SQLite's EXPLAIN documentation, the ANALYZE form appends the actual number of rows each step produced. PostgreSQL documents the same idea as estimated versus actual rows per node.

```d2
direction: right
e1: "EXPLAIN
planned tree + estimates
nothing runs" {width: 220; height: 90}
e2: "EXPLAIN ANALYZE
executes + annotates
real rows, loops, time" {width: 230; height: 90}
q: "audit: estimate vs actual
divergence = stale stats or skew" {width: 260; height: 90}
e1 -> q
e2 -> q
```

**Fig. 1.** The pair answers two different questions: what the engine intends, and what it actually did — the gap between them is the diagnostic signal.

> [!warning] EXPLAIN ANALYZE runs the statement — including its writes
> On PostgreSQL, `EXPLAIN ANALYZE DELETE ...` deletes rows (triggering side effects and triggers); the documented safe pattern is `BEGIN; EXPLAIN ANALYZE <statement>; ROLLBACK;`. Treating ANALYZE as a read-only inspection is a production incident waiting for a schedule ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> EXPLAIN prints the plan with cost estimates; EXPLAIN ANALYZE also executes it and annotates every node with actual row counts, loops and time — that is how you audit planner estimates against reality and find where the guess was wrong. I always mention it runs the statement, so for writes I wrap it in a transaction and roll back, and I read loops carefully: an inner node reporting tiny rows but thousands of loops did the whole work of the join.
