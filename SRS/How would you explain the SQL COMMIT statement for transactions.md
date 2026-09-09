<!--
reps: 0
priority: 0
-->
#Databases/SQL/Transactions #SRS

# How would you explain the SQL COMMIT statement for transactions

> [!abstract] Short answer
> **`COMMIT` ends the current transaction and makes all its changes durable and visible to other transactions.** It releases every lock the transaction held, closes any open cursors, drops temporary savepoints, and emits a warning if issued outside a transaction. The `AND CHAIN` clause (a PostgreSQL extension also in the SQL standard) starts a new transaction with the same isolation level, access mode, and deferrable flag as the one just committed.

## What `COMMIT` does, exactly

Inside a transaction block opened by `BEGIN` (or implicitly by the first data statement in autocommit-off mode), `COMMIT` performs four things atomically from the application's perspective:

1. **Durability.** The transaction's WAL (write-ahead log) records are flushed to disk according to `synchronous_commit` (`on` by default; `off` lets the commit return before the WAL is durable). Once `COMMIT` returns successfully, the changes survive a crash.
2. **Visibility.** Rows inserted/updated/deleted by the transaction become visible to other transactions whose snapshots start after the commit. Transactions that already have a snapshot (RR/SERIALIZABLE) still don't see the changes — they have a frozen snapshot.
3. **Lock release.** Every row-level lock, table-level lock, and advisory transaction-level lock held by the transaction is released. Session-level advisory locks and session-level settings survive.
4. **Resource cleanup.** Open cursors are closed, prepared statements remain valid (they are session-scoped, not transaction-scoped), temporary savepoints vanish, and `LISTEN` channels registered during the transaction stay registered (`LISTEN` is session-scoped).

```d2
direction: right
begin: "BEGIN" {
  width: 120
  height: 60
  style.fill: "#e3f2fd"
}
work: "INSERT / UPDATE / DELETE\nlocks held, snapshot taken" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
commit: "COMMIT" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}
release: "WAL flushed\nlocks released\nchanges visible" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
chain: "AND CHAIN?\nnew tx with same characteristics" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
begin -> work -> commit -> release
commit -> chain: "optional"
```

**Fig. 1.** `COMMIT` is the boundary at which a transaction's effects become permanent and visible. After it returns, no locks remain; before it returns, no other transaction can see the changes (under snapshot isolation) or can depend on the writes surviving a crash.

## Verified on PostgreSQL 17.11

The script below shows the three behaviors an interviewer expects: visibility flips on commit, locks release on commit, and `COMMIT AND CHAIN` opens a new transaction with the same isolation level. `COMMIT` outside a transaction emits a warning but does no harm:

```python
import psycopg
import subprocess

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS commit_demo")
    adm.execute("CREATE TABLE commit_demo (id int PRIMARY KEY)")

t1 = psycopg.connect(DSN, autocommit=False)
t2 = psycopg.connect(DSN, autocommit=True)
c1 = t1.cursor(); c2 = t2.cursor()

c1.execute("BEGIN")
c1.execute("INSERT INTO commit_demo VALUES (1)")
c2.execute("SELECT count(*) FROM commit_demo")
print(f"before T1 COMMIT — T2 count: {c2.fetchone()[0]}")
c1.execute("COMMIT")
c2.execute("SELECT count(*) FROM commit_demo")
print(f"after  T1 COMMIT — T2 count: {c2.fetchone()[0]}")

# COMMIT outside a transaction: WARNING, no error.
res = subprocess.run(
    ["/home/z/my-project/scripts/pg/bin/psql", "-h", "/tmp", "-U", "postgres",
     "-d", "postgres", "-v", "ON_ERROR_STOP=1", "-c", "COMMIT;"],
    capture_output=True, text=True,
    env={"LD_PRELOAD": "/home/z/my-project/scripts/pg/pgpath.so",
         "PGHOST": "/tmp", "PGUSER": "postgres", "PGDATABASE": "postgres"},
)
print(f"COMMIT outside transaction — stderr: {res.stderr.strip()}")
print(f"COMMIT outside transaction — stdout: {res.stdout.strip()}")

# COMMIT AND CHAIN: a new RR transaction is opened automatically.
c1.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
c1.execute("INSERT INTO commit_demo VALUES (2)")
c1.execute("COMMIT AND CHAIN")
c1.execute("SHOW transaction_isolation")
print(f"after COMMIT AND CHAIN — transaction_isolation: {c1.fetchone()[0]}")
c1.execute("INSERT INTO commit_demo VALUES (3)")
c1.execute("COMMIT")
c2.execute("SELECT count(*) FROM commit_demo")
print(f"after 2nd COMMIT — T2 count: {c2.fetchone()[0]}")
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
before T1 COMMIT — T2 count: 0
after  T1 COMMIT — T2 count: 1
COMMIT outside transaction — stderr: WARNING:  there is no transaction in progress
COMMIT outside transaction — stdout: COMMIT
after COMMIT AND CHAIN — transaction_isolation: repeatable read
after 2nd COMMIT — T2 count: 3
```
**Listing 2.** Verified on PostgreSQL 17.11: T2's count goes from 0 to 1 exactly when T1 commits; `COMMIT` outside a transaction emits a WARNING but returns normally; `COMMIT AND CHAIN` opens a new transaction at the same isolation level, so a subsequent `SHOW transaction_isolation` returns `repeatable read` without an explicit `BEGIN ISOLATION LEVEL`.

## `AND CHAIN` and prepared transactions

`COMMIT AND CHAIN` carries the prior transaction's characteristics (isolation, access mode, deferrable) into the next transaction without re-typing them. It does not carry savepoints, temp tables, or cursors — those are transaction-scoped. The standard form `COMMIT AND CHAIN` is also `COMMIT AND NO CHAIN` (the default), which simply ends the transaction. Issuing `COMMIT AND CHAIN` outside a transaction is an error, unlike plain `COMMIT` which only warns.

`COMMIT PREPARED` is a different command for the two-phase commit protocol: a transaction first prepared with `PREPARE TRANSACTION 'gid'` is durably staged and can be committed later (possibly after a reconnect, possibly on a different node of a coordinator) with `COMMIT PREPARED 'gid'`. This is unrelated to `COMMIT AND CHAIN` and is rarely used outside distributed transaction coordinators.

> [!warning] `COMMIT` outside a transaction is a warning, not an error
> The standard and PostgreSQL allow `COMMIT` with no open transaction; the server emits `WARNING: there is no transaction in progress` and returns successfully. Application code that uses ad-hoc `COMMIT` calls (e.g. in a generic "savepoint" wrapper) will silently no-op outside a transaction instead of throwing. `COMMIT AND CHAIN` outside a transaction is the strict version: it raises an error. `ROLLBACK` outside a transaction also warns; `ROLLBACK AND CHAIN` errors.

> [!warning] `synchronous_commit=off` trades durability for latency
> With `synchronous_commit = off` (per-session or per-transaction `SET LOCAL synchronous_commit = off`), `COMMIT` returns before the WAL is flushed — a crash in the next ~10 ms can lose committed transactions. This is legitimate for bulk loads and idempotent writes where replay is cheap, but it is a durability regression. The visibility and lock-release behavior is unchanged; only the crash-survival guarantee is loosened. Quoting the value back to the user — "yes, the data is visible, no, it may not survive a power loss in the next few milliseconds" — is the right interview framing.

> [!tip] Interview answer
> `COMMIT` ends a transaction: WAL is flushed (unless `synchronous_commit=off`), changes become visible to new transactions, all locks are released, and resources like cursors and savepoints are cleaned up. Issued outside a transaction it warns but does not error. `COMMIT AND CHAIN` is a PostgreSQL extension that opens a new transaction with the same isolation level, access mode, and deferrable flag as the one just committed. The related two-phase commit command is `COMMIT PREPARED`, used by distributed coordinators. Related: [[What is a SAVEPOINT in PostgreSQL]] and [[What are SQL transaction isolation levels]].
