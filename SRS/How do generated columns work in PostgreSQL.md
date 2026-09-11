<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DDL #SRS

# How do generated columns work in PostgreSQL

> [!abstract] Short answer
> **A generated column is computed from other columns in the same row and cannot be written to directly.** PostgreSQL 17 implements only **`STORED`** generated columns — the value is computed on `INSERT`/`UPDATE` and occupies disk like a normal column. The generation expression must be **immutable**, cannot reference other generated columns or system columns (except `tableoid`), and cannot use subqueries. The keyword `DEFAULT` is the only way to "supply" a value for a generated column on insert. PostgreSQL 18 adds `VIRTUAL` generated columns (computed on read, no storage).

## Shape and rules

```sql
CREATE TABLE people (
    height_cm numeric,
    height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
);
```

**Listing 1.** The `GENERATED ALWAYS AS (...) STORED` clause defines a stored generated column. The expression is evaluated when the row is written; the result is stored and read back like any other column.

The constraints on the generation expression come from the PostgreSQL manual (`ddl-generated-columns.html`):

| Rule | Reason |
|---|---|
| Immutable functions only | The value is computed once at write time; the database must be able to recompute it consistently after a dump/restore |
| No subqueries | A generated column depends only on the current row |
| No reference to other generated columns | Prevents ordering problems in the computation chain |
| No reference to system columns (except `tableoid`) | System columns (`ctid`, `xmin`, etc.) change invisibly to the user |
| Cannot have a column default or identity definition | A generated column is its own "default" |
| Cannot be part of a partition key | The partitioner needs a stable, user-supplied value |

A column `DEFAULT` is different from a generated column in two ways: a default is evaluated **once** at insert (if no value is supplied) and can be overridden; a generated column is recomputed **every** time the row changes and cannot be overridden. A default may use volatile functions (`random()`, `now()`); a generation expression may not.

```d2
direction: right
src: "height_cm numeric\n(user-supplied)" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
expr: "height_cm / 2.54\n(immutable expression)" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
gen: "height_in numeric\nGENERATED ALWAYS AS ... STORED" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
src -> expr: "on INSERT or UPDATE of height_cm"
expr -> gen: "value written to disk"
```

**Fig. 1.** The user writes `height_cm`; PostgreSQL computes `height_in` from the generation expression and stores both. The generated column cannot be written to directly — only `DEFAULT` is accepted.

## Verified on PostgreSQL 17.11

The empiric below shows the four behaviors an interviewer expects: explicit insert into a generated column is rejected; `DEFAULT` is accepted; `UPDATE` of the base column re-computes the generated one; a volatile function in the generation expression is rejected; the generated column can be indexed and the planner uses the index.

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS people")
    adm.execute("""
        CREATE TABLE people (
            height_cm numeric,
            height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
        )
    """)

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO people (height_cm, height_in) VALUES (180, 70.8)")
    except psycopg.errors.GeneratedAlways as e:
        conn.rollback()
        print(f"INSERT explicit value into generated column: sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")

    cur.execute("INSERT INTO people (height_cm, height_in) VALUES (180, DEFAULT)")
    cur.execute("INSERT INTO people (height_cm) VALUES (50)")
    cur.execute("INSERT INTO people (height_cm) VALUES (NULL)")
    cur.execute("SELECT height_cm, height_in FROM people ORDER BY height_cm NULLS LAST")
    for r in cur.fetchall():
        print(f"  height_cm={r[0]}  height_in={r[1]}")

    cur.execute("UPDATE people SET height_cm = 200 WHERE height_cm = 180")
    cur.execute("SELECT height_cm, height_in FROM people WHERE height_cm = 200")
    r = cur.fetchone()
    print(f"after UPDATE base column: height_cm={r[0]}  height_in={r[1]}")
    conn.commit()

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS bad_gen")
    try:
        adm.execute("CREATE TABLE bad_gen (a int, b int GENERATED ALWAYS AS (a + random()) STORED)")
    except psycopg.errors.InvalidObjectDefinition as e:
        print(f"volatile random() in generated column: sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")

    adm.execute("CREATE INDEX people_height_in_idx ON people (height_in)")
    adm.execute("ANALYZE people")

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("SET enable_seqscan = off")
    cur.execute("EXPLAIN (COSTS OFF) SELECT * FROM people WHERE height_in = 19.685039370078740")
    for r in cur.fetchall():
        print(f"  {r[0]}")
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
INSERT explicit value into generated column: sqlstate=428C9 — cannot insert a non-DEFAULT value into column "height_in"
  height_cm=50  height_in=19.6850393700787402
  height_cm=180  height_in=70.8661417322834646
  height_cm=None  height_in=None
after UPDATE base column: height_cm=200  height_in=78.7401574803149606
volatile random() in generated column: sqlstate=42P17 — generation expression is not immutable
  Index Scan using people_height_in_idx on people
    Index Cond: (height_in = 19.685039370078740)
```
**Listing 2.** Verified on PostgreSQL 17.11: inserting an explicit value into `height_in` is rejected with sqlstate `428C9`; inserting with `DEFAULT` works; updating `height_cm` re-computes `height_in`; `random()` in the generation expression is rejected with `42P17` (not immutable); the generated column is indexable, and the planner picks the index when `enable_seqscan=off`.

## When to use a generated column vs an expression index

A generated column and an expression index (`CREATE INDEX ... ON tbl ((a + b))`) both let you query a computed value efficiently, but they differ in important ways. A generated column stores the value, so it is cheap to read but costs disk; an expression index stores only the index entries, so it is cheaper on disk but recomputes the expression on every index probe. A generated column can be part of a foreign key or a `CHECK` constraint; an expression index cannot be the target of a foreign key, though it can back a `UNIQUE` constraint. A generated column appears in `\d` and `SELECT *`; an expression index does not. The usual rule: if you query the value often and want it visible, use a generated column; if you only need to filter by it, use an expression index.

> [!warning] `STORED` is the only kind in PostgreSQL 17; `VIRTUAL` is in PostgreSQL 18+
> The SQL standard distinguishes stored and virtual generated columns. PostgreSQL 17 implements only `STORED` — the keyword is **required** in `GENERATED ALWAYS AS (...) STORED`. Virtual generated columns (computed on read, no storage) ship in PostgreSQL 18. Code that assumes virtual generation is portable across versions will be wrong on PG 17; code that assumes storage cost is zero will be wrong on PG 18. Always state the version when discussing generated columns.

> [!warning] Generated columns are skipped by logical replication
> A generated column on the source database is **not** published by `CREATE PUBLICATION` and is not in the default column list. The subscriber must define the same generated column itself — the subscriber's generation expression is what runs on the subscriber side. Mixing a generated column on the publisher with a plain column on the subscriber (or vice versa) breaks logical replication silently. Also, generated columns are computed **after** `BEFORE` triggers fire, so a `BEFORE` trigger that modifies the base column will see its change reflected in the generated value — but a `BEFORE` trigger that tries to **read** the generated column will fail, because the value is not yet computed. See [[How do you add a column to a large PostgreSQL table without downtime]] and [[How would you explain CREATE TABLE syntax in SQL]].

> [!tip] Interview answer
> A generated column is computed from other columns in the same row and stored on disk (PG 17 implements only `STORED`; `VIRTUAL` arrives in PG 18). The expression must be immutable, cannot use subqueries, cannot reference other generated columns or system columns, and cannot be a partition key. You write to the base columns; PostgreSQL computes the generated column automatically. You cannot insert an explicit value into it — only `DEFAULT`. Use it when you query the derived value often and want it visible; use an expression index when you only need to filter by it. Generated columns can be indexed and can back a `UNIQUE` constraint, but they are skipped by logical replication. Related: [[How would you explain CREATE TABLE syntax in SQL]] and [[How would you explain DDL DML and DCL in SQL]].
