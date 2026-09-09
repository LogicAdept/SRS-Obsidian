<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS

# What is the difference between FOR UPDATE and FOR SHARE in PostgreSQL

> [!abstract] Short answer
> **`FOR UPDATE` takes an exclusive row lock** — it blocks other transactions from `UPDATE`, `DELETE`, `FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE`, and `FOR KEY SHARE` on the same row. **`FOR SHARE` takes a shared row lock** — it allows other transactions to take `FOR SHARE` or `FOR KEY SHARE` on the same row concurrently, but still blocks `UPDATE`, `DELETE`, `FOR UPDATE`, and `FOR NO KEY UPDATE`. Both release at `COMMIT`/`ROLLBACK`. Use `FOR UPDATE` when you intend to write; use `FOR SHARE` when you only need the row to stay put while you read related data.

## The four row-level lock modes

PostgreSQL actually has four row-locking clauses, ordered from strongest to weakest:

| Clause | Mode | Blocks |
|---|---|---|
| `FOR UPDATE` | exclusive (full) | `DELETE`, key-changing `UPDATE`, and all four `FOR ...` clauses |
| `FOR NO KEY UPDATE` | exclusive (key-only) | `DELETE`, key-changing `UPDATE`, `FOR UPDATE`, `FOR NO KEY UPDATE` |
| `FOR SHARE` | shared | `DELETE`, key-changing `UPDATE`, `FOR UPDATE`, `FOR NO KEY UPDATE` (allows `FOR SHARE`, `FOR KEY SHARE`) |
| `FOR KEY SHARE` | shared (key-only) | `DELETE`, key-changing `UPDATE` (allows non-key `UPDATE`, `FOR SHARE`, `FOR KEY SHARE`) |

The "key" in `FOR NO KEY UPDATE` and `FOR KEY SHARE` refers to the columns covered by a unique index usable for a foreign key — the columns that, if changed, would break a `REFERENCES` constraint. A non-key `UPDATE` (one that doesn't touch those columns) acquires `FOR NO KEY UPDATE`, the weaker lock, which lets another transaction take `FOR KEY SHARE` concurrently.

```d2
direction: right
fu: "FOR UPDATE\n(exclusive, full)" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
fnku: "FOR NO KEY UPDATE\n(exclusive, key-only)" {
  width: 260
  height: 80
  style.fill: "#ffe0b2"
}
fs: "FOR SHARE\n(shared, full)" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
fks: "FOR KEY SHARE\n(shared, key-only)" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
fu -> fnku -> fs -> fks: "weaker"
```

**Fig. 1.** Four row-locking clauses, strongest to weakest. The two `SHARE` modes allow concurrent holders; the two `UPDATE` modes do not. `FOR KEY SHARE` is narrow enough that a non-key `UPDATE` does not conflict with it — that is how a parent row referenced by a foreign key can be updated for non-key columns while child inserts proceed.

## Verified on PostgreSQL 17.11

Four cases that exercise the matrix: `SHARE` + `SHARE` (both succeed), `SHARE` + `UPDATE`-intent (blocks), `UPDATE` + `SHARE` (blocks), `UPDATE` + plain `UPDATE` (blocks). Each conflict is surfaced via `lock_timeout = 100ms`:

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS fs_demo")
    adm.execute("CREATE TABLE fs_demo (id int PRIMARY KEY, v int)")
    adm.execute("INSERT INTO fs_demo VALUES (1,0)")

t1 = psycopg.connect(DSN, autocommit=False)
t2 = psycopg.connect(DSN, autocommit=False)
c1 = t1.cursor(); c2 = t2.cursor()

# A) FOR SHARE + FOR SHARE: both succeed (shared lock).
c1.execute("BEGIN")
c1.execute("SELECT id FROM fs_demo WHERE id = 1 FOR SHARE")
c1.fetchone()
c2.execute("BEGIN")
c2.execute("SELECT id FROM fs_demo WHERE id = 1 FOR SHARE")
c2.fetchone()
print("FOR SHARE then FOR SHARE  — both acquired (shared lock)")
t1.rollback(); t2.rollback()

# B) FOR SHARE + FOR UPDATE: T2 blocks.
c1.execute("BEGIN")
c1.execute("SELECT id FROM fs_demo WHERE id = 1 FOR SHARE")
c1.fetchone()
try:
    c2.execute("BEGIN")
    c2.execute("SET LOCAL lock_timeout = '100ms'")
    c2.execute("SELECT id FROM fs_demo WHERE id = 1 FOR UPDATE")
    c2.fetchone()
except psycopg.errors.OperationalError as e:
    print(f"FOR SHARE then FOR UPDATE — sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")
t1.rollback(); t2.rollback()

# C) FOR UPDATE + FOR SHARE: T2 blocks.
c1.execute("BEGIN")
c1.execute("SELECT id FROM fs_demo WHERE id = 1 FOR UPDATE")
c1.fetchone()
try:
    c2.execute("BEGIN")
    c2.execute("SET LOCAL lock_timeout = '100ms'")
    c2.execute("SELECT id FROM fs_demo WHERE id = 1 FOR SHARE")
    c2.fetchone()
except psycopg.errors.OperationalError as e:
    print(f"FOR UPDATE then FOR SHARE — sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")
t1.rollback(); t2.rollback()

# D) FOR UPDATE + UPDATE: T2 blocks.
c1.execute("BEGIN")
c1.execute("SELECT id FROM fs_demo WHERE id = 1 FOR UPDATE")
c1.fetchone()
try:
    c2.execute("BEGIN")
    c2.execute("SET LOCAL lock_timeout = '100ms'")
    c2.execute("UPDATE fs_demo SET v = v + 1 WHERE id = 1")
    c2.fetchone()
except psycopg.errors.OperationalError as e:
    print(f"FOR UPDATE then UPDATE    — sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")
t1.rollback(); t2.rollback()
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
FOR SHARE then FOR SHARE  — both acquired (shared lock)
FOR SHARE then FOR UPDATE — sqlstate=55P03 — canceling statement due to lock timeout
FOR UPDATE then FOR SHARE — sqlstate=55P03 — canceling statement due to lock timeout
FOR UPDATE then UPDATE    — sqlstate=55P03 — canceling statement due to lock timeout
```
**Listing 2.** Verified on PostgreSQL 17.11: `FOR SHARE` allows another `FOR SHARE` concurrently (shared), but conflicts with `FOR UPDATE` and plain `UPDATE`. `FOR UPDATE` conflicts with everything: another `FOR SHARE`, a plain `UPDATE`, even another `FOR UPDATE` (not shown, but symmetric).

## When to pick which

The decision is: do you intend to write the row, or just keep it from changing while you read something else?

- **`FOR UPDATE`** — you will modify or delete the row in this transaction. The default for `UPDATE`/`DELETE` internally; explicit when you want to lock now, decide later, then update.
- **`FOR NO KEY UPDATE`** — you will update the row but not its key columns. Acquired automatically by a non-key `UPDATE`; rarely written explicitly.
- **`FOR SHARE`** — you need the row to stay put (no update, no delete) while you read related data and make a decision. The classic case is "lock the parent row while I check the children" before deciding whether to insert a new child.
- **`FOR KEY SHARE`** — you only need the key columns to stay stable. Acquired automatically by a foreign-key check on the parent row; rarely written explicitly.

`SKIP LOCKED` and `NOWAIT` apply to all four modes. The lock granularity is per-row, not per-statement: a `SELECT FOR UPDATE` that matches 100 rows holds 100 row locks, not one. See [[What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL]] for the worker-pool pattern.

> [!warning] `FOR SHARE` is not "SELECT with a read lock"
> Calling `FOR SHARE` "a read lock" is the most common interview mistake. It is a **shared row lock** that blocks writers and `FOR UPDATE`/`FOR NO KEY UPDATE` on the same row. It does not block readers — pure `SELECT` never blocks in PostgreSQL because of MVCC. The "share" is about multiple transactions holding the lock at once, not about reading. The use case is "I depend on this row staying as-is while I look at other things"; the misuse is treating it as a "make my SELECT safer" knob, which it is not.

> [!warning] `FOR UPDATE` on a join locks every row from every locked table
> `SELECT ... FROM a JOIN b ... FOR UPDATE` locks all matched rows from both `a` and `b` unless you use `FOR UPDATE OF a` to limit the lock to one table. Locking more than you need is the standard cause of lock-contention surprises in join-heavy code. The same applies to views — `FOR UPDATE` of a view locks every underlying row that contributed to the result. Use `FOR UPDATE OF <alias>` to be explicit.

> [!tip] Interview answer
> `FOR UPDATE` is an exclusive row lock — it blocks other writers, `FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE`, and `FOR KEY SHARE` on the same row. `FOR SHARE` is a shared row lock — it allows concurrent `FOR SHARE`/`FOR KEY SHARE` but still blocks `UPDATE`, `DELETE`, `FOR UPDATE`, and `FOR NO KEY UPDATE`. Use `FOR UPDATE` when you intend to write the row, `FOR SHARE` when you only need it to stay put while you read related data. Both release at transaction end. The "key" variants narrow the lock to key columns, which is how PostgreSQL lets a parent row be updated for non-key columns while foreign-key checks proceed. Related: [[What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL]] and [[How does PostgreSQL handle locks and deadlocks]].
