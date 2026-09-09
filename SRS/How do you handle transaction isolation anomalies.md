<!--
reps: 0
priority: 0
-->
#Databases/SQL/Transactions #SRS

# How do you handle transaction isolation anomalies

> [!abstract] Short answer
> **An isolation anomaly is a concurrency effect the SQL standard names** — dirty read, non-repeatable read, phantom read, serialization anomaly — **plus the implementation-defined conflicts that arise under snapshot isolation and SSI** (lost update, write skew, first-updater-wins abort). The handling is uniform: pick the weakest isolation level that the correctness requirement permits, then **wrap each unit of work in a retry loop that re-executes the entire transaction when the database aborts it with a retryable sqlstate** (`40001` serialization failure, `40P01` deadlock, `55P03` lock timeout if you choose to retry). For anomalies the isolation level does not prevent, add explicit locks or schema-level constraints.

## Anomaly catalog and the standard answer

The SQL standard names four phenomena. Each has a standard remedy (a higher isolation level) and an implementation-specific remedy (a lock, a constraint, or a different access pattern).

| Anomaly | Definition | Minimum isolation that prevents it | PostgreSQL-specific notes |
|---|---|---|---|
| Dirty read | T2 reads T1's uncommitted change | `READ COMMITTED` | impossible in PG — MVCC never returns uncommitted versions |
| Non-repeatable read | T1 re-reads a row and sees a different value | `REPEATABLE READ` | PG's RR (snapshot isolation) prevents it via a frozen snapshot |
| Phantom read | T1 re-runs a predicate query and sees extra rows | `REPEATABLE READ` (PG) / `SERIALIZABLE` (standard) | PG's RR prevents phantoms too — stronger than the standard requires |
| Serialization anomaly | the committed outcome is not equivalent to any serial order | `SERIALIZABLE` | PG's SSI aborts one transaction with `40001`; RR allows the anomaly (e.g. write skew) |

Two non-standard but practically important anomalies: **lost update** (two transactions read-then-write the same row; one update silently overwrites the other) and **write skew** (each transaction's local decision is safe given its snapshot, but the combined result is not serializable). PostgreSQL's RR prevents lost update by aborting the second writer with `40001` "could not serialize access due to concurrent update"; RR does not prevent write skew. SERIALIZABLE prevents both.

```d2
direction: down
iso: "pick the weakest isolation that the correctness requirement permits" {
  width: 480
  height: 70
  style.fill: "#e3f2fd"
}
retry: "wrap each tx in a retry loop on sqlstate 40001 / 40P01" {
  width: 480
  height: 70
  style.fill: "#fff3e0"
}
extra: "for anomalies the isolation level does not prevent:\nexplicit FOR UPDATE, schema constraints, application-level invariant" {
  width: 480
  height: 90
  style.fill: "#e8f5e9"
}
iso -> retry -> extra
```

**Fig. 1.** The three layers of defense: choose isolation deliberately, retry on the well-known retryable sqlstates, and use explicit locks or constraints for what the isolation level still allows.

## Retry loop pattern, verified on PostgreSQL 17.11

The canonical pattern is a `while True` that re-executes the whole transaction on `40001`. The example is the "two doctors on call" write-skew scenario under `SERIALIZABLE`: both transactions see "2 on call" and decide to go off-call; SSI aborts one with `40001`; the loser retries and on the second attempt reads "1 on call" (the survivor's update is now visible) and decides to stay on call:

```python
import psycopg
import threading

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS doctors")
    adm.execute("CREATE TABLE doctors (id int PRIMARY KEY, on_call boolean)")
    adm.execute("INSERT INTO doctors VALUES (1, true),(2, true)")
    adm.execute("DROP TABLE IF EXISTS attempt_log")
    adm.execute("CREATE TABLE attempt_log (worker text, attempt int, outcome text)")

def worker(name, my_id, ready, go):
    attempt = 0
    while True:
        attempt += 1
        ready[threading.current_thread()] = True
        go.wait(timeout=10); go.clear()
        conn = psycopg.connect(DSN, autocommit=False)
        try:
            cur = conn.cursor()
            cur.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
            cur.execute("SELECT count(*) FROM doctors WHERE on_call AND id <> %s", (my_id,))
            n = cur.fetchone()[0]
            if n >= 1:
                cur.execute("UPDATE doctors SET on_call = false WHERE id = %s", (my_id,))
                outcome = "went off-call"
            else:
                outcome = "stay on-call"
            cur.execute("COMMIT")
            with psycopg.connect(DSN, autocommit=True) as log:
                log.execute("INSERT INTO attempt_log VALUES (%s,%s,%s)", (name, attempt, outcome + " committed"))
            return
        except psycopg.errors.SerializationFailure as e:
            conn.rollback()
            with psycopg.connect(DSN, autocommit=True) as log:
                log.execute("INSERT INTO attempt_log VALUES (%s,%s,%s)", (name, attempt, f"aborted {e.sqlstate} retrying"))
            if attempt > 5:
                return
        finally:
            conn.close()

import time
go = threading.Event(); ready = {}
th1 = threading.Thread(target=worker, args=("A", 1, ready, go))
th2 = threading.Thread(target=worker, args=("B", 2, ready, go))
th1.start(); th2.start()
for _ in range(6):
    for _ in range(100):
        if th1 in ready and th2 in ready and ready[th1] and ready[th2]:
            break
        time.sleep(0.01)
    ready.clear(); ready[th1] = False; ready[th2] = False
    go.set()
    time.sleep(0.3)
    if not th1.is_alive() and not th2.is_alive():
        break
th1.join(timeout=10); th2.join(timeout=10)

with psycopg.connect(DSN, autocommit=True) as r:
    cur = r.execute("SELECT worker, attempt, outcome FROM attempt_log ORDER BY attempt, worker")
    print("attempt log:")
    for row in cur.fetchall():
        print(f"  {row[0]} attempt {row[1]}: {row[2]}")
    cur = r.execute("SELECT id, on_call FROM doctors ORDER BY id")
    print("final state:")
    for row in cur.fetchall():
        print(f"  doctor {row[0]}: on_call={row[1]}")
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
attempt log:
  A attempt 1: went off-call committed
  B attempt 1: aborted 40001 retrying
  B attempt 2: stay on-call committed
final state:
  doctor 1: on_call=False
  doctor 2: on_call=True
```
**Listing 2.** Verified on PostgreSQL 17.11: both workers see "2 on call" on the first attempt; SSI lets one commit and aborts the other with `40001`. The loser retries on a fresh snapshot, sees "1 on call" (the survivor's update is now visible), and stays on call. Final state — exactly one doctor on call — is achievable by a serial execution.

## Choosing defenses beyond retry

Retry handles the conflicts the database surfaces. Some anomalies need extra defense because the isolation level does not flag them or because retry is too expensive:

- **`SELECT FOR UPDATE` for "read-then-write" on a known row.** Pessimistic; takes an exclusive row lock so the second transaction waits. Use when contention is low and the cost of a retry is high.
- **`SELECT FOR UPDATE SKIP LOCKED` for queue dispatch.** Avoids the wait entirely by skipping locked rows; see [[What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL]].
- **Unique constraints for "insert if absent".** `INSERT ... ON CONFLICT DO NOTHING` makes the "is this key present?" check atomic with the insert, so two transactions cannot both succeed. SSI does not prevent unique-constraint violations even under SERIALIZABLE.
- **Check constraints and triggers for invariant rules.** The "at least one doctor on call" rule belongs as a constraint if the database supports it (PostgreSQL does not natively, but a deferred trigger or a materialized "count" table with a CHECK can enforce it).
- **Application-level locks** (advisory locks) for cross-table invariants that cannot be expressed as a single row lock.

> [!warning] Retry only the retryable sqlstates
> The pattern is to retry on `40001` (`serialization_failure`), `40P01` (`deadlock_detected`), and optionally `55P03` (`lock_not_available`) when you set `lock_timeout`. Other sqlstates — `23505` unique violation, `23503` foreign-key violation, `23514` check violation, `40002` transaction integrity constraint violation — are **not** retryable; they signal a logic error and retrying will hit the same error. The standard mistake is `catch (SQLException e) { retry(); }`, which masks real bugs and turns a logic error into an infinite loop. Inspect `getSQLState()` and retry only the conflict-class codes.

> [!warning] The retry must re-execute the entire transaction, not just the failing statement
> SSI and deadlock aborts roll back the **whole transaction** — locks, savepoints, snapshot. Retrying just the last `UPDATE` from the catch site will not work; the connection is no longer in a transaction. Re-run from the `BEGIN`, re-read the data, re-decide, re-write, re-commit. Code that holds the snapshot in application memory across the retry (e.g. caching a `count(*)` result) bypasses SSI's protection and re-introduces the anomaly. See [[What is PostgreSQL Serializable Snapshot Isolation]] and [[How does PostgreSQL handle locks and deadlocks]].

> [!warning] Retrying forever is its own outage
> Under heavy contention, retrying indefinitely can livelock — the same transaction keeps losing the SSI race. Bound the retry count (5–10 is typical), and on the final failure propagate the error to the caller. The same applies to `40P01`: a sustained deadlock pattern points to a missing index or a lock-ordering bug, and retrying forever just hides it.

> [!tip] Interview answer
> Isolation anomalies are handled in three layers: pick the weakest isolation level the correctness requirement allows, wrap each unit of work in a retry loop that re-executes the whole transaction on retryable sqlstates (`40001` serialization failure, `40P01` deadlock, optionally `55P03` lock timeout), and use explicit `FOR UPDATE` locks, unique constraints, or application-level invariants for what the isolation level still allows. Retry must re-execute from `BEGIN`, must be bounded, and must not catch non-retryable sqlstates like `23505`. Under PostgreSQL SERIALIZABLE, SSI surfaces write skew as `40001` and the retry loop converges naturally. Related: [[What are SQL transaction isolation levels]] and [[What is PostgreSQL Serializable Snapshot Isolation]].
