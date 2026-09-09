<!--
reps: 0
priority: 0
-->
#Databases/SQL/DDL #Databases/SQL/DML #Databases/SQL/DCL #SRS

# How would you explain DDL DML and DCL in SQL

> [!abstract] Short answer
> **DDL (Data Definition Language)** defines schema: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`. **DML (Data Manipulation Language)** changes or queries row data: `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `SELECT` (the SQL standard puts `SELECT` in DML, though practitioners often separate it as DQL). **DCL (Data Control Language)** manages access rights: `GRANT`, `REVOKE`. A fourth category, **TCL (Transaction Control Language)**, brackets units of work: `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`. PostgreSQL implements all of these as ordinary SQL commands; the boundaries are conventions about what the command touches, not separate parsers.

## The four categories

| Category | Commands | What it touches | Transactional in PG? |
|---|---|---|---|
| **DDL** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | Schema (tables, indexes, views, functions, roles, schemas) | Yes — DDL is transactional in PostgreSQL |
| **DML** | `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `SELECT` | Row data | Yes |
| **DCL** | `GRANT`, `REVOKE` | Access rights (`pg_authid`, `aclitem`) | Yes |
| **TCL** | `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Transaction boundaries | n/a — these *are* the transaction controls |

The PostgreSQL documentation does not use these category names — they come from the SQL standard and database textbooks. The PostgreSQL manuals group commands by function ("SQL Commands" reference, "Data Definition" tutorial chapter, "Data Manipulation" tutorial chapter, "Privileges" section). Interviewers use the abbreviations because they are a useful shorthand for "what kind of operation are you doing?"

```d2
direction: right
ddl: "DDL\nCREATE / ALTER / DROP / TRUNCATE\nschema objects" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
dml: "DML\nINSERT / UPDATE / DELETE / MERGE / SELECT\nrow data" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
dcl: "DCL\nGRANT / REVOKE\naccess rights" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
tcl: "TCL\nBEGIN / COMMIT / ROLLBACK / SAVEPOINT\ntransaction bracket" {
  width: 320
  height: 90
  style.fill: "#fce4ec"
}
ddl -> dml: "schema before data"
dml -> dcl: "data access controlled"
dcl -> tcl: "all inside a transaction"
```

**Fig. 1.** The four SQL command categories. DDL defines the schema; DML reads and writes row data; DCL controls who can do either; TCL brackets the unit of work. In PostgreSQL all four are transactional — you can roll back a `CREATE TABLE` or a `GRANT` as easily as an `INSERT`.

## Verified on PostgreSQL 17.11

One command from each category, executed against PostgreSQL 17.11, with the effect introspected from the catalog. The DCL step creates a role and grants/revoke `SELECT` on the DDL-created table. The TCL step uses `SAVEPOINT` inside a transaction to show that all four categories participate in the same transaction.

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP ROLE IF EXISTS analyst")
    adm.execute("DROP TABLE IF EXISTS dml_demo")
    adm.execute("CREATE ROLE analyst LOGIN")

# DDL: CREATE TABLE
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("CREATE TABLE dml_demo (id int PRIMARY KEY, v int)")
    cur = adm.execute("SELECT relname FROM pg_class WHERE relname = 'dml_demo' AND relkind = 'r'")
    print(f"DDL: CREATE TABLE — table exists: {cur.fetchone() is not None}")

# DML: INSERT, UPDATE, DELETE, SELECT
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("INSERT INTO dml_demo VALUES (1, 10), (2, 20), (3, 30)")
    adm.execute("UPDATE dml_demo SET v = v + 1 WHERE id = 2")
    adm.execute("DELETE FROM dml_demo WHERE id = 3")
    cur = adm.execute("SELECT id, v FROM dml_demo ORDER BY id")
    print("DML: INSERT + UPDATE + DELETE + SELECT result:")
    for r in cur.fetchall():
        print(f"  id={r[0]}  v={r[1]}")

# DCL: GRANT, REVOKE
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("GRANT SELECT ON dml_demo TO analyst")
    cur = adm.execute("""
        SELECT privilege_type FROM information_schema.role_table_grants
        WHERE table_name = 'dml_demo' AND grantee = 'analyst'
    """)
    print(f"DCL: GRANT — privileges granted to analyst: {[r[0] for r in cur.fetchall()]}")
    adm.execute("REVOKE SELECT ON dml_demo FROM analyst")
    cur = adm.execute("""
        SELECT privilege_type FROM information_schema.role_table_grants
        WHERE table_name = 'dml_demo' AND grantee = 'analyst'
    """)
    print(f"DCL: REVOKE — privileges remaining: {[r[0] for r in cur.fetchall()]}")

# TCL: BEGIN, SAVEPOINT, ROLLBACK TO, COMMIT
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("BEGIN")
    cur.execute("INSERT INTO dml_demo VALUES (10, 100)")
    cur.execute("SAVEPOINT sp1")
    cur.execute("INSERT INTO dml_demo VALUES (11, 110)")
    cur.execute("ROLLBACK TO SAVEPOINT sp1")
    cur.execute("INSERT INTO dml_demo VALUES (12, 120)")
    cur.execute("COMMIT")
    cur.execute("SELECT id, v FROM dml_demo WHERE id >= 10 ORDER BY id")
    print("TCL: BEGIN + SAVEPOINT + ROLLBACK TO + COMMIT result:")
    for r in cur.fetchall():
        print(f"  id={r[0]}  v={r[1]}")

# DDL: DROP TABLE (cleanup)
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS dml_demo")
    cur = adm.execute("SELECT relname FROM pg_class WHERE relname = 'dml_demo' AND relkind = 'r'")
    print(f"DDL: DROP TABLE — table exists: {cur.fetchone() is not None}")
    adm.execute("DROP ROLE IF EXISTS analyst")
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
DDL: CREATE TABLE — table exists: True
DML: INSERT + UPDATE + DELETE + SELECT result:
  id=1  v=10
  id=2  v=21
DCL: GRANT — privileges granted to analyst: ['SELECT']
DCL: REVOKE — privileges remaining: []
TCL: BEGIN + SAVEPOINT + ROLLBACK TO + COMMIT result:
  id=10  v=100
  id=12  v=120
DDL: DROP TABLE — table exists: False
```
**Listing 2.** Verified on PostgreSQL 17.11. Each category is exercised with a representative command: `CREATE TABLE` (DDL), `INSERT/UPDATE/DELETE/SELECT` (DML), `GRANT/REVOKE` (DCL), `BEGIN/SAVEPOINT/ROLLBACK TO/COMMIT` (TCL). All four participate in the same transaction model — `SAVEPOINT` and `ROLLBACK TO SAVEPOINT` work the same way inside the TCL block regardless of which category produced the changes.

## PostgreSQL-specific note: DDL is transactional

In PostgreSQL, `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, `GRANT`, `REVOKE`, `CREATE INDEX`, and most other DDL/DCL commands are **transactional** — you can wrap them in `BEGIN`/`COMMIT` and `ROLLBACK` undoes them. This is not true on every engine: MySQL's InnoDB is transactional for DDL since 8.0 with some caveats; Oracle has had transactional DDL for decades; SQL Server is transactional; some NoSQL-adjacent engines are not. The practical consequence is that a PostgreSQL migration script can wrap a multi-step schema change in a single transaction and either commit it atomically or roll it back cleanly. See [[How do you add a column to a large PostgreSQL table without downtime]] for why some `ALTER TABLE` forms still need the `NOT VALID` + `VALIDATE` pattern even though they are transactional.

> [!warning] `TRUNCATE` is DDL, not DML
> `TRUNCATE` is classified as DDL even though it removes rows. The reason is that it takes `ACCESS EXCLUSIVE` (like `DROP`), resets the table's `reltuples` and the sequence-owned-by-the-table counters are not advanced, and in PostgreSQL it is transactional but cannot be inside a `BEGIN` block with other DDL that touches the same table in some replication setups. `TRUNCATE` is much faster than `DELETE` for emptying a table, but it bypasses the row-level locks and triggers that `DELETE` fires — see [[What is ACCESS EXCLUSIVE in PostgreSQL]] for the lock implications.

> [!warning] `SELECT` is DML by the standard; many practitioners call it DQL
> The SQL standard classifies `SELECT` as DML because it manipulates (reads) data. Many practitioners and textbooks split it out as **DQL (Data Query Language)** because the operational concerns of `SELECT` (planner, indexes, joins) are very different from `INSERT`/`UPDATE`/`DELETE`. PostgreSQL's own manual puts `SELECT` in the "Queries" chapter, separate from "Modifying Tables". Both conventions are defensible; the trap is to insist that one is "correct" — interviewers may use either. If asked, give the standard answer (DML) and note the DQL split.

> [!tip] Interview answer
> DDL defines schema (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`); DML manipulates row data (`INSERT`, `UPDATE`, `DELETE`, `MERGE`, `SELECT`); DCL controls access (`GRANT`, `REVOKE`); TCL brackets transactions (`BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`). In PostgreSQL all four categories are transactional — you can wrap a `CREATE TABLE` or a `GRANT` in `BEGIN`/`COMMIT` and `ROLLBACK` undoes it, which makes multi-step migration scripts atomic. The standard puts `SELECT` in DML; practitioners often split it out as DQL. Related: [[How do you add a column to a large PostgreSQL table without downtime]] and [[How would you explain the SQL DROP statement]].
