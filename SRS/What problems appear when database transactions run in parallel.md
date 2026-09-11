<!--
reps: 0
priority: 0
-->
#Databases/Transactions #Problems/Concurrency #SRS

# What problems appear when database transactions run in parallel

> [!abstract] Short answer
> **Four named anomalies: lost update — one overwrite erases another; dirty read — reading uncommitted data; non-repeatable read — the same row changes between two reads; phantom read — the same predicate returns a different row set.** Isolation levels exist precisely to forbid these, and the fix space is "raise the level or take explicit locks".

## The catalog with a two-session sketch

**Lost update.** Both sessions read `counter = 10`, both write back their own computed value; one write silently replaces the other. The cure is read-modify-write inside the DBMS (`UPDATE t SET counter = counter + 1`), `SELECT ... FOR UPDATE`, or optimistic version columns (`UPDATE ... WHERE version = :seen`) — the last fails the update instead of silently dropping one writer.

**Dirty read.** Session B sees session A's uncommitted balance change; A rolls back; B acted on data that never existed. **Non-repeatable read.** B reads a row, A commits an update to it, B reads it again and gets a different value — breaks in-transaction invariants like "check then use". **Phantom read.** B counts rows matching a predicate, A commits an insert matching it, B's re-count differs. The difference from non-repeatable read is the predicate: rows appearing/disappearing in a *set*, not a single row changing.

```d2
direction: right
a1: "A: read row (v1)" {
  width: 190
  height: 70
  style.fill: "#e3f2fd"
}
a2: "B: update row, commit" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
a3: "A: read row again (v2)\nnon-repeatable read" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
a1 -> a2 -> a3
```

**Fig. 1.** Non-repeatable read in three steps: nothing dirty, no lock — just two reads of the same row straddling another transaction's commit.

Which anomalies survive depends on the level: READ COMMITTED blocks dirty reads but allows the other three; snapshot-based REPEATABLE READ blocks row changes but may allow phantoms (standard minimum) unless it is PostgreSQL's snapshot isolation, which blocks them too; SERIALIZABLE blocks all. The mapping table lives in [[What is database transaction isolation]].

```sql
-- optimistic lost-update guard: the write fails if someone else got there first
UPDATE account
SET balance = balance - 100, version = version + 1
WHERE id = 42 AND version = :version_seen_at_read;
```

**Listing 1.** Version-column concurrency control: the affected-row count of 0 tells the caller the update lost the race, so it can retry or report.

> [!warning] "It works in tests" because tests run one session at a time
> These anomalies need genuine concurrency; sequential tests and local debugging never reproduce them, and the code ships looking correct. The second trap is fixing them blindly with SERIALIZABLE everywhere — you buy anomaly-freedom at the price of serialization failures that every caller must retry. Prefer the narrowest cure: restructure as atomic UPDATE, add FOR UPDATE or a version column, raise the level only for the transaction that needs it.

The specific anomalies get their own drills: [[What are dirty reads in transaction isolation]] and [[What are phantom reads under weak isolation]]; the level ladder that governs them all in [[What is database transaction isolation]].

> [!tip] Interview answer
> Parallel transactions can lose updates, read uncommitted data, see rows change between reads, or see a predicate's row set change — lost update, dirty, non-repeatable, and phantom reads. Isolation levels map one-to-one onto forbidding these; the practical fixes are atomic read-modify-write statements, SELECT FOR UPDATE, or optimistic version checks, with higher isolation plus retries only where the invariant truly needs it.
