<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS

# How does PostgreSQL handle locks and deadlocks

> [!abstract] Short answer
> **PostgreSQL uses MVCC for readers and row-level locks for writers.** Readers (`SELECT` without `FOR UPDATE/SHARE`) never block on writes and never take row locks; writers (`UPDATE`, `DELETE`, `MERGE`, `SELECT FOR UPDATE`) take a row-level lock on each affected tuple and wait if another transaction holds a conflicting one. Table-level locks coordinate schema and bulk operations. PostgreSQL detects deadlocks automatically using a background process and aborts one transaction with sqlstate `40P01` (`deadlock_detected`); the survivor proceeds and the application is expected to retry the loser.

## The locking model

Three layers cooperate. **MVCC** gives each transaction a snapshot and lets readers see a consistent view without taking locks on the rows they read — a writer's uncommitted version is invisible to other readers, and a writer's lock only matters to other writers and lockers. **Row-level locks** (`FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE`, `FOR KEY SHARE`) protect individual tuples; they are stored in the tuple's `xmax` and a small in-memory multixact structure, never in a global lock table. **Table-level locks** (eight modes from `ACCESS SHARE` up to `ACCESS EXCLUSIVE`) coordinate schema and bulk operations. The same transaction can hold both a row lock and a table lock on the same relation; they don't conflict with themselves.

```d2
direction: down
t1w: "T1: UPDATE row 1\n(row lock on tuple 1)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
t2w: "T2: UPDATE row 2\n(row lock on tuple 2)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
t1w2: "T1: UPDATE row 2\n(blocks — T2 holds the lock)" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
t2w2: "T2: UPDATE row 1\n(blocks — T1 holds the lock)" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
detect: "deadlock detector\n(deadlock_timeout cycle scan)" {
  width: 320
  height: 70
  style.fill: "#fce4ec"
}
abort: "one transaction aborted\nsqlstate 40P01" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
t1w -> t1w2
t2w -> t2w2
t1w2 -> detect: "wait"
t2w2 -> detect: "wait"
detect -> abort
```

**Fig. 1.** Classic two-row deadlock: T1 locks row 1 then waits for row 2; T2 locks row 2 then waits for row 1. The deadlock detector scans the wait-for graph after `deadlock_timeout` and aborts one transaction with `40P01`.

## Deadlock detection, verified on PostgreSQL 17.11

The detector runs after `deadlock_timeout` (1 s by default; lowered to 50 ms in this run). Two threads, each in its own transaction, take a row in opposite order:

```python
import psycopg
import threading

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS dl_demo")
    adm.execute("CREATE TABLE dl_demo (id int PRIMARY KEY, v int)")
    adm.execute("INSERT INTO dl_demo VALUES (1,0),(2,0)")
    adm.execute("ALTER SYSTEM SET deadlock_timeout = '50ms'")
    adm.execute("SELECT pg_reload_conf()")

t1 = psycopg.connect(DSN, autocommit=False)
t2 = psycopg.connect(DSN, autocommit=False)
for c in (t1, t2):
    c.execute("SET deadlock_timeout = '50ms'")
    c.commit()
c1 = t1.cursor(); c2 = t2.cursor()

outcome = {"t1": None, "t2": None}

def tx(c, first, second, who):
    try:
        c.execute("BEGIN")
        c.execute(f"UPDATE dl_demo SET v = v + 1 WHERE id = {first}")
        barrier.wait()
        c.execute(f"UPDATE dl_demo SET v = v + 1 WHERE id = {second}")
        c.connection.commit()
        outcome[who] = ("committed", None, None)
    except psycopg.errors.DeadlockDetected as e:
        c.connection.rollback()
        outcome[who] = ("deadlock", e.sqlstate, str(e).strip().splitlines()[0])
    except Exception as e:
        try: c.connection.rollback()
        except: pass
        outcome[who] = ("err", e.sqlstate, str(e).strip().splitlines()[0])

barrier = threading.Barrier(2, timeout=10)
th1 = threading.Thread(target=tx, args=(c1, 1, 2, "t1"))
th2 = threading.Thread(target=tx, args=(c2, 2, 1, "t2"))
th1.start(); th2.start()
th1.join(timeout=20); th2.join(timeout=20)

print(f"T1 outcome: {outcome['t1']}")
print(f"T2 outcome: {outcome['t2']}")

with psycopg.connect(DSN, autocommit=True) as r:
    cur = r.execute("SELECT id, v FROM dl_demo ORDER BY id")
    for row in cur.fetchall():
        print(f"  row {row[0]}: v={row[1]}")
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
T1 outcome: ('committed', None, None)
T2 outcome: ('deadlock', '40P01', 'deadlock detected')
  row 1: v=1
  row 2: v=1
```
**Listing 2.** Verified on PostgreSQL 17.11 with `deadlock_timeout = 50ms`. T1 wins, T2 is aborted with sqlstate `40P01`. The final table shows each row was updated exactly once — by the winner.

## What causes deadlocks in real code

The trigger is always the same: two or more transactions acquire locks in inconsistent orders. The classic shapes are:

- **Opposite update order across transactions** — T1 updates `accounts 1 then 2`, T2 updates `accounts 2 then 1`. Fix: sort the account ids in the application before issuing `UPDATE`s.
- **Foreign-key cascades** — a parent update that cascades to a child table can lock child rows in a different order than an explicit child update. Fix: order parent and child updates consistently, or batch the parent update.
- **Trigger-driven writes** — a trigger that updates a "summary" row on every detail insert can collide with a concurrent transaction that updates the summary directly.
- **Mixed `SELECT FOR UPDATE` and `UPDATE`** — one transaction locks the row then updates it; another updates first. Fix: pick one order and use it everywhere.

The mitigation is consistent lock ordering plus a retry loop on `40P01` (and the related `40001` serialization failure). Keep transactions short — long-running transactions widen the window for conflicts and stretch `deadlock_timeout` into seconds of wait. `SELECT FOR UPDATE SKIP LOCKED` is the right tool for queue-style workloads where strict ordering does not matter; see [[What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL]].

> [!warning] `deadlock_timeout` is also the wait before logging
> The detector does not fire instantly; it fires after `deadlock_timeout` (default 1 s). Lowering it makes deadlocks abort faster but burns more CPU on cycle scans under load. Raising it means users wait longer before the deadlock is even noticed. The default is a compromise — leave it unless you have measured the cost. The same parameter also controls when the server logs "process N detected deadlock while waiting for transaction" — useful for tracing but noisy if set very low.

> [!warning] Read-only transactions do not deadlock — until they take `FOR UPDATE` locks
> MVCC readers never block on writers and never block other readers, so a pure `SELECT` transaction cannot be in a deadlock. The moment a transaction takes a row lock via `FOR UPDATE`/`FOR SHARE`/`UPDATE`/`DELETE`, it can deadlock. Code that "only reads" but uses `SELECT FOR UPDATE` for pessimistic locking is just as deadlock-prone as write-heavy code; the same ordering rules apply. See [[What is the difference between FOR UPDATE and FOR SHARE in PostgreSQL]] and [[What lock granularities exist in a relational database]].

> [!tip] Interview answer
> PostgreSQL readers use MVCC and don't take locks; writers take row-level locks on the tuples they modify and wait for conflicting locks to release. Table-level locks (eight modes from `ACCESS SHARE` to `ACCESS EXCLUSIVE`) coordinate schema and bulk operations. A background deadlock detector scans the wait-for graph after `deadlock_timeout` and, if it finds a cycle, aborts one transaction with sqlstate `40P01` so the other can proceed. The standard fixes are consistent lock ordering across transactions, short transactions, and a retry loop on `40P01` and `40001`. Related: [[What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL]] and [[How do you handle transaction isolation anomalies]].
