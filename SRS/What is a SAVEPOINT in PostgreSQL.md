<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS

# What is a SAVEPOINT in PostgreSQL

> [!abstract] Short answer
> **`SAVEPOINT` establishes a named mark inside the current transaction** so a later `ROLLBACK TO SAVEPOINT` undoes only the work done after that mark, keeping the outer transaction open. Use it to retry a single statement or a sub-step without aborting the whole unit of work. Savepoints exist only inside a transaction block; they are released at `COMMIT`/`ROLLBACK` and can be nested.

## Syntax and the lifecycle of a mark

```sql
SAVEPOINT savepoint_name
ROLLBACK TO [SAVEPOINT] savepoint_name
RELEASE SAVEPOINT savepoint_name
```

**Listing 1.** The three savepoint-related statements. `SAVEPOINT` creates the mark, `ROLLBACK TO SAVEPOINT` rewinds to it, `RELEASE SAVEPOINT` destroys it while keeping the post-savepoint work.

A `SAVEPOINT` is a transaction-control statement, not a separate transaction. `ROLLBACK TO SAVEPOINT` rolls the transaction state back to the mark — rows inserted after the mark are gone, locks acquired after the mark are released, sequences keep advancing — but the transaction itself stays open and you must still issue a final `COMMIT` or `ROLLBACK`. `RELEASE SAVEPOINT` destroys the mark while keeping the post-savepoint work; the name becomes free for reuse (with the caveat on same-name stacks below).

```d2
direction: right
begin: "BEGIN" {
  width: 120
  height: 60
  style.fill: "#e3f2fd"
}
ins1: "INSERT v=1" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}
sp: "SAVEPOINT my_sp" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
ins2: "INSERT v=2" {
  width: 140
  height: 60
  style.fill: "#ffebee"
}
rb: "ROLLBACK TO SAVEPOINT my_sp" {
  width: 280
  height: 60
  style.fill: "#ffebee"
}
ins3: "INSERT v=3" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}
commit: "COMMIT" {
  width: 120
  height: 60
  style.fill: "#e3f2fd"
}
begin -> ins1 -> sp -> ins2 -> rb -> ins3 -> commit
```

**Fig. 1.** A savepoint marks a point in the transaction. `ROLLBACK TO SAVEPOINT` rewinds to that mark — the second insert is undone, the third insert and the outer transaction survive.

## The docs example, run on PostgreSQL 17

The canonical illustration from the PostgreSQL manual, executed against PostgreSQL 17.11 with two extra cases — `RELEASE SAVEPOINT` and the same-name stack:

```python
# psycopg3 against PostgreSQL 17.11 on a local socket
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS table1")
    adm.execute("CREATE TABLE table1 (val int)")

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("BEGIN")
    cur.execute("INSERT INTO table1 VALUES (1)")
    cur.execute("SAVEPOINT my_savepoint")
    cur.execute("INSERT INTO table1 VALUES (2)")
    cur.execute("ROLLBACK TO SAVEPOINT my_savepoint")
    cur.execute("INSERT INTO table1 VALUES (3)")
    cur.execute("COMMIT")
    cur.execute("SELECT val FROM table1 ORDER BY val")
    for r in cur.fetchall():
        print(f"  {r[0]}")
```

**Listing 2.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
after ROLLBACK TO SAVEPOINT then COMMIT:
  1
  3
after RELEASE SAVEPOINT keeps post-savepoint work:
  3
  3
  4
after second SAVEPOINT then ROLLBACK TO (uses most recent):
  1
  2
after RELEASE then ROLLBACK TO (now reaches the first savepoint):
  1
```
**Listing 3.** Verified on PostgreSQL 17.11: `ROLLBACK TO SAVEPOINT` discards only the second insert; `RELEASE SAVEPOINT` keeps the post-savepoint work; same-name savepoints stack, with the most recent one selected by `ROLLBACK TO` until `RELEASE` exposes the older mark.

## Same-name savepoints stack

The SQL standard says a new savepoint with the same name destroys the old one. PostgreSQL extends this: the old savepoint is kept, but it is shadowed until the newer one is released. `ROLLBACK TO SAVEPOINT` and `RELEASE SAVEPOINT` always target the most recent matching mark. After `RELEASE`, the previously shadowed mark is reachable again. This is the only material deviation from the standard, and it is documented.

## When savepoints earn their keep

The two production patterns are partial retry and procedural recovery. In a loop that inserts N children, wrapping each iteration in a savepoint lets one bad row abort just that iteration instead of the whole transaction — the outer transaction stays usable. In PL/pgSQL, an `EXCEPTION` block implicitly creates a savepoint; entering the handler rolls back to that subtransaction, which is how a caught `unique_violation` keeps the surrounding work alive. Heavy use as a substitute for correct control flow is a smell — each savepoint has bookkeeping cost, and stacking hundreds without releasing them bloats the lock table and complicates debugging.

> [!warning] `ROLLBACK TO SAVEPOINT` does not release the transaction
> It rewinds to the mark, but the outer transaction is still open and still holds its locks. You still have to issue a final `COMMIT` (or `ROLLBACK`) — otherwise the connection stays `idle in transaction` and the server keeps every lock the transaction holds. The same applies to locks acquired after the savepoint: they are released by `ROLLBACK TO SAVEPOINT`, but locks acquired before the mark stay held.

> [!warning] Sequences and `COMMIT`-side effects are not undone
> `ROLLBACK TO SAVEPOINT` rolls back row changes and post-savepoint locks, but `nextval` of a sequence is not transactional — the consumed value is gone. Same for `LISTEN`/`NOTIFY` payloads already queued: `NOTIFY` is transactional (the payload is sent on `COMMIT`), so a savepoint rollback cancels it cleanly, but anything that escaped the transaction before the savepoint (cursor moves, side effects in `C`-level functions, writes to external systems) is not reversed. See [[How would you explain the SQL COMMIT statement for transactions]] for what `COMMIT` makes durable.

> [!tip] Interview answer
> `SAVEPOINT` is a named mark inside a transaction. `ROLLBACK TO SAVEPOINT` undoes only the work done after the mark, leaving the transaction open for further work; `RELEASE SAVEPOINT` destroys the mark while keeping that work. The classic use is partial retry: one bad iteration in a loop rolls back to the savepoint instead of aborting the whole transaction. PostgreSQL extends the standard by stacking same-name savepoints, with the most recent one targeted until released. Related: [[How does PostgreSQL handle locks and deadlocks]] and [[What are SQL transaction isolation levels]].
