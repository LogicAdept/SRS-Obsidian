<!--
reps: 0
priority: 0
-->
#Databases/SQL/Transactions #Databases/Relational/PostgreSQL #SRS

# What are SQL transaction isolation levels

> [!abstract] Short answer
> **The SQL standard defines four transaction isolation levels** — `READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE` — ordered from weakest to strongest by which concurrency anomalies they forbid. PostgreSQL implements all four syntactically, but **`READ UNCOMMITTED` behaves like `READ COMMITTED`** (no dirty reads are possible under MVCC) and **`REPEATABLE READ` is stronger than the standard requires** (it also prevents phantom reads). `READ COMMITTED` is the default in PostgreSQL; `SERIALIZABLE` is the default in the standard.

## The four levels and what each prevents

The SQL standard names four phenomena that can result from concurrent execution: dirty read, non-repeatable read, phantom read, serialization anomaly. Each level forbids a subset:

| Level | Dirty read | Non-repeatable read | Phantom read | Serialization anomaly |
|---|---|---|---|---|
| `READ UNCOMMITTED` | allowed | allowed | allowed | allowed |
| `READ COMMITTED` | prevented | allowed | allowed | allowed |
| `REPEATABLE READ` | prevented | prevented | allowed | allowed |
| `SERIALIZABLE` | prevented | prevented | prevented | prevented |

PostgreSQL's table (from the official docs, `transaction-iso.html` §13.2) differs in two cells:

| Level | Dirty read | Non-repeatable read | Phantom read | Serialization anomaly |
|---|---|---|---|---|
| `READ UNCOMMITTED` | **not possible in PG** | possible | possible | possible |
| `READ COMMITTED` | not possible | possible | possible | possible |
| `REPEATABLE READ` | not possible | not possible | **not possible in PG** | possible |
| `SERIALIZABLE` | not possible | not possible | not possible | not possible |

The two PG-specific differences: `READ UNCOMMITTED` is mapped to `READ COMMITTED` (MVCC never returns uncommitted versions, so dirty reads cannot happen at any level), and `REPEATABLE READ` prevents phantoms because it uses one snapshot per transaction (Snapshot Isolation). What PG's `REPEATABLE READ` still allows is the serialization anomaly (e.g. write skew).

```d2
direction: right
ru: "READ UNCOMMITTED\n(PG: behaves like RC)" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
rc: "READ COMMITTED\n(PG default)" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
rr: "REPEATABLE READ\nSnapshot Isolation\nprevents phantoms too" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
ser: "SERIALIZABLE\nSSI + predicate locks" {
  width: 240
  height: 70
  style.fill: "#c8e6c9"
}
ru -> rc -> rr -> ser: "stronger"
```

**Fig. 1.** The four SQL isolation levels, weakest to strongest. PostgreSQL accepts all four in `SET TRANSACTION ISOLATION LEVEL`, but `READ UNCOMMITTED` is implemented as `READ COMMITTED` and `REPEATABLE READ` is implemented as Snapshot Isolation (stronger than the SQL standard requires).

## Verified on PostgreSQL 17.11

The script shows: the default isolation is `read committed`; all four levels can be requested; `READ UNCOMMITTED` is accepted but PostgreSQL does not perform dirty reads — a second transaction at `READ UNCOMMITTED` cannot see an uncommitted value:

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as r:
    cur = r.execute("SHOW transaction_isolation")
    print(f"default transaction_isolation: {cur.fetchone()[0]}")

levels = [
    ("READ UNCOMMITTED", "read uncommitted"),
    ("READ COMMITTED",   "read committed"),
    ("REPEATABLE READ",  "repeatable read"),
    ("SERIALIZABLE",     "serializable"),
]
for set_level, expected_show in levels:
    with psycopg.connect(DSN) as conn:
        conn.execute(f"BEGIN ISOLATION LEVEL {set_level}")
        cur = conn.execute("SHOW transaction_isolation")
        shown = cur.fetchone()[0]
        note = "READ UNCOMMITTED behaves as READ COMMITTED" if set_level == "READ UNCOMMITTED" else "OK"
        print(f"BEGIN ISOLATION LEVEL {set_level:18s} -> SHOW = {shown}  ({note})")
        conn.execute("COMMIT")

# READ UNCOMMITTED does NOT do dirty reads in PostgreSQL.
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS iso_demo")
    adm.execute("CREATE TABLE iso_demo (id int PRIMARY KEY, v int)")
    adm.execute("INSERT INTO iso_demo VALUES (1, 0)")

t1 = psycopg.connect(DSN, autocommit=False)
t2 = psycopg.connect(DSN, autocommit=False)
c1 = t1.cursor(); c2 = t2.cursor()

c1.execute("BEGIN")
c1.execute("UPDATE iso_demo SET v = 99 WHERE id = 1")
c2.execute("BEGIN ISOLATION LEVEL READ UNCOMMITTED")
c2.execute("SELECT v FROM iso_demo WHERE id = 1")
print(f"T2 (READ UNCOMMITTED) sees v = {c2.fetchone()[0]}  (PG: no dirty read)")

c1.execute("ROLLBACK")
c2.execute("COMMIT")
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
default transaction_isolation: read committed
BEGIN ISOLATION LEVEL READ UNCOMMITTED   -> SHOW = read uncommitted  (READ UNCOMMITTED behaves as READ COMMITTED)
BEGIN ISOLATION LEVEL READ COMMITTED     -> SHOW = read committed  (OK)
BEGIN ISOLATION LEVEL REPEATABLE READ    -> SHOW = repeatable read  (OK)
BEGIN ISOLATION LEVEL SERIALIZABLE       -> SHOW = serializable  (OK)
T2 (READ UNCOMMITTED) sees v = 0  (PG: no dirty read)
```
**Listing 2.** Verified on PostgreSQL 17.11: the default isolation is `read committed`. All four standard levels are accepted by `BEGIN ISOLATION LEVEL`. The `SHOW` for `READ UNCOMMITTED` reports the requested name, but the behavior is `READ COMMITTED` — T2 at `READ UNCOMMITTED` cannot see T1's uncommitted `v=99`; it reads the last committed value `v=0`.

## Setting the level

The level is set per transaction, either at the start or via session defaults:

```sql
-- Per transaction, at the start.
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- ... work ...
COMMIT;

-- Per session (default for all subsequent transactions).
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Per database (cluster-wide via config file).
ALTER DATABASE mydb SET default_transaction_isolation = 'serializable';
```

**Listing 3.** Three scopes for setting the isolation level: per-transaction (at `BEGIN`), per-session (via `SET SESSION CHARACTERISTICS`), and per-database (via `ALTER DATABASE` or the config file).

A `SET TRANSACTION` issued after the first non-transaction-control statement of the transaction is too late — the snapshot has already been taken. `SET SESSION CHARACTERISTICS` is the right tool for a connection pool that hands out connections to multiple callers; per-transaction `BEGIN ISOLATION LEVEL` is the right tool when the level is chosen per unit of work.

## Picking a level in practice

The defaults that work for most PostgreSQL applications:

- **`READ COMMITTED`** (the default) — short transactions, OLTP, dashboards. Each statement sees a fresh snapshot; no phantoms within a single statement. Suitable for >90% of workloads.
- **`REPEATABLE READ`** — long-running reports that need a stable view, batch exports, idempotent retry of multi-statement units. The frozen snapshot means a re-read returns the same value.
- **`SERIALIZABLE`** — correctness-critical multi-row invariants (financial ledgers, inventory reservations, "at least one doctor on call"). Adds SSI overhead and a mandatory retry loop on `40001`.

`READ UNCOMMITTED` should not appear in production PostgreSQL code: it is accepted for SQL-standard compatibility but behaves identically to `READ COMMITTED`. Pretending otherwise (using it as a "fast and dirty" read mode) is a misuse — the speedup does not exist.

> [!warning] `REPEATABLE READ` in PostgreSQL is Snapshot Isolation, not standard RR
> The SQL standard permits phantom reads at `REPEATABLE READ`. PostgreSQL's RR prevents them by taking one snapshot per transaction (the technique academic literature calls Snapshot Isolation). The tradeoff is that PostgreSQL's RR allows the **serialization anomaly** — write skew — that the standard says only `SERIALIZABLE` should prevent. The retry pattern for SSI aborts (`40001`) applies to RR's first-updater-wins aborts too. See [[How does Repeatable Read prevent phantom reads in PostgreSQL]] and [[How do you handle transaction isolation anomalies]].

> [!warning] The default differs across databases
> PostgreSQL and MySQL default to `READ COMMITTED` (MySQL is `REPEATABLE READ` by default since 8.0, actually). Oracle defaults to `READ COMMITTED`. SQL Server defaults to `READ COMMITTED` (with `READ_COMMITTED_SNAPSHOT` controlling whether it is snapshot-based). Code that assumes "the default is `SERIALIZABLE`" because that is what the SQL standard says is wrong on every major engine. Always set the level explicitly when correctness depends on it.

> [!tip] Interview answer
> The SQL standard defines four isolation levels — `READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE` — ordered by which anomalies they forbid (dirty, non-repeatable, phantom read, serialization anomaly). PostgreSQL accepts all four but maps `READ UNCOMMITTED` to `READ COMMITTED` (dirty reads are impossible under MVCC) and implements `REPEATABLE READ` as Snapshot Isolation, which also prevents phantoms — stronger than the standard requires. The default is `READ COMMITTED`; use `REPEATABLE READ` for stable-snapshot reports and `SERIALIZABLE` (SSI) for correctness-critical invariants with a retry loop on `40001`. Related: [[How does Repeatable Read prevent phantom reads in PostgreSQL]] and [[What is PostgreSQL Serializable Snapshot Isolation]].
