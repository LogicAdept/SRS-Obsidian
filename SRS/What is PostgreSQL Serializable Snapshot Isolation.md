<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS

# What is PostgreSQL Serializable Snapshot Isolation

> [!abstract] Short answer
> **PostgreSQL's `SERIALIZABLE` is Repeatable Read plus predicate-conflict detection — the algorithm known academically as Serializable Snapshot Isolation (SSI).** It keeps the snapshot semantics of RR (one snapshot per transaction, no phantoms, no non-repeatable reads) and adds **predicate locks** that record which rows a transaction read. If a concurrent write would have changed the result of an earlier read in another serializable transaction, the database aborts one of them with sqlstate `40001` (`serialization_failure`). The application is expected to retry the aborted transaction.

## What SSI adds on top of Snapshot Isolation

`REPEATABLE READ` in PostgreSQL is Snapshot Isolation — it prevents dirty reads, non-repeatable reads, and phantoms, but it allows the **serialization anomaly**: a result that no serial execution of the same transactions could produce. The classic shape is **write skew**:

- T1 reads "count of doctors on call = 2", decides "I can go off call", sets itself off-call, commits.
- T2 reads "count of doctors on call = 2", decides "I can go off call", sets itself off-call, commits.
- Neither overwrote the other's row, so neither blocked. Final state: 0 doctors on call — but no serial order produces this (in any serial order, the second reader would see 1 on-call doctor and stay on call).

SSI catches this. PostgreSQL tracks predicate reads (technically, `SIReadLock` entries in `pg_locks`) and, at commit time, checks whether the reads would still be valid given concurrent writes. If not, one of the transactions is aborted with `40001`. The locks do not block; they are bookkeeping that lets the database prove or disprove serializability.

```d2
direction: down
rr: "REPEATABLE READ = Snapshot Isolation\nno dirty / non-repeatable / phantom reads\nstill allows serialization anomaly" {
  width: 460
  height: 90
  style.fill: "#fff3e0"
}
ser: "SERIALIZABLE = SSI\nRR + predicate-conflict detection\naborts one tx with 40001 on conflict" {
  width: 460
  height: 90
  style.fill: "#e8f5e9"
}
retry: "application retries the aborted tx\n(fresh snapshot on second attempt)" {
  width: 460
  height: 80
  style.fill: "#e3f2fd"
}
rr -> ser: "add SSI"
ser -> retry: "on 40001"
```

**Fig. 1.** `SERIALIZABLE` = RR + predicate tracking. The locks do not block; they let the database decide at commit time whether the concurrent execution is equivalent to some serial order. When it is not, one transaction is aborted and the application retries it.

## Write skew under RR vs SSI, verified on PostgreSQL 17.11

Reproduces the canonical example from the PostgreSQL manual (`transaction-iso.html` §13.2.3). A table has rows `class=1: 10, 20` and `class=2: 100, 200`. Two concurrent transactions:

- T_A computes `SUM(value) WHERE class=1` (=30) and inserts a new row `class=2, value=30`.
- T_B computes `SUM(value) WHERE class=2` (=300) and inserts a new row `class=1, value=300`.

In any serial order, the second transaction's sum would have included the first's insert — so the concurrent result is not serializable.

```python
import psycopg
import threading

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS mytab")
    adm.execute("CREATE TABLE mytab (class int, value int)")
    adm.execute("INSERT INTO mytab VALUES (1,10),(1,20),(2,100),(2,200)")

def run_pair(iso):
    barrier = threading.Barrier(2, timeout=10)
    res = {"a": None, "b": None}

    def worker(side, other_class, my_value):
        conn = psycopg.connect(DSN, autocommit=False)
        try:
            cur = conn.cursor()
            cur.execute(f"BEGIN ISOLATION LEVEL {iso}")
            cur.execute(f"SELECT SUM(value) FROM mytab WHERE class = {other_class}")
            s = cur.fetchone()[0]
            barrier.wait()
            my_class = 2 if side == "a" else 1
            cur.execute("INSERT INTO mytab VALUES (%s, %s)", (my_class, s))
            cur.execute("COMMIT")
            res[side] = ("committed", None, f"read sum={s} from class={other_class}, inserted class={my_class} value={s}")
        except psycopg.errors.SerializationFailure as e:
            try: conn.rollback()
            except: pass
            res[side] = ("aborted", e.sqlstate, str(e).strip().splitlines()[0])
        finally:
            conn.close()

    th_a = threading.Thread(target=worker, args=("a", 1, 30))
    th_b = threading.Thread(target=worker, args=("b", 2, 300))
    th_a.start(); th_b.start()
    th_a.join(timeout=15); th_b.join(timeout=15)
    return res

print("REPEATABLE READ:  T_A={}  T_B={}".format(*[run_pair("REPEATABLE READ")[k] for k in ("a","b")]))

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("TRUNCATE mytab")
    adm.execute("INSERT INTO mytab VALUES (1,10),(1,20),(2,100),(2,200)")

print("SERIALIZABLE:      T_A={}  T_B={}".format(*[run_pair("SERIALIZABLE")[k] for k in ("a","b")]))
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
REPEATABLE READ:  T_A=('committed', None, 'read sum=30 from class=1, inserted class=2 value=30')  T_B=('committed', None, 'read sum=300 from class=2, inserted class=1 value=300')
SERIALIZABLE:      T_A=('aborted', '40001', 'could not serialize access due to read/write dependencies among transactions')  T_B=('committed', None, 'read sum=300 from class=2, inserted class=1 value=300')
```
**Listing 2.** Verified on PostgreSQL 17.11. Under `REPEATABLE READ` both transactions commit — write skew slips through, and the result is not achievable by any serial order. Under `SERIALIZABLE`, SSI detects the read/write dependency and aborts one transaction with sqlstate `40001`; the survivor commits.

## Performance and operational notes

SSI monitoring is cheaper than the table-level locks an RC/RR transaction would need to enforce the same guarantee, but it is not free. Each read may install `SIReadLock` entries; under memory pressure the database combines them into coarser-grained relation-level predicate locks, which can increase the abort rate. Tuning knobs are `max_pred_locks_per_transaction`, `max_pred_locks_per_relation`, and `max_pred_locks_per_page`. A sequential scan always takes a relation-level predicate lock, so a `SERIALIZABLE` transaction that does a seq scan on a busy table will see more aborts than the same query with an index scan. Indexing the predicates SSI tracks is the most reliable performance lever.

Deferrable read-only serializable transactions are a special case: `BEGIN ISOLATION LEVEL SERIALIZABLE READ ONLY DEFERRABLE` waits until it can acquire a snapshot guaranteed to be safe (no possible SSI conflicts) before running. This is the only case where a serializable transaction blocks when an RR transaction would not.

> [!warning] SSI prevents anomalies; it does not prevent unique-constraint violations
> Even under `SERIALIZABLE`, two transactions that both check "does this key exist?" and then insert it can both fail with a unique-constraint violation, because the unique index is enforced before SSI's commit-time check. The PostgreSQL docs spell this out: "it is possible to see unique constraint violations caused by conflicts with overlapping Serializable transactions even after explicitly checking that the key isn't present before attempting to insert it." The fix is to either let the constraint catch it (and retry on `23505`) or to use explicit `SELECT ... FOR UPDATE` on the parent row to serialize inserts.

> [!warning] Retry on `40001`, but only on `40001`
> SSI aborts come back with sqlstate `40001`. So do RR's "could not serialize access due to concurrent update" errors. Both are retryable — re-execute the whole transaction with a fresh snapshot. Other sqlstates (lock timeout `55P03`, deadlock `40P01`, unique violation `23505`) need different handling: `40P01` is also retryable, `55P03` may be retried but usually points to a hot row that needs redesign, `23505` is a logic error. Catching `40001` too broadly (e.g. blanket retry on any `SQLException`) hides real bugs. See [[How do you handle transaction isolation anomalies]] and [[What are SQL transaction isolation levels]].

> [!tip] Interview answer
> PostgreSQL's `SERIALIZABLE` is implemented as Serializable Snapshot Isolation: Repeatable Read (snapshot isolation) plus predicate-conflict detection. The snapshot prevents dirty, non-repeatable, and phantom reads; predicate locks — `SIReadLock` entries in `pg_locks` — record what each transaction read, and at commit time the database checks whether concurrent writes would have changed those reads. If they would, one transaction is aborted with sqlstate `40001`. The classic example is write skew: two doctors both go off-call because both saw "two on call" — RR allows it, SSI aborts one. The application is expected to retry the aborted transaction. Related: [[How does Repeatable Read prevent phantom reads in PostgreSQL]] and [[How do you handle transaction isolation anomalies]].
