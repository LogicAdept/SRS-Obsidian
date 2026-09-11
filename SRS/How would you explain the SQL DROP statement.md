<!--
reps: 0
priority: 0
-->
#Databases/SQL/DDL #SRS

# How would you explain the SQL DROP statement

> [!abstract] Short answer
> **`DROP` removes a database object permanently.** PostgreSQL supports `DROP TABLE`, `DROP INDEX`, `DROP VIEW`, `DROP FUNCTION`, `DROP PROCEDURE`, `DROP SCHEMA`, `DROP DATABASE`, `DROP ROLE`, `DROP TYPE`, `DROP EXTENSION`, and many more — each with the same shape: `DROP <type> [IF EXISTS] name [, ...] [CASCADE | RESTRICT]`. The default is `RESTRICT`: if any other object depends on the target, the `DROP` fails with sqlstate `2BP01`. `CASCADE` drops the dependent objects too. `IF EXISTS` turns the "object does not exist" error into a notice.

## Syntax and the dependency model

```sql
DROP TABLE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

**Listing 1.** The `DROP TABLE` shape. The same `IF EXISTS` and `CASCADE | RESTRICT` modifiers apply to `DROP INDEX`, `DROP VIEW`, `DROP FUNCTION`, `DROP SCHEMA`, `DROP DATABASE`, and other `DROP` variants.

PostgreSQL tracks dependencies between objects in `pg_depend`. A view depends on its underlying tables. A foreign key constraint depends on both the referencing and referenced tables. An index depends on its table. A function depends on the types of its arguments. When you issue `DROP TABLE base RESTRICT` (the default), PostgreSQL checks `pg_depend` for anything that depends on `base`; if it finds anything, the drop fails. `DROP TABLE base CASCADE` recursively drops every object that depends on `base`, then `base` itself.

```d2
direction: right
base: "base table" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
view: "base_view\nSELECT * FROM base" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
child: "dependent table\nFK -> base" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
restrict: "DROP TABLE base\nRESTRICT (default)\n-> 2BP01 error" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
cascade: "DROP TABLE base CASCADE\n-> drops base_view\n-> drops dependent's FK\n-> drops base" {
  width: 360
  height: 90
  style.fill: "#e8f5e9"
}
base -> view: "depends on"
base -> child: "FK references"
base -> restrict
base -> cascade
```

**Fig. 1.** `base` has two dependents: a view (`base_view`) and a child table with a foreign key to `base`. `DROP TABLE base RESTRICT` fails with sqlstate `2BP01`; `DROP TABLE base CASCADE` drops the view, removes the foreign key constraint from `dependent` (but keeps the `dependent` table itself), then drops `base`.

## Verified on PostgreSQL 17.11

The empiric builds a small schema with a base table, a view, a dependent table with a foreign key, and a function, then exercises `RESTRICT`, `CASCADE`, `IF EXISTS`, and `DROP SCHEMA CASCADE`:

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP SCHEMA IF EXISTS drop_demo CASCADE")
    adm.execute("CREATE SCHEMA drop_demo")
    adm.execute("SET search_path TO drop_demo")
    adm.execute("CREATE TABLE base (id int PRIMARY KEY, v int)")
    adm.execute("CREATE TABLE dependent (id int REFERENCES base(id))")
    adm.execute("CREATE VIEW base_view AS SELECT * FROM base")
    adm.execute("CREATE INDEX base_v_idx ON base(v)")
    adm.execute("CREATE FUNCTION base_count() RETURNS int AS $$ SELECT count(*) FROM base $$ LANGUAGE sql")

# 1) DROP TABLE with RESTRICT (default) fails when a view depends on it.
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("SET search_path TO drop_demo")
    try:
        adm.execute("DROP TABLE base")
        print("ERROR: DROP TABLE base RESTRICT did not raise")
    except psycopg.errors.DependentObjectsStillExist as e:
        print(f"DROP TABLE base (RESTRICT default): sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")

# 2) DROP TABLE base CASCADE removes the view too.
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("SET search_path TO drop_demo")
    adm.execute("DROP TABLE base CASCADE")
    cur = adm.execute("""
        SELECT relname, relkind FROM pg_class
        WHERE relname IN ('base','base_view','dependent')
        ORDER BY relname
    """)
    rows = cur.fetchall()
    print("after DROP TABLE base CASCADE — remaining objects:")
    for r in rows:
        print(f"  {r[0]} (relkind={r[1]})")

# 3) DROP IF EXISTS on an absent object is a notice, not an error.
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("SET search_path TO drop_demo")
    try:
        adm.execute("DROP TABLE no_such_table")
        print("ERROR: DROP TABLE no_such_table did not raise")
    except psycopg.errors.UndefinedTable as e:
        print(f"DROP TABLE no_such_table (no IF EXISTS): sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")
    adm.execute("DROP TABLE IF EXISTS no_such_table")
    print("DROP TABLE IF EXISTS no_such_table — succeeded silently")

# 4) DROP FUNCTION base_count() — also dependent on schema.
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("SET search_path TO drop_demo")
    adm.execute("DROP FUNCTION IF EXISTS base_count()")
    cur = adm.execute("""
        SELECT proname FROM pg_proc
        WHERE proname = 'base_count' AND pronamespace = 'drop_demo'::regnamespace
    """)
    print(f"after DROP FUNCTION IF EXISTS base_count: function exists = {cur.fetchone() is not None}")

# 5) DROP SCHEMA CASCADE removes everything inside.
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP SCHEMA drop_demo CASCADE")
    cur = adm.execute("SELECT nspname FROM pg_namespace WHERE nspname = 'drop_demo'")
    print(f"after DROP SCHEMA drop_demo CASCADE: schema exists = {cur.fetchone() is not None}")
```

**Listing 2.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
DROP TABLE base (RESTRICT default): sqlstate=2BP01 — cannot drop table base because other objects depend on it
after DROP TABLE base CASCADE — remaining objects:
  dependent (relkind=r)
DROP TABLE no_such_table (no IF EXISTS): sqlstate=42P01 — table "no_such_table" does not exist
DROP TABLE IF EXISTS no_such_table — succeeded silently
after DROP FUNCTION IF EXISTS base_count: function exists = False
after DROP SCHEMA drop_demo CASCADE: schema exists = False
```
**Listing 3.** Verified on PostgreSQL 17.11. `RESTRICT` (default) fails with `2BP01` because `base_view` depends on `base`. `CASCADE` drops `base`, `base_view`, and the `base_v_idx` index; the `dependent` table survives but its foreign key constraint to `base` is dropped automatically. `DROP TABLE no_such_table` raises `42P01`; `DROP TABLE IF EXISTS no_such_table` is a notice and succeeds. `DROP SCHEMA ... CASCADE` removes the schema and everything inside it.

## Operational notes

`DROP` is transactional in PostgreSQL — you can wrap it in `BEGIN`/`COMMIT` and `ROLLBACK` undoes it. This makes a multi-object migration atomic. `DROP TABLE` takes `ACCESS EXCLUSIVE` for the duration; on a large table with concurrent reads, the `DROP` queues behind them and subsequent statements queue behind the `DROP`. `DROP DATABASE` is special: it cannot run inside a transaction, and it requires that no one is connected to the database (PostgreSQL will terminate existing connections if you set `WITH (FORCE)` on PG 13+). `DROP ROLE` fails if the role still owns objects or has privileges — use `REASSIGN OWNED` and `DROP OWNED` first.

The destructive nature of `DROP` is what makes `RESTRICT` the right default: it forces the user to acknowledge the dependents explicitly, either by dropping them first or by adding `CASCADE`. A migration script that uses `CASCADE` casually can drop a view that another team depends on without notice. The standard discipline is to use `RESTRICT` (the default) in migrations and to handle dependents explicitly; reserve `CASCADE` for cases where you have audited the dependency tree.

> [!warning] `DROP TABLE ... CASCADE` does not cascade to foreign keys **from** other tables — only to objects that depend on the dropped table
> The dependency direction matters. `base_view` depends on `base`, so `DROP TABLE base CASCADE` drops the view. A foreign key constraint on `dependent` that references `base` also depends on `base`, so `CASCADE` drops the **constraint** on `dependent` — but `dependent` itself is not dropped, because `dependent` does not depend on `base` (only the FK constraint does). This is usually what you want, but it surprises people who expect `CASCADE` to drop every table that references the dropped table. For "drop every table that references this one", you need to drop them explicitly.

> [!warning] `DROP` is irreversible
> `DROP TABLE` removes the file backing the table. There is no recycle bin. The only recovery paths are: a recent base backup plus WAL replay (PITR), a logical replication slot that captured the data, or a manual restore from a dump. `TRUNCATE` is similarly destructive but at least leaves the table shell; `DROP` removes the shell too. Always run `DROP` inside a transaction in interactive sessions — `BEGIN; DROP TABLE ...;` lets you `ROLLBACK` if you change your mind before `COMMIT`. See [[How would you explain DDL DML and DCL in SQL]] and [[How would you explain CREATE TABLE syntax in SQL]].

> [!tip] Interview answer
> `DROP` permanently removes a database object. PostgreSQL has `DROP TABLE`, `DROP INDEX`, `DROP VIEW`, `DROP FUNCTION`, `DROP SCHEMA`, `DROP DATABASE`, `DROP ROLE`, and more — all sharing the shape `DROP <type> [IF EXISTS] name [CASCADE | RESTRICT]`. `RESTRICT` (the default) fails with sqlstate `2BP01` if any other object depends on the target; `CASCADE` recursively drops the dependents too. `IF EXISTS` turns the "object does not exist" error into a notice. `DROP` is transactional in PostgreSQL — you can wrap it in `BEGIN`/`COMMIT` and `ROLLBACK` undoes it. `DROP DATABASE` is the exception: it cannot run inside a transaction and requires no active connections. Related: [[How would you explain DDL DML and DCL in SQL]] and [[How would you explain CREATE TABLE syntax in SQL]].
