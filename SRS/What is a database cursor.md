<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A **cursor** is a named, positioned handle over a result set that the client (or a procedure) steps through row by row: DECLARE (bind the query), OPEN, FETCH (advance and retrieve), CLOSE. Standard SQL has them; PostgreSQL exposes DECLARE/FETCH/MOVE/CLOSE. The modern default is *not* to declare them: language APIs (JDBC ResultSet, sqlite3 Cursor) already iterate results as cursors, and set-at-a-time SQL beats row-by-row processing ([[What is the N plus 1 problem in SQL]]).

The mechanics are genuinely useful in two niches. Streaming huge results: a server-side cursor with a small fetch size (JDBC `setFetchSize`, PostgreSQL's DECLARE ... CURSOR WITH HOLD + FETCH n, or its cursor-shaped protocol) keeps memory bounded where buffering the whole ResultSet would not — the documented answer to "SELECT of 50M rows OOMs the client". Procedural row-by-row logic inside PL/pgSQL loops uses cursors explicitly — legitimate where per-row logic is irreducible. The costs are the reason they carry a smell: row-by-row processing forfeits set-at-a-time optimization (one UPDATE instead of a fetch-compute-update loop), holds the transaction/position open (long-lived cursors pin snapshots and vacuum cannot clean what a cursor might still read — PostgreSQL documents this for WITH HOLD cursors), and multiplies round trips by row count. The verified demo shows the *modern* cursor — the client API's forward iteration — consuming an UPDATE ... RETURNING result row by row: positioned, streaming, no DECLARE. The interview formulation: "cursor" names two things — the SQL object and the API concept — and knowing which one the question means is half the answer ([[How does a database query run]]).

```sql
UPDATE employees SET salary = salary + 1 WHERE dept_id = 1
RETURNING name, salary;
-- Greta|5001
-- Hans|3501
-- Ivan|3501
-- (rows stream out one by one: the client's cursor reads them
--  incrementally -- this is what RETURNING + iteration is for)
-- SQL-standard server-side spelling (PostgreSQL syntax, per docs):
-- DECLARE emp_cur CURSOR FOR SELECT name, salary FROM employees;
-- OPEN emp_cur; FETCH NEXT FROM emp_cur; ... CLOSE emp_cur;
```

**Listing 1.** Verified on SQLite 3.53.1: RETURNING streams modified rows for row-by-row client consumption — the API-cursor pattern. The DECLARE/OPEN/FETCH block is the SQL-standard server-side form as documented by PostgreSQL.

```d2
direction: right
q: "query
result set" {width: 140; height: 70}
c: "cursor
position + fetch" {width: 160; height: 80}
r1: "row 1" {width: 90; height: 50}
r2: "row 2" {width: 90; height: 50}
r3: "..." {width: 80; height: 50}
q -> c
c -> r1 -> r2 -> r3
```

**Fig. 1.** A cursor is a bookmark over the result set: each FETCH advances the position and returns one row — streaming semantics over a query.

> [!warning] Row-by-row cursors are usually a set-based query in disguise
> A cursor loop that updates each row is a locking, round-trip-hungry echo of `UPDATE ... WHERE ...`; the set form runs in one statement, one pass, with the optimizer's plan. Reserve explicit cursors for streaming large reads and irreducible per-row procedures — and expect the "why is this loop slow" ticket afterwards otherwise ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> A cursor is a positioned handle over a result set: declare, open, fetch, close — SQL-standard, and PostgreSQL exposes it. In practice I meet cursors as the client API's iteration (JDBC ResultSet, sqlite3 Cursor) and use server-side cursors only for streaming huge result sets with bounded fetch sizes or for genuinely per-row procedures. I flag row-by-row cursor loops that could be one set-based UPDATE, and I know WITH HOLD cursors pin snapshots and block vacuum — open them deliberately, close them early.
