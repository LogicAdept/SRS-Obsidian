<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/SQL/DDL #Databases/Relational/PostgreSQL #SRS

# What is foreign key cascading in a relational database

> [!abstract] Short answer
> **Foreign key cascading is the set of actions the database takes automatically when a referenced parent row is deleted or its key is updated.** PostgreSQL (and the SQL standard) defines five `ON DELETE` actions and the same five `ON UPDATE` actions: `NO ACTION` (default, can be deferred), `RESTRICT` (immediate), `CASCADE` (propagate to children), `SET NULL` (null the FK columns), `SET DEFAULT` (set the FK columns to their `DEFAULT`). The choice is part of the foreign key constraint declaration and applies per FK column.

## The five actions

| Action | `ON DELETE` behavior | `ON UPDATE` behavior |
|---|---|---|
| `NO ACTION` (default) | Block parent delete if children exist; check can be deferred to end of transaction | Block parent key update if children exist; same deferral |
| `RESTRICT` | Block parent delete immediately (no deferral) | Block parent key update immediately |
| `CASCADE` | Delete the child rows automatically | Copy the new parent key into the child rows |
| `SET NULL` | Set the child FK columns to NULL | Set the child FK columns to NULL |
| `SET DEFAULT` | Set the child FK columns to their `DEFAULT` | Set the child FK columns to their `DEFAULT` |

`NO ACTION` and `RESTRICT` look identical in the common case. The difference is **deferral**: `NO ACTION` is checked at the end of the transaction (or immediately, if the constraint is not declared `DEFERRABLE INITIALLY DEFERRED`); `RESTRICT` is always checked immediately and cannot be deferred. In practice, `RESTRICT` is the right choice when you want an immediate error, and `NO ACTION` is the right choice when you want to allow temporary violations within a transaction that you fix before commit.

```d2
direction: right
parent: "parent (id PK)" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
child: "child (id PK, parent_id FK)" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
cascade: "ON DELETE CASCADE\nchild row removed" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
setnull: "ON DELETE SET NULL\nchild row kept; parent_id -> NULL" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
restrict: "ON DELETE RESTRICT / NO ACTION\nDELETE parent fails (23503)" {
  width: 360
  height: 70
  style.fill: "#ffebee"
}
parent -> child: "DELETE parent"
child -> cascade: "if CASCADE"
child -> setnull: "if SET NULL"
child -> restrict: "if RESTRICT / NO ACTION"
```

**Fig. 1.** Three of the five `ON DELETE` actions. `CASCADE` removes the child row; `SET NULL` keeps the child and nulls the FK column; `RESTRICT`/`NO ACTION` block the parent delete with sqlstate `23503`. `SET DEFAULT` works like `SET NULL` but uses the column's `DEFAULT`; `NO ACTION` works like `RESTRICT` but can be deferred.

## Verified on PostgreSQL 17.11

Each action is exercised in isolation with its own child row, so the FK under test is the only thing blocking the parent delete. The empiric confirms the sqlstate (`23503` foreign key violation) for `RESTRICT` and `NO ACTION`, the row count for `CASCADE`, the NULL value for `SET NULL`, the sentinel value for `SET DEFAULT`, and the propagated key for `ON UPDATE CASCADE`:

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS child CASCADE")
    adm.execute("DROP TABLE IF EXISTS parent CASCADE")
    adm.execute("""
        CREATE TABLE parent (
            id int PRIMARY KEY,
            name text
        )
    """)
    adm.execute("""
        CREATE TABLE child (
            id int PRIMARY KEY,
            f_cascade int REFERENCES parent(id) ON DELETE CASCADE,
            f_restrict int REFERENCES parent(id) ON DELETE RESTRICT,
            f_no_action int REFERENCES parent(id) ON DELETE NO ACTION,
            f_set_null int REFERENCES parent(id) ON DELETE SET NULL,
            f_set_default int REFERENCES parent(id) ON DELETE SET DEFAULT DEFAULT 0,
            f_upd_cascade int REFERENCES parent(id) ON UPDATE CASCADE
        )
    """)
    adm.execute("INSERT INTO parent VALUES (0, 'unknown'), (1, 'alice'), (2, 'bob'), (3, 'carol'), (4, 'dave')")

# A: ON DELETE RESTRICT
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO child (id, f_restrict) VALUES (10, 1)")
    try:
        cur.execute("DELETE FROM parent WHERE id = 1")
    except psycopg.errors.ForeignKeyViolation as e:
        conn.rollback()
        print(f"ON DELETE RESTRICT:  sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")
    cur.execute("UPDATE child SET f_restrict = NULL WHERE id = 10")
    cur.execute("DELETE FROM parent WHERE id = 1")
    conn.commit()

# B: ON DELETE NO ACTION
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO child (id, f_no_action) VALUES (11, 2)")
    try:
        cur.execute("DELETE FROM parent WHERE id = 2")
    except psycopg.errors.ForeignKeyViolation as e:
        conn.rollback()
        print(f"ON DELETE NO ACTION: sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")
    cur.execute("UPDATE child SET f_no_action = NULL WHERE id = 11")
    cur.execute("DELETE FROM parent WHERE id = 2")
    conn.commit()

# C: ON DELETE CASCADE
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO child (id, f_cascade) VALUES (12, 3)")
    cur.execute("DELETE FROM parent WHERE id = 3")
    cur.execute("SELECT count(*) FROM child WHERE id = 12")
    print(f"ON DELETE CASCADE:   child rows remaining for id=12: {cur.fetchone()[0]}")
    conn.commit()

# D: ON DELETE SET NULL
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO child (id, f_set_null) VALUES (13, 4)")
    cur.execute("DELETE FROM parent WHERE id = 4")
    cur.execute("SELECT id, f_set_null FROM child WHERE id = 13")
    r = cur.fetchone()
    print(f"ON DELETE SET NULL:  child id={r[0]}  f_set_null={r[1]}  (was 4, now NULL)")
    conn.commit()

# E: ON DELETE SET DEFAULT
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO parent VALUES (5, 'eve')")
    cur.execute("INSERT INTO child (id, f_set_default) VALUES (14, 5)")
    cur.execute("DELETE FROM parent WHERE id = 5")
    cur.execute("SELECT id, f_set_default FROM child WHERE id = 14")
    r = cur.fetchone()
    print(f"ON DELETE SET DEFAULT: child id={r[0]}  f_set_default={r[1]}  (was 5, now DEFAULT 0 — the sentinel parent)")
    conn.commit()

# F: ON UPDATE CASCADE
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO parent VALUES (100, 'frank')")
    cur.execute("INSERT INTO child (id, f_upd_cascade) VALUES (15, 100)")
    cur.execute("UPDATE parent SET id = 200 WHERE id = 100")
    cur.execute("SELECT id, f_upd_cascade FROM child WHERE id = 15")
    r = cur.fetchone()
    print(f"ON UPDATE CASCADE:   parent 100 -> 200; child id={r[0]}  f_upd_cascade={r[1]}")
    conn.commit()
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
ON DELETE RESTRICT:  sqlstate=23503 — update or delete on table "parent" violates foreign key constraint "child_f_restrict_fkey" on table "child"
ON DELETE NO ACTION: sqlstate=23503 — update or delete on table "parent" violates foreign key constraint "child_f_no_action_fkey" on table "child"
ON DELETE CASCADE:   child rows remaining for id=12: 0
ON DELETE SET NULL:  child id=13  f_set_null=None  (was 4, now NULL)
ON DELETE SET DEFAULT: child id=14  f_set_default=0  (was 5, now DEFAULT 0 — the sentinel parent)
ON UPDATE CASCADE:   parent 100 -> 200; child id=15  f_upd_cascade=200
```
**Listing 2.** Verified on PostgreSQL 17.11. `RESTRICT` and `NO ACTION` both block the parent delete with sqlstate `23503`; the difference is deferral, not visible in this test. `CASCADE` removes the child row entirely (count = 0). `SET NULL` keeps the child and nulls the FK column. `SET DEFAULT` keeps the child and sets the FK column to the column's `DEFAULT` (0 — the sentinel parent row, which must exist for the FK to remain valid). `ON UPDATE CASCADE` propagates the new parent key to the child.

## Choosing the action

The choice is about what the child represents relative to the parent:

- **`ON DELETE CASCADE`** — the child cannot exist without the parent. Order items when an order is deleted; tags when a post is deleted.
- **`ON DELETE RESTRICT`** — the child can exist independently; the parent cannot be removed while the child references it. An employee's department: do not silently delete a department that has employees.
- **`ON DELETE NO ACTION`** — same as `RESTRICT` for the common case, but allows temporary violations inside a transaction when declared `DEFERRABLE INITIALLY DEFERRED`. Useful when you need to reorder parent and child deletes within a transaction.
- **`ON DELETE SET NULL`** — the child can exist independently and the relationship is optional. A product's `discontinued_by_user_id` when the user is deleted: keep the product, null the reference.
- **`ON DELETE SET DEFAULT`** — like `SET NULL` but uses a sentinel value (typically a "system" or "unknown" parent row with id 0 or -1). Requires the sentinel parent row to exist.

> [!warning] `CASCADE` can be a loaded footgun
> `ON DELETE CASCADE` propagates deletes recursively: if the child is itself referenced by a grandchild with `CASCADE`, the grandchild rows are also deleted. A schema with several `CASCADE` FKs in a chain can turn a single `DELETE FROM top WHERE id = ?` into a multi-table sweep that removes thousands of rows. The cascade also fires **inside the same transaction** — if the transaction aborts, the cascaded deletes roll back. The footgun is when the cascade crosses a boundary the application did not expect (e.g. deleting a `tenant` cascades to `users` cascades to `posts` cascades to `comments`), which is fine for correctness but bad for performance if the application thought it was deleting one row. Always check the FK definitions before issuing a `DELETE` on a parent table.

> [!warning] `SET DEFAULT` requires the sentinel parent row to exist
> `ON DELETE SET DEFAULT` sets the child FK column to its declared `DEFAULT`. If the `DEFAULT` value does not correspond to an existing parent row, the cascade fails with a foreign key violation (sqlstate `23503`). The standard pattern is to create a sentinel parent row (e.g. `id = 0, name = 'unknown'`) and declare `DEFAULT 0` on the child column. Forgetting the sentinel is a common production bug — the schema accepts inserts (the column has a `DEFAULT`), the first parent delete cascades correctly (the column is set to `0`), and the second parent delete fails because `0` does not exist in the parent table.

> [!warning] Index the FK column on the child side
> PostgreSQL automatically creates an index on the **referenced** (parent) columns because they must be `PRIMARY KEY` or `UNIQUE`. It does **not** automatically index the **referencing** (child) columns. A parent delete or parent key update scans the child table for matching rows — without an index on the child FK column, that scan is a full table scan and takes `ACCESS EXCLUSIVE` worth of time. For any FK on a non-trivial child table, create an explicit index on the FK column. See [[What is ACCESS EXCLUSIVE in PostgreSQL]] and [[How would you explain CREATE TABLE syntax in SQL]].

> [!tip] Interview answer
> Foreign key cascading is the set of actions the database takes when a referenced parent row is deleted or its key is updated. PostgreSQL supports five `ON DELETE` actions and five matching `ON UPDATE` actions: `NO ACTION` (default, can be deferred), `RESTRICT` (immediate), `CASCADE` (propagate), `SET NULL`, `SET DEFAULT`. `CASCADE` deletes child rows or copies the new parent key; `SET NULL` keeps the child and nulls the FK; `SET DEFAULT` keeps the child and sets the FK to the column's `DEFAULT` (which must point to an existing parent row). Choose `CASCADE` when the child cannot exist without the parent, `RESTRICT` when the child is independent, `SET NULL` when the relationship is optional. Index the FK column on the child side — PostgreSQL does not do it for you. Related: [[How would you explain CREATE TABLE syntax in SQL]] and [[What is ACCESS EXCLUSIVE in PostgreSQL]].
