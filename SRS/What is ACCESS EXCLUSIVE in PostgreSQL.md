<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/Transactions #SRS

# What is ACCESS EXCLUSIVE in PostgreSQL

> [!abstract] Short answer
> **`ACCESS EXCLUSIVE` is the strongest of PostgreSQL's eight table-level lock modes.** It conflicts with every other lock mode, including the `ACCESS SHARE` that a plain `SELECT` takes — so a transaction holding `ACCESS EXCLUSIVE` on a table is the only transaction that can touch that table in any way. It is acquired automatically by `DROP TABLE`, `TRUNCATE`, `REINDEX`, `CLUSTER`, `VACUUM FULL`, `REFRESH MATERIALIZED VIEW` (without `CONCURRENTLY`), and many forms of `ALTER TABLE`; it is also the default for `LOCK TABLE` without an explicit mode.

## The eight table-level lock modes

PostgreSQL documents eight table-level lock modes; `ACCESS EXCLUSIVE` is the top of the conflict matrix. The list below summarizes the modes from weakest to strongest, what acquires them, and what they conflict with:

| Mode | Acquired by | Conflicts with |
|---|---|---|
| `ACCESS SHARE` | `SELECT` (read) | `ACCESS EXCLUSIVE` only |
| `ROW SHARE` | `SELECT ... FOR UPDATE/SHARE/...` | `EXCLUSIVE`, `ACCESS EXCLUSIVE` |
| `ROW EXCLUSIVE` | `INSERT`, `UPDATE`, `DELETE`, `MERGE` | `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE`, `ACCESS EXCLUSIVE` |
| `SHARE UPDATE EXCLUSIVE` | `VACUUM` (not `FULL`), `ANALYZE`, `CREATE INDEX CONCURRENTLY`, `REINDEX CONCURRENTLY` | self + `SHARE`/`SHARE ROW EXCL`/`EXCL`/`ACCESS EXCL` |
| `SHARE` | `CREATE INDEX` (not `CONCURRENTLY`) | `ROW EXCL` + `SHARE UPDATE EXCL` + `SHARE ROW EXCL` + `EXCL` + `ACCESS EXCL` |
| `SHARE ROW EXCLUSIVE` | `CREATE TRIGGER`, some `ALTER TABLE` | `ROW EXCL` + self + `SHARE` + `EXCL` + `ACCESS EXCL` |
| `EXCLUSIVE` | `REFRESH MATERIALIZED VIEW CONCURRENTLY` | everything except `ACCESS SHARE` |
| `ACCESS EXCLUSIVE` | `DROP TABLE`, `TRUNCATE`, `REINDEX`, `CLUSTER`, `VACUUM FULL`, `REFRESH MV` (no `CONCURRENTLY`), many `ALTER TABLE`, `LOCK TABLE` default | everything |

The single line that defines `ACCESS EXCLUSIVE` is "conflicts with locks of all modes." That is what makes it the outage lock: even a `SELECT` cannot proceed.

```d2
direction: right
as: "ACCESS SHARE\n(plain SELECT)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
rs: "ROW SHARE\n(FOR UPDATE/SHARE)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
re: "ROW EXCLUSIVE\n(INSERT/UPDATE/DELETE)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
sue: "SHARE UPDATE EXCLUSIVE\n(VACUUM, ANALYZE, CREATE INDEX CONCURRENTLY)" {
  width: 340
  height: 70
  style.fill: "#fff3e0"
}
sh: "SHARE\n(CREATE INDEX)" {
  width: 220
  height: 70
  style.fill: "#ffe0b2"
}
sre: "SHARE ROW EXCLUSIVE\n(CREATE TRIGGER)" {
  width: 280
  height: 70
  style.fill: "#ffe0b2"
}
ex: "EXCLUSIVE\n(REFRESH MV CONCURRENTLY)" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ae: "ACCESS EXCLUSIVE\n(DROP, TRUNCATE, VACUUM FULL, ALTER TABLE rewrite, LOCK TABLE default)" {
  width: 480
  height: 90
  style.fill: "#ffebee"
}
as -> rs -> re -> sue -> sh -> sre -> ex -> ae: "stronger"
```

**Fig. 1.** The eight table-level lock modes, weakest to strongest. `ACCESS EXCLUSIVE` sits at the top and conflicts with every other mode — including the `ACCESS SHARE` taken by a plain `SELECT`.

## Verified on PostgreSQL 17.11

A plain `SELECT` acquires only `ACCESS SHARE`. `LOCK TABLE ... ACCESS EXCLUSIVE` blocks even that `SELECT`. `TRUNCATE` acquires `ACCESS EXCLUSIVE` internally:

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS ae_demo")
    adm.execute("CREATE TABLE ae_demo (id int PRIMARY KEY)")
    adm.execute("INSERT INTO ae_demo VALUES (1),(2),(3)")

t1 = psycopg.connect(DSN, autocommit=False)
t2 = psycopg.connect(DSN, autocommit=True)
c1 = t1.cursor(); c2 = t2.cursor()

# 1) Plain SELECT acquires only ACCESS SHARE.
c2.execute("BEGIN")
c2.execute("SELECT count(*) FROM ae_demo")
c2.fetchone()
c1.execute("SELECT mode FROM pg_locks WHERE pid = %s AND relation = 'ae_demo'::regclass",
           (t2.info.backend_pid,))
print(f"plain SELECT lock on ae_demo: {[r[0] for r in c1.fetchall()]}")
t2.rollback()

# 2) T1 takes ACCESS EXCLUSIVE; T2 SELECT blocks.
c1.execute("BEGIN")
c1.execute("LOCK TABLE ae_demo IN ACCESS EXCLUSIVE MODE")
c1.execute("SELECT mode FROM pg_locks WHERE pid = %s AND relation = 'ae_demo'::regclass",
           (t1.info.backend_pid,))
print(f"LOCK TABLE ACCESS EXCLUSIVE — held mode: {[r[0] for r in c1.fetchall()]}")
try:
    c2.execute("BEGIN")
    c2.execute("SET LOCAL lock_timeout = '100ms'")
    c2.execute("SELECT count(*) FROM ae_demo")
    c2.fetchone()
except psycopg.errors.OperationalError as e:
    print(f"SELECT while ACCESS EXCLUSIVE held — sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")
t2.rollback()
t1.rollback()

# 3) TRUNCATE acquires ACCESS EXCLUSIVE.
c1.execute("BEGIN")
c1.execute("TRUNCATE ae_demo")
c1.execute("SELECT mode FROM pg_locks WHERE pid = %s AND relation = 'ae_demo'::regclass",
           (t1.info.backend_pid,))
print(f"TRUNCATE lock on ae_demo: {[r[0] for r in c1.fetchall()]}")
t1.rollback()
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
plain SELECT lock on ae_demo: ['AccessShareLock']
LOCK TABLE ACCESS EXCLUSIVE — held mode: ['AccessExclusiveLock']
SELECT while ACCESS EXCLUSIVE held — sqlstate=55P03 — canceling statement due to lock timeout
TRUNCATE lock on ae_demo: ['ShareLock', 'AccessExclusiveLock']
```
**Listing 2.** Verified on PostgreSQL 17.11: a plain `SELECT` takes only `AccessShareLock`; an explicit `LOCK TABLE ... ACCESS EXCLUSIVE` blocks even that `SELECT` (`55P03` under a 100 ms `lock_timeout`); `TRUNCATE` acquires both a `ShareLock` (transient, for the truncation phase) and the `AccessExclusiveLock` that is the persistent table lock.

## Why `CONCURRENTLY` and `NOT VALID` exist

The whole reason PostgreSQL offers `CREATE INDEX CONCURRENTLY`, `REINDEX CONCURRENTLY`, `DROP INDEX CONCURRENTLY`, `ALTER TABLE ... NOT VALID`, and `VACUUM (FULL)` versus `VACUUM` is to avoid `ACCESS EXCLUSIVE` where possible. `CREATE INDEX CONCURRENTLY` takes `SHARE UPDATE EXCLUSIVE` instead of `SHARE`, which allows both reads and writes during the build — at the cost of two heap scans, longer total time, and the possibility of leaving an `INVALID` index if it fails. `ALTER TABLE ... ADD CONSTRAINT ... NOT VALID` skips the full table scan at constraint-creation time, taking only `SHARE UPDATE EXCLUSIVE`; `VALIDATE CONSTRAINT` then runs the scan with only `SHARE UPDATE EXCLUSIVE` instead of `ACCESS EXCLUSIVE`. These are the production-safe variants of the schema commands that would otherwise lock out everything.

> [!warning] `ALTER TABLE` forms that rewrite the heap take `ACCESS EXCLUSIVE`
> Adding a column with a non-volatile default is fast since PostgreSQL 11 (it only rewrites the catalog). But adding a column with a volatile default, changing a column type, changing collation, or any operation that rewrites every row acquires `ACCESS EXCLUSIVE` and rescans the whole table. On a multi-gigabyte table that means full outage. The escape hatches: add a new column with a `NULL` default, backfill in batches, then switch in a separate transaction; or use `pg_repack`/`pg_squeeze` for online physical rewrites. Always check the "Concurrency Considerations" section of the relevant `ALTER TABLE` form before running it on a live table.

> [!warning] `VACUUM FULL` is not `VACUUM`
> Plain `VACUUM` takes `SHARE UPDATE EXCLUSIVE` and runs concurrently with reads and writes — it does not compact the table, only makes dead tuples reusable. `VACUUM FULL` physically rewrites the heap, returns disk space to the OS, and takes `ACCESS EXCLUSIVE` for the whole rewrite — no reads, no writes, no `SELECT` until it finishes. Confusing them is a common cause of unexplained outages during maintenance. The online alternative is `pg_repack` or `pg_squeeze`; see [[What is the difference between VACUUM and VACUUM FULL]] for the full picture.

> [!tip] Interview answer
> `ACCESS EXCLUSIVE` is PostgreSQL's strongest table-level lock — it conflicts with every other mode, including the `ACCESS SHARE` taken by a plain `SELECT`. It is acquired by `DROP TABLE`, `TRUNCATE`, `REINDEX`, `CLUSTER`, `VACUUM FULL`, `REFRESH MATERIALIZED VIEW` without `CONCURRENTLY`, and many `ALTER TABLE` forms, and it is the default for `LOCK TABLE`. While it is held, no other transaction can touch the table in any way. `CREATE INDEX CONCURRENTLY`, `REINDEX CONCURRENTLY`, `VACUUM` (not `FULL`), and `ALTER TABLE ... NOT VALID` exist specifically to avoid `ACCESS EXCLUSIVE` and keep the table online. Related: [[What lock granularities exist in a relational database]] and [[How does PostgreSQL handle locks and deadlocks]].
