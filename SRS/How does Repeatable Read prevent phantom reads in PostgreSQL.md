<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS

# How does Repeatable Read prevent phantom reads in PostgreSQL

> [!abstract] Short answer
> **PostgreSQL `REPEATABLE READ` uses one snapshot for the entire transaction**, taken at the first non-transaction-control statement. Subsequent `SELECT`s in that transaction see the same set of rows, so a row another transaction inserts and commits after ours started is invisible — no phantom read. This is stronger than the SQL standard requires (the standard allows phantoms at RR); the standard anomaly that PG's RR still permits is the serialization anomaly, blocked only at `SERIALIZABLE`.

## Snapshot isolation, not locking

The SQL standard defines `REPEATABLE READ` by what it forbids: dirty read, non-repeatable read. Phantom reads are *allowed* at RR under the standard. PostgreSQL implements RR as Snapshot Isolation: instead of re-running every query against the latest committed state, the transaction freezes a snapshot at the first statement and uses it for every subsequent query. A row inserted by another transaction after the snapshot is simply not in it — not blocked, not waited for, just invisible. The same logic prevents non-repeatable reads: a re-read returns the same value because the snapshot hasn't moved.

```d2
direction: right
start: "T1 BEGIN ISOLATION LEVEL REPEATABLE READ\n(snapshot taken at first SELECT)" {
  width: 360
  height: 80
  style.fill: "#e3f2fd"
}
q1: "T1 SELECT count(*)\n-> 1 (sees row from snapshot)" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
t2: "T2 INSERT (2); COMMIT" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
q2: "T1 SELECT count(*)\n-> still 1 (snapshot frozen)" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
end: "T1 COMMIT" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
start -> q1 -> q2 -> end
q1 -> t2: "concurrent"
t2 -> q2: "invisible to T1"
```

**Fig. 1.** T1's snapshot is frozen at its first query. T2's insert commits, but T1's second `count(*)` reads the snapshot, not the live table — no phantom appears. Under SQL-standard RR the new row would be visible at the second read.

## Verified on PostgreSQL 17.11

Two transactions, one table with one row at the start. T1 opens an RR transaction and reads the count; T2 inserts a row and commits; T1 reads the count again:

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS rr_demo")
    adm.execute("CREATE TABLE rr_demo (id int)")
    adm.execute("INSERT INTO rr_demo VALUES (1)")

t1 = psycopg.connect(DSN, autocommit=False)
t2 = psycopg.connect(DSN, autocommit=False)
c1 = t1.cursor(); c2 = t2.cursor()

c1.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
c1.execute("SELECT count(*) FROM rr_demo")
print(f"T1 first  count at RR: {c1.fetchone()[0]}")

c2.execute("BEGIN")
c2.execute("INSERT INTO rr_demo VALUES (2)")
c2.execute("COMMIT")

c1.execute("SELECT count(*) FROM rr_demo")
print(f"T1 second count at RR: {c1.fetchone()[0]}  (phantom not visible — PG RR uses one snapshot)")

c1.execute("COMMIT")
c1.execute("BEGIN ISOLATION LEVEL READ COMMITTED")
c1.execute("SELECT count(*) FROM rr_demo")
print(f"T1 then    count at RC: {c1.fetchone()[0]}  (new row visible under RC)")

c1.execute("COMMIT")
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
T1 first  count at RR: 1
T1 second count at RR: 1  (phantom not visible — PG RR uses one snapshot)
T1 then    count at RC: 2  (new row visible under RC)
```
**Listing 2.** Verified on PostgreSQL 17.11: under `REPEATABLE READ`, the second `count(*)` returns 1 even though T2 committed an insert between the two reads — the snapshot is frozen. After T1 commits and re-opens at `READ COMMITTED`, the new row becomes visible.

## What RR still allows: the serialization anomaly

A frozen snapshot does not guarantee that the committed outcome is equivalent to some serial order of the concurrent transactions. The classic example is **write skew**: two transactions each read a shared predicate, decide a local action is safe, and commit. Neither overwrites the other's row, so neither waits; both commit. The result is not achievable by any serial order. PostgreSQL's RR allows this. The defense is `SERIALIZABLE` (which adds SSI predicate tracking and aborts one transaction with sqlstate `40001`), explicit `SELECT FOR UPDATE` locks, or an application-level constraint.

A second, narrower hazard: an RR transaction that tries to `UPDATE` or `DELETE` a row modified by a concurrent committed transaction is aborted with `ERROR: could not serialize access due to concurrent update` (sqlstate `40001`). Read-only RR transactions never see this; only writers do. The recovery is the same as for SSI: rollback and retry the whole transaction.

> [!warning] Repeatable Read in PostgreSQL is Snapshot Isolation, not the SQL-standard RR
> Two implications interviewers probe. First, "PG RR is stricter than standard RR" is true only for *phantoms*: PG also prevents non-repeatable reads (snapshot) but still allows the serialization anomaly. Second, the snapshot is taken at the **first non-transaction-control statement**, not at `BEGIN`. A `BEGIN` followed by ten minutes of idle is fine; the snapshot is set when the first `SELECT`/`INSERT`/etc. runs, not when `BEGIN` was issued. Confusing these makes people think RR holds a fresher snapshot than it does. See [[What are SQL transaction isolation levels]] and [[What is PostgreSQL Serializable Snapshot Isolation]].

> [!warning] First-updater-wins aborts the second RR writer
> Under PG RR, if T1 reads a row, T2 updates and commits, then T1 tries to update the same row, T1 is aborted with `could not serialize access due to concurrent update` (sqlstate `40001`). T1 cannot see T2's new version (snapshot is frozen) but also cannot overwrite it. This is different from `READ COMMITTED`, where T1 would wait for T2, then update the latest committed version. The retry loop is the same one used for SSI: abort, re-execute, succeed on the second attempt against a fresh snapshot.

> [!tip] Interview answer
> PostgreSQL's `REPEATABLE READ` is implemented as Snapshot Isolation: the transaction takes one snapshot at its first statement and reads from it for the rest of the transaction, so rows inserted by other transactions after that point are invisible — phantoms cannot occur. This is stronger than the SQL standard, which permits phantoms at RR. What PG's RR still allows is the serialization anomaly (write skew), and a writer that hits a row already modified by a concurrent committed transaction is aborted with `40001`. For full serializability use `SERIALIZABLE`, which adds SSI predicate tracking. Related: [[What are SQL transaction isolation levels]] and [[How do you handle transaction isolation anomalies]].
