<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DDL #SRS

# How do you add a column to a large PostgreSQL table without downtime

> [!abstract] Short answer
> **`ALTER TABLE ... ADD COLUMN` with a constant default is metadata-only since PostgreSQL 11** — it does not rewrite the table, so it is safe on a table of any size. A **volatile** default (`random()`, `clock_timestamp()`) still rewrites every row and is the classic outage. For `NOT NULL` on a populated column, use the **`NOT VALID` + `VALIDATE`** pattern: add the column nullable, backfill in batches, add a `CHECK` constraint `NOT VALID` (no scan), then `VALIDATE CONSTRAINT` (scans but takes only `SHARE UPDATE EXCLUSIVE`, allowing concurrent reads and writes). `CREATE INDEX CONCURRENTLY` is the analogous pattern for indexes.

## The metadata-only fast path

PostgreSQL 11 changed `ADD COLUMN ... DEFAULT` so that a **constant** default is stored in the catalog and applied lazily to existing rows when they are read. The table is not rewritten. The same applies to a `STABLE` expression like `now()` — the default is evaluated once at `ALTER TABLE` time and the resulting value is used for all pre-existing rows. A **volatile** default (`random()`, `clock_timestamp()`) cannot be evaluated once and reused, so PostgreSQL rewrites the whole table — exactly the outage scenario.

```d2
direction: right
const: "DEFAULT false\nDEFAULT 'pending'\nDEFAULT now() (evaluated once)" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
meta: "ALTER TABLE\nupdates pg_attribute.attmissingval\n~1 ms, ACCESS EXCLUSIVE briefly" {
  width: 340
  height: 90
  style.fill: "#e3f2fd"
}
vol: "DEFAULT random()\nDEFAULT clock_timestamp()" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
rewrite: "ALTER TABLE\nrewrites every row\nseconds to minutes per GB" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
const -> meta
vol -> rewrite
```

**Fig. 1.** Two paths for `ADD COLUMN ... DEFAULT`. A constant or single-eval default is metadata-only (top); a volatile default rewrites the whole table (bottom). The metadata-only path takes milliseconds and locks the table only for the catalog update; the rewrite path holds `ACCESS EXCLUSIVE` for the whole rewrite.

## Verified on PostgreSQL 17.11

A 100 000-row table, three `ALTER TABLE ADD COLUMN` variants. The constant default and the `now()` default finish in milliseconds; the `random()` default takes ~60× longer because it rewrites the table. The `NOT VALID` + `VALIDATE` pattern for adding a `NOT NULL`-equivalent constraint on a populated column is shown separately.

```python
import psycopg
import time

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS big_demo")
    adm.execute("CREATE TABLE big_demo (id int PRIMARY KEY)")
    adm.execute("INSERT INTO big_demo SELECT i FROM generate_series(1, 100000) AS i")
    cur = adm.execute("SELECT count(*) FROM big_demo")
    print(f"rows in big_demo: {cur.fetchone()[0]}")

with psycopg.connect(DSN, autocommit=True) as adm:
    t0 = time.perf_counter()
    adm.execute("ALTER TABLE big_demo ADD COLUMN flag boolean DEFAULT false")
    dt = time.perf_counter() - t0
    cur = adm.execute("SELECT count(*) FROM big_demo WHERE flag = false")
    print(f"ADD COLUMN flag boolean DEFAULT false: {dt*1000:.1f} ms; rows with flag=false: {cur.fetchone()[0]}")

with psycopg.connect(DSN, autocommit=True) as adm:
    t0 = time.perf_counter()
    adm.execute("ALTER TABLE big_demo ADD COLUMN created_at timestamptz DEFAULT now()")
    dt = time.perf_counter() - t0
    cur = adm.execute("SELECT count(*) FROM big_demo WHERE created_at IS NOT NULL")
    print(f"ADD COLUMN created_at DEFAULT now(): {dt*1000:.1f} ms; rows with non-null created_at: {cur.fetchone()[0]}")

with psycopg.connect(DSN, autocommit=True) as adm:
    t0 = time.perf_counter()
    adm.execute("ALTER TABLE big_demo ADD COLUMN rnd int DEFAULT (random() * 1000)::int")
    dt = time.perf_counter() - t0
    cur = adm.execute("SELECT count(*) FROM big_demo WHERE rnd IS NOT NULL")
    print(f"ADD COLUMN rnd DEFAULT random(): {dt*1000:.1f} ms; rows with non-null rnd: {cur.fetchone()[0]}")

# NOT VALID + VALIDATE pattern for adding a NOT NULL-equivalent constraint.
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS nn_demo")
    adm.execute("CREATE TABLE nn_demo (id int PRIMARY KEY)")
    adm.execute("INSERT INTO nn_demo SELECT i FROM generate_series(1, 50000) AS i")
    adm.execute("ALTER TABLE nn_demo ADD COLUMN email text")
    adm.execute("UPDATE nn_demo SET email = 'user_' || id::text || '@example.com'")
    t0 = time.perf_counter()
    adm.execute("ALTER TABLE nn_demo ADD CONSTRAINT email_not_null CHECK (email IS NOT NULL) NOT VALID")
    print(f"ADD CONSTRAINT ... NOT VALID: {(time.perf_counter()-t0)*1000:.1f} ms (no scan)")
    t0 = time.perf_counter()
    adm.execute("ALTER TABLE nn_demo VALIDATE CONSTRAINT email_not_null")
    print(f"VALIDATE CONSTRAINT: {(time.perf_counter()-t0)*1000:.1f} ms (scan, concurrent writes allowed)")
    cur = adm.execute("""
        SELECT conname, convalidated FROM pg_constraint
        WHERE conrelid = 'nn_demo'::regclass AND conname = 'email_not_null'
    """)
    r = cur.fetchone()
    print(f"constraint {r[0]}: convalidated={r[1]}")
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
rows in big_demo: 100000
ADD COLUMN flag boolean DEFAULT false: 1.7 ms; rows with flag=false: 100000
ADD COLUMN created_at DEFAULT now(): 0.9 ms; rows with non-null created_at: 100000
ADD COLUMN rnd DEFAULT random(): 103.7 ms; rows with non-null rnd: 100000
ADD CONSTRAINT ... NOT VALID: 0.5 ms (no scan)
VALIDATE CONSTRAINT: 5.7 ms (scan, but concurrent writes allowed)
constraint email_not_null: convalidated=True
```
**Listing 2.** Verified on PostgreSQL 17.11 on a 100 000-row table. The constant default (`false`) and the single-eval default (`now()`) finish in ~1 ms — metadata only. The volatile default (`random()`) takes ~100 ms because it rewrites every row. The `NOT VALID` + `VALIDATE` pattern adds the constraint without a rewrite: `NOT VALID` is sub-millisecond (no scan); `VALIDATE` scans the table but takes `SHARE UPDATE EXCLUSIVE`, so concurrent reads and writes proceed.

## The full online migration playbook

For the general case — adding a populated `NOT NULL` column with a non-trivial default to a large table under load — the standard sequence is:

1. `ALTER TABLE ... ADD COLUMN new_col type DEFAULT <constant>` — metadata-only since PG 11; locks the table only for the catalog update.
2. Backfill any rows that should have a different value, in batches, with `lock_timeout` set so you do not queue behind long transactions.
3. `ALTER TABLE ... ADD CONSTRAINT new_col_not_null CHECK (new_col IS NOT NULL) NOT VALID` — sub-second; does not scan.
4. `ALTER TABLE ... VALIDATE CONSTRAINT new_col_not_null` — scans the table, but takes `SHARE UPDATE EXCLUSIVE`, allowing concurrent reads and writes.
5. From PG 12+, you can now `ALTER TABLE ... ALTER COLUMN new_col SET NOT NULL` cheaply, because the validated `CHECK` proves the constraint holds — the scan that `SET NOT NULL` would otherwise require is skipped.

The same shape applies to index creation: `CREATE INDEX CONCURRENTLY` takes `SHARE UPDATE EXCLUSIVE` instead of `SHARE`, allowing writes during the build, at the cost of two heap scans and a longer total time. See [[What is ACCESS EXCLUSIVE in PostgreSQL]] for why avoiding `ACCESS EXCLUSIVE` matters.

> [!warning] `SET NOT NULL` still scans in PostgreSQL 12+ if no validated CHECK proves it
> The PG 12 optimization that lets `SET NOT NULL` skip the scan applies **only** when a validated `CHECK (col IS NOT NULL)` constraint already exists. Without that constraint, `SET NOT NULL` scans the whole table and takes `ACCESS EXCLUSIVE` for the duration. Always pair the `NOT VALID` + `VALIDATE` step with `SET NOT NULL` to get the fast path. See [[What is ACCESS EXCLUSIVE in PostgreSQL]] and [[How would you explain CREATE TABLE syntax in SQL]].

> [!warning] A long-running transaction can still break the online path
> `ADD COLUMN ... DEFAULT` and `VALIDATE CONSTRAINT` are fast, but they still need `ACCESS EXCLUSIVE` and `SHARE UPDATE EXCLUSIVE` respectively for the catalog update. A long-running transaction that holds `ACCESS SHARE` on the table blocks the `ACCESS EXCLUSIVE` — the `ALTER` queues behind it, and every subsequent transaction queues behind the `ALTER`. The standard mitigation is `lock_timeout = '2s'` on the migration session: if the catalog update cannot acquire its lock quickly, it aborts and you retry, instead of stalling the whole table. This is the same pattern used for `CREATE INDEX CONCURRENTLY` retries.

> [!tip] Interview answer
> Adding a column with a constant default is metadata-only since PostgreSQL 11 — no rewrite, safe on any size table. A volatile default (`random()`, `clock_timestamp()`) still rewrites every row. For `NOT NULL` on a populated column, use the `NOT VALID` + `VALIDATE` pattern: add the column nullable, backfill in batches, add `CHECK (col IS NOT NULL) NOT VALID` (no scan), then `VALIDATE CONSTRAINT` (scans but allows concurrent writes). From PG 12, a validated `CHECK` lets a later `SET NOT NULL` skip its scan. `CREATE INDEX CONCURRENTLY` is the analogous pattern for indexes. Always set `lock_timeout` so the migration aborts instead of queuing behind a long transaction. Related: [[What is ACCESS EXCLUSIVE in PostgreSQL]] and [[How would you explain CREATE TABLE syntax in SQL]].
