<!--
reps: 0
priority: 0
-->
#Databases/Transactions #Problems/Persistence #SRS

# What are phantom reads under weak isolation

> [!abstract] Short answer
> **A phantom read is a predicate-driven query returning a different set of rows when re-run inside the same transaction, because another transaction inserted or deleted matching rows and committed.** The row *set* changed — that is what separates a phantom from a non-repeatable read, which is one row changing value.

## The anatomy and why snapshot isolation matters here

Session B runs `SELECT count(*) FROM orders WHERE created_at >= today` → 42. Session A inserts one more order for today and commits. B re-runs the count → 43. Under READ COMMITTED each statement takes a fresh snapshot, so B sees A's commit; under the standard's minimum REPEATABLE READ guarantee, single-row stability is promised but the standard still permits phantoms. The practical outcome then depends on the engine's snapshot design: PostgreSQL's REPEATABLE READ is snapshot isolation — every read in the transaction sees the transaction-start snapshot, so the new row is invisible and the phantom cannot happen; InnoDB's REPEATABLE READ similarly reads from its first-read snapshot, and its gap/next-key locks additionally block other sessions from inserting into a scanned range, so even locking reads do not grow phantom rows. The standard's version of REPEATABLE READ — "no non-repeatable reads, phantoms allowed" — describes the floor, not every implementation.

```sql
-- session B (READ COMMITTED, PostgreSQL)
SELECT count(*) FROM orders WHERE created_at >= current_date;  -- 42
-- session A commits: INSERT INTO orders ... created_at = now()
SELECT count(*) FROM orders WHERE created_at >= current_date;  -- 43: phantom
```

**Listing 1.** Two counts in one transaction at READ COMMITTED straddle another session's insert — the row set moved.

```d2
direction: right
b1: "B: SELECT ... WHERE p\n42 rows" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
a1: "A: INSERT matching p\ncommit" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
b2: "B: same SELECT\n43 rows: phantom" {
  width: 230
  height: 90
  style.fill: "#ffebee"
}
b1 -> a1 -> b2
```

**Fig. 1.** A phantom is born between two executions of the same predicate query: committed insert, fresh snapshot, different set.

Phantoms bite check-then-act logic across a *set*: "if no invoice exists for this month, create one" — two transactions can both see zero and both create. Cures in order of preference: make the act atomic and unique (a partial unique index `ON invoices (period)` turns the race into a constraint violation and retry), lock the range explicitly (`SELECT ... FOR UPDATE` / InnoDB's automatic gap locks), or run SERIALIZABLE with retry handling.

> [!warning] Snapshot isolation hides phantoms from readers but not from writers
> In PostgreSQL's REPEATABLE READ, B's re-count stays 42 — the anomaly is invisible — but if B then *writes* based on that snapshot, the write can still conflict with A's committed insert and fail with a serialization error. "My REPEATABLE READ transaction saw consistent data" is true and incomplete: the write side is where set-level races resurface, which is why transactions at this level must be retry-safe per [[What is database transaction isolation]].

The full anomaly catalog: [[What problems appear when database transactions run in parallel]]; the row-level sibling: [[What are dirty reads in transaction isolation]]; the applied SQL drill: [[How do you handle transaction isolation anomalies]].

> [!tip] Interview answer
> A phantom read is the same predicate query returning a different row set inside one transaction because another transaction inserted or deleted matching rows — a set-level change, unlike a non-repeatable read's single-row change. READ COMMITTED allows it; snapshot-based REPEATABLE READ hides it from readers (PostgreSQL's blocks it outright, InnoDB also gap-locks the range), and serializable plus retry is the general cure.
