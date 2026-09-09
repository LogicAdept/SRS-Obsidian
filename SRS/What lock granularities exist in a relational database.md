<!--
reps: 0
priority: 0
-->
#Databases/SQL/Transactions #Databases/Relational/PostgreSQL #SRS

# What lock granularities exist in a relational database

> [!abstract] Short answer
> Relational databases lock at several granularities: **database**, **table**, **page**, and **row** (some products add **tuple** and **key** variants). Coarser locks are cheaper to acquire and bookkeep but reduce concurrency; finer locks allow more parallel work at higher overhead. PostgreSQL exposes table-level and row-level lock modes through `pg_locks`, plus short-lived page-level locks internal to the buffer pool. The right granularity is whatever the workload tolerates: OLTP tends to row locks; bulk maintenance and schema changes take table locks.

## The classical hierarchy

Textbook order, coarsest to finest:

| Granularity | What it covers | Typical cost | Concurrency impact |
|---|---|---|---|
| Database | The whole DB file / catalog | one entry per session | blocks all writes (and often reads) to the DB |
| Table | All rows of one table | a few entries per table | blocks conflicting modes on that table |
| Page | One 8 KB (PG) heap/index page | a few entries per page | blocks conflicting access to that page only |
| Row (tuple) | One row version | one entry per row | blocks conflicting writes to that one row |
| Key (index entry) | One index tuple | one entry per index entry | narrowest; used by some products for key-range locking |

PostgreSQL implements **table**, **row**, and short-lived **page** locks. It does **not** implement key-range locking the way some other engines do; SERIALIZABLE predicate locking is built from `SIReadLock` entries tracked in `pg_locks`, not from row locks. Page-level share/exclusive locks exist inside the buffer manager and are released immediately after a row is fetched or updated — application code does not manage them.

## Table vs row locks in PostgreSQL, observed live

Table locks are visible in `pg_locks` as `locktype = 'relation'`; row locks show up as `transactionid` locks (the locker's xid is marked, and other writers consult that) and as tuple-level locks visible to `pg_locks` only after promotion. Two sessions on the same table make both layers visible:

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS lock_demo")
    adm.execute("CREATE TABLE lock_demo (id int PRIMARY KEY, txt text)")
    adm.execute("INSERT INTO lock_demo VALUES (1,'a'),(2,'b'),(3,'c')")

t1 = psycopg.connect(DSN, autocommit=False)
t2 = psycopg.connect(DSN, autocommit=False)
c1 = t1.cursor(); c2 = t2.cursor()

# Row-level: FOR UPDATE keeps a row lock until commit.
c1.execute("BEGIN")
c1.execute("SELECT id FROM lock_demo WHERE id = 1 FOR UPDATE")
c1.fetchone()

c2.execute("BEGIN")
c2.execute("""
    SELECT locktype, mode, granted
    FROM pg_locks
    WHERE pid = %s AND locktype IN ('relation','transactionid')
    ORDER BY locktype, mode
""", (t1.info.backend_pid,))
print("T1 row lock (FOR UPDATE) — locks visible from T2:")
for r in c2.fetchall():
    print(f"  {r[0]:15s} {r[1]:30s} granted={r[2]}")

try:
    c2.execute("SET LOCAL lock_timeout = '50ms'")
    c2.execute("UPDATE lock_demo SET txt='x' WHERE id = 1")
    c2.fetchone()
except psycopg.errors.OperationalError as e:
    print(f"T2 UPDATE ... id=1 lock_timeout=50ms: sqlstate={e.sqlstate} — could not obtain lock on tuple (0,1)")
t2.rollback()

c1.execute("COMMIT")

# Table-level: LOCK TABLE ... ACCESS EXCLUSIVE blocks even a plain SELECT.
c1.execute("BEGIN")
c1.execute("LOCK TABLE lock_demo IN ACCESS EXCLUSIVE MODE")
try:
    c2.execute("BEGIN")
    c2.execute("SET LOCAL lock_timeout = '50ms'")
    c2.execute("SELECT count(*) FROM lock_demo")
    c2.fetchone()
except psycopg.errors.OperationalError as e:
    print(f"T2 SELECT while ACCESS EXCLUSIVE held: sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")
t2.rollback()

c2.execute("""
    SELECT locktype, mode, granted
    FROM pg_locks
    WHERE pid = %s AND relation = 'lock_demo'::regclass
""", (t1.info.backend_pid,))
print("T1 ACCESS EXCLUSIVE on lock_demo — locks visible from T2:")
for r in c2.fetchall():
    print(f"  {r[0]:15s} {r[1]:30s} granted={r[2]}")
c1.execute("COMMIT")
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
T1 row lock (FOR UPDATE) — locks visible from T2:
  relation        RowShareLock                   granted=True
  relation        RowShareLock                   granted=True
  transactionid   ExclusiveLock                  granted=True
T2 UPDATE ... id=1 lock_timeout=50ms: sqlstate=55P03 — could not obtain lock on tuple (0,1)
T2 SELECT while ACCESS EXCLUSIVE held: sqlstate=55P03 — canceling statement due to lock timeout
T1 ACCESS EXCLUSIVE on lock_demo — locks visible from T2:
  relation        AccessExclusiveLock            granted=True
```
**Listing 2.** Verified on PostgreSQL 17.11. The `FOR UPDATE` row lock shows up as a `RowShareLock` on the relation plus an `ExclusiveLock` on T1's transaction id; a competing `UPDATE` on the same row is rejected with `55P03` under a 50 ms `lock_timeout`. The `LOCK TABLE ... ACCESS EXCLUSIVE` mode is visible as a single `AccessExclusiveLock` on the relation and blocks even a plain `SELECT`.

## Choosing a granularity

The coarsest lock that the workload tolerates is usually the cheapest. `VACUUM`, `CLUSTER`, `REINDEX`, `TRUNCATE`, and most `ALTER TABLE` forms acquire `ACCESS EXCLUSIVE` because they need to rewrite or replace the whole heap — there is no finer lock that protects them. `CREATE INDEX (without CONCURRENTLY)` takes `SHARE`, blocking writes but allowing reads; `CREATE INDEX CONCURRENTLY` drops to `SHARE UPDATE EXCLUSIVE`, allowing both reads and writes at the cost of two heap scans and a longer build. A row-level `FOR UPDATE` is the right granularity for "this one row is mine, leave the rest alone."

> [!warning] "Page lock" is rarely the answer in PostgreSQL interviews
> The page-vs-row distinction matters in textbook database courses and in some products (older SQL Server configurations, certain ISAM-style engines), but PostgreSQL's page locks are short-lived buffer-manager locks that application code never holds across user statements. If an interviewer asks about page locks in PostgreSQL, the correct answer is "they exist for buffer pool reads and writes, but they are released immediately after a row is fetched or updated — the user-visible granularities are table and row." Pretending otherwise sets up the candidate to claim a page-locking behavior PostgreSQL does not have.

> [!warning] Row locks are not free either
> A `SELECT FOR UPDATE` writes to the tuple's `xmax` and may cause disk I/O — locking 100 000 rows in one transaction bloats the lock table and slows down every other transaction that has to consult it. PostgreSQL never holds row locks in memory longer than the transaction, but the tuple itself carries the lock marker until vacuum reclaims it. The pattern "scan a big table locking rows to simulate a queue" is a known anti-pattern; use `SELECT FOR UPDATE SKIP LOCKED LIMIT n` to bound the working set, or move the queue out of the OLTP table entirely. See [[What is SELECT FOR UPDATE SKIP LOCKED in PostgreSQL]] and [[What is ACCESS EXCLUSIVE in PostgreSQL]].

> [!tip] Interview answer
> Relational databases lock at four granularities — database, table, page, and row — trading off bookkeeping cost against concurrency. PostgreSQL exposes table and row locks to the user; page locks exist only inside the buffer manager and are released as soon as a row is fetched. Table locks (`ACCESS SHARE` up to `ACCESS EXCLUSIVE`) cover schema and bulk operations; row locks (`FOR UPDATE`, `FOR SHARE`, etc.) cover one row version and are visible in `pg_locks` together with the locker's transaction id. Coarser locks are cheaper and block more; finer locks allow more concurrency at higher per-row overhead. Related: [[How does PostgreSQL handle locks and deadlocks]] and [[What is ACCESS EXCLUSIVE in PostgreSQL]].
