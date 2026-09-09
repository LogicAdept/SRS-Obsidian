<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS

# What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL

> [!abstract] Short answer
> **`FOR UPDATE SKIP LOCKED` locks the rows returned by a `SELECT` and silently skips any row that is already locked by another transaction**, instead of waiting. It is the canonical PostgreSQL primitive for **work-queue tables**: many workers can pull the next free job without blocking each other or competing for the same row. The bare `FOR UPDATE` blocks on a locked row; `FOR UPDATE NOWAIT` raises an error instead of waiting; `FOR UPDATE SKIP LOCKED` skips and continues.

## Three locking policies for `SELECT ... FOR UPDATE`

`FOR UPDATE` is the row-locking clause. The three skip/wait policies answer the same question — what to do when a row is already locked by another transaction:

| Variant | On a locked row |
|---|---|
| `FOR UPDATE` (default) | **wait** until the holder commits or rolls back |
| `FOR UPDATE NOWAIT` | **raise** sqlstate `55P03` (`lock_not_available`) immediately |
| `FOR UPDATE SKIP LOCKED` | **skip** the row and continue the result set |

`SKIP LOCKED` and `NOWAIT` apply to all four row-locking modes (`FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE`, `FOR KEY SHARE`). The skipping is silent — the client sees a result set with the locked rows omitted, no warning, no diagnostic.

```d2
direction: right
queue: "jobq\n1,2,3 (all 'new')" {
  width: 180
  height: 110
  style.fill: "#e3f2fd"
}
wa: "Worker A\nSELECT ... WHERE id=1 FOR UPDATE\n(locks row 1, no commit yet)" {
  width: 360
  height: 110
  style.fill: "#fff3e0"
}
wb: "Worker B\nSELECT ... ORDER BY id\nFOR UPDATE SKIP LOCKED" {
  width: 360
  height: 110
  style.fill: "#e8f5e9"
}
out: "Worker B result: id 2, id 3\n(row 1 silently skipped)" {
  width: 360
  height: 80
  style.fill: "#e8f5e9"
}
queue -> wa
queue -> wb
wb -> out
```

**Fig. 1.** Worker A locks row 1; Worker B issues `FOR UPDATE SKIP LOCKED`. The queue contains rows 1, 2, 3 — Worker B receives rows 2 and 3 with their row locks, silently skipping row 1.

## Work-queue pattern, verified on PostgreSQL 17.11

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS jobq")
    adm.execute("CREATE TABLE jobq (id int PRIMARY KEY, status text)")
    adm.execute("INSERT INTO jobq VALUES (1,'new'),(2,'new'),(3,'new')")

# Worker A locks row 1 and holds the transaction open.
a = psycopg.connect(DSN, autocommit=False)
cur_a = a.execute("SELECT id FROM jobq WHERE id = 1 FOR UPDATE")
cur_a.fetchone()

# Worker B uses SKIP LOCKED: receives rows 2 and 3, skips row 1.
b = psycopg.connect(DSN, autocommit=True)
cur = b.execute("SELECT id FROM jobq WHERE status = 'new' ORDER BY id FOR UPDATE SKIP LOCKED")
print("Worker B with FOR UPDATE SKIP LOCKED (Worker A holds row 1):")
for r in cur.fetchall():
    print(f"  picked row {r[0]}")

# Worker C tries plain FOR UPDATE: would block on row 1.
c = psycopg.connect(DSN, autocommit=False)
c.execute("BEGIN")
try:
    c.execute("SET LOCAL lock_timeout = '100ms'")
    c.execute("SELECT id FROM jobq WHERE status = 'new' ORDER BY id FOR UPDATE")
    c.fetchall()
except psycopg.errors.OperationalError as e:
    print(f"Worker C plain FOR UPDATE: sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")
c.rollback()

# NOWAIT: raises immediately.
try:
    cur = b.execute("SELECT id FROM jobq WHERE status = 'new' ORDER BY id FOR UPDATE NOWAIT")
    cur.fetchall()
except psycopg.errors.LockNotAvailable as e:
    print(f"Worker B FOR UPDATE NOWAIT: sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")

a.rollback(); a.close(); b.close(); c.close()
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
Worker B with FOR UPDATE SKIP LOCKED (Worker A holds row 1):
  picked row 2
  picked row 3
Worker C plain FOR UPDATE: sqlstate=55P03 — canceling statement due to lock timeout
Worker B FOR UPDATE NOWAIT: sqlstate=55P03 — could not obtain lock on row in relation "jobq"
```
**Listing 2.** Verified on PostgreSQL 17.11. Worker B with `SKIP LOCKED` gets rows 2 and 3 — row 1 is silently skipped because Worker A holds it. Plain `FOR UPDATE` would block on row 1; `NOWAIT` raises `55P03` immediately.

## The shape of a safe worker loop

A typical worker transaction is one statement that locks, returns, and updates in the same unit of work:

```sql
BEGIN;
SELECT id FROM jobq
  WHERE status = 'new'
  ORDER BY id
  FOR UPDATE SKIP LOCKED
  LIMIT 10;

UPDATE jobq SET status = 'in_progress'
  WHERE id = ANY($1);  -- ids returned by the SELECT

COMMIT;
```

**Listing 3.** A typical worker-claim transaction: lock up to ten free rows, mark them in-progress, commit. `LIMIT` bounds the working set; the row locks release only on `COMMIT`/`ROLLBACK`.

`LIMIT` matters: without it, `SKIP LOCKED` will scan and lock every free row in the table, starving other workers. `LIMIT N` per transaction keeps the working set bounded. For single-job dispatch, `LIMIT 1` plus `RETURNING` from the `UPDATE` is even cleaner: `UPDATE ... SET status='in_progress' WHERE id = (SELECT id FROM jobq WHERE status='new' ORDER BY id FOR UPDATE SKIP LOCKED LIMIT 1) RETURNING id;` does the lock, the update, and the dispatch in one statement.

> [!warning] `SKIP LOCKED` is silent — order can shift in unexpected ways
> Skipping changes the result set without notice. A `SELECT ... ORDER BY id FOR UPDATE SKIP LOCKED` does not return the first N ids; it returns the first N *unlocked* ids. Code that assumes "the next job is always the smallest id" breaks when a row is locked. Two correct framings: (a) the queue is unordered and any free row is fine, or (b) the order is a hint and locked rows are picked up later. For strict FIFO, use plain `FOR UPDATE` and accept the wait, or use a separate "queue position" column that is never locked.

> [!warning] Skipping rows does not skip `WHERE` clauses or `LIMIT` semantics
> `SKIP LOCKED` applies after the row is identified as a candidate. A `LIMIT 10` with `SKIP LOCKED` may return fewer than 10 rows if some are locked; it does **not** scan further to fill the limit. If you need exactly N rows, loop until you have them or use a `RETURNING`-based `UPDATE ... WHERE id IN (SELECT ... LIMIT N FOR UPDATE SKIP LOCKED)`. Also remember `SKIP LOCKED` works at row level; an `ACCESS EXCLUSIVE` table lock (from `TRUNCATE`, `VACUUM FULL`, many `ALTER TABLE` forms) blocks the whole `SELECT` regardless of `SKIP LOCKED`. See [[What is ACCESS EXCLUSIVE in PostgreSQL]] and [[What is the difference between FOR UPDATE and FOR SHARE in PostgreSQL]].

> [!tip] Interview answer
> `FOR UPDATE SKIP LOCKED` locks the rows returned by a `SELECT` and silently skips rows already locked by another transaction, instead of waiting. It is the standard primitive for work-queue tables in PostgreSQL: many workers can claim the next free job without blocking each other. The bare `FOR UPDATE` waits, `NOWAIT` raises `55P03` immediately, and `SKIP LOCKED` skips. Pair it with `LIMIT` to bound the working set, and keep each worker transaction short. Skipping changes the result set silently, so do not assume FIFO ordering when rows may be locked. Related: [[What is the difference between FOR UPDATE and FOR SHARE in PostgreSQL]] and [[How does PostgreSQL handle locks and deadlocks]].
