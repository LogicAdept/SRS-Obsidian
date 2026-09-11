<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DDL #SRS

# What is an exclusion constraint in PostgreSQL

> [!abstract] Short answer
> **An exclusion constraint (`EXCLUDE`) guarantees that, for any two rows in the table, at least one of the specified operator comparisons returns `FALSE` or `NULL`.** It is a generalization of `UNIQUE`: `UNIQUE (a)` is equivalent to `EXCLUDE (a WITH =)`, but `EXCLUDE` lets you pick any operator, not just equality. The canonical use is **`EXCLUDE USING gist (room WITH =, during WITH &&)`** — no two bookings for the same room can have overlapping time ranges. It requires a GiST (or SP-GiST, GIN) index to enforce, because btree cannot index range-overlap predicates.

## Syntax and the operator pair

```sql
EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ...] ) [ ... ]
```

**Listing 1.** The `EXCLUDE` clause shape, used inside `CREATE TABLE` or as a table constraint. `index_method` is usually `gist`; `exclude_element` is a column or expression paired with an operator that must be in the operator class of the chosen index method.

Each `exclude_element` is a column or expression, paired with an operator. The constraint is violated if, for some pair of rows, **every** operator returns `TRUE`. The most common pairs:

| Element | Operator | Meaning |
|---|---|---|
| `room` | `=` | same room |
| `during` | `&&` | overlapping time range |
| `c` (circle) | `&&` | overlapping geometry |
| `ip_range` | `&&` | overlapping IP range |

The constraint fires when **all** elements match — so `EXCLUDE (room WITH =, during WITH &&)` rejects a row only if both the room is the same and the time ranges overlap. Two bookings for different rooms can have the same time range; two bookings for the same room can have adjacent (non-overlapping) time ranges.

```d2
direction: right
book1: "booking 1\nroom=1, 10:00-11:00" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
book2: "booking 2\nroom=1, 11:00-12:00" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
book3: "booking 3\nroom=1, 10:30-11:30\n(overlaps booking 1)" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}
book4: "booking 4\nroom=2, 10:00-11:00\n(same time, different room)" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
ok1: "INSERT OK" {
  width: 120
  height: 60
  style.fill: "#e8f5e9"
}
ok2: "INSERT OK\n(adjacent, not overlapping)" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
fail: "INSERT FAIL\nsqlstate 23P01" {
  width: 200
  height: 60
  style.fill: "#ffebee"
}
ok4: "INSERT OK\n(different room)" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
book1 -> ok1
book2 -> ok2
book3 -> fail
book4 -> ok4
```

**Fig. 1.** Four inserts against the `EXCLUDE (room WITH =, during WITH &&)` constraint. Booking 1 (the first insert) succeeds. Booking 2 succeeds because the ranges are adjacent, not overlapping. Booking 3 fails because it overlaps booking 1 in the same room. Booking 4 succeeds because the room is different.

## Verified on PostgreSQL 17.11

The classic room-booking example. The `btree_gist` extension is needed because the `room` column is a scalar `int` and btree-GiST lets the scalar share an index with the `tstzrange` column.

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP TABLE IF EXISTS bookings CASCADE")
    adm.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    adm.execute("""
        CREATE TABLE bookings (
            id      int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            room    int NOT NULL,
            during  tstzrange NOT NULL,
            EXCLUDE USING gist (
                room WITH =,
                during WITH &&
            )
        )
    """)

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO bookings (room, during) VALUES (1, tstzrange('2026-01-01 10:00 UTC', '2026-01-01 11:00 UTC'))")
    conn.commit()
    print("insert booking 1: room=1 10:00-11:00 — OK")

    cur.execute("INSERT INTO bookings (room, during) VALUES (1, tstzrange('2026-01-01 11:00 UTC', '2026-01-01 12:00 UTC'))")
    conn.commit()
    print("insert booking 2: room=1 11:00-12:00 — OK (adjacent, not overlapping)")

    try:
        cur.execute("INSERT INTO bookings (room, during) VALUES (1, tstzrange('2026-01-01 10:30 UTC', '2026-01-01 11:30 UTC'))")
    except psycopg.errors.ExclusionViolation as e:
        conn.rollback()
        print(f"insert booking 3: room=1 10:30-11:30 — sqlstate={e.sqlstate} — {str(e).strip().splitlines()[0]}")

    cur.execute("INSERT INTO bookings (room, during) VALUES (2, tstzrange('2026-01-01 10:00 UTC', '2026-01-01 11:00 UTC'))")
    conn.commit()
    print("insert booking 4: room=2 10:00-11:00 — OK (different room, no conflict)")

    cur.execute("SELECT room, during FROM bookings ORDER BY room, during")
    print("final bookings:")
    for r in cur.fetchall():
        print(f"  room={r[0]}  during={r[1]}")

with psycopg.connect(DSN, autocommit=True) as r:
    cur = r.execute("""
        SELECT conname, contype, pg_get_constraintdef(oid)
        FROM pg_constraint
        WHERE conrelid = 'bookings'::regclass AND contype = 'x'
    """)
    print("EXCLUDE constraint definition:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[2]}")
    cur = r.execute("""
        SELECT indexname, indexdef FROM pg_indexes
        WHERE tablename = 'bookings' AND indexname LIKE '%_excl%'
    """)
    print("underlying GiST index:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")
```

**Listing 2.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
insert booking 1: room=1 10:00-11:00 — OK
insert booking 2: room=1 11:00-12:00 — OK (adjacent, not overlapping)
insert booking 3: room=1 10:30-11:30 — sqlstate=23P01 — conflicting key value violates exclusion constraint "bookings_room_during_excl"
insert booking 4: room=2 10:00-11:00 — OK (different room, no conflict)
final bookings:
  room=1  during=[2026-01-01 10:00:00+00:00, 2026-01-01 11:00:00+00:00)
  room=1  during=[2026-01-01 11:00:00+00:00, 2026-01-01 12:00:00+00:00)
  room=2  during=[2026-01-01 10:00:00+00:00, 2026-01-01 11:00:00+00:00)
EXCLUDE constraint definition:
  bookings_room_during_excl: EXCLUDE USING gist (room WITH =, during WITH &&)
underlying GiST index:
  bookings_room_during_excl: CREATE INDEX bookings_room_during_excl ON public.bookings USING gist (room, during)
```
**Listing 3.** Verified on PostgreSQL 17.11. Booking 3 (overlapping time range for the same room) is rejected with sqlstate `23P01`. Booking 4 (same time range, different room) is accepted because the `room WITH =` clause fails before the `during WITH &&` clause can match. The constraint is backed by a GiST index on `(room, during)`, created automatically when the constraint was added.

## When `EXCLUDE` is the right tool

`EXCLUDE` answers questions that `UNIQUE` cannot:

- **Booking/calendar**: no two bookings for the same resource can overlap in time.
- **Pricing**: no two price rules for the same product can apply to the same date range.
- **IP allocation**: no two subnets in the same table can overlap.
- **Geometry**: no two shapes in the same layer can overlap (using the `&&` operator on `geometry` or `circle` types).

The alternative without `EXCLUDE` is application-level locking: take a row lock on the parent resource, then check for conflicts, then insert. That works but it serializes all inserts for the same resource and requires careful ordering to avoid deadlocks. `EXCLUDE` enforces the invariant at the database level with a GiST index probe, so concurrent inserts that do not conflict can proceed in parallel; conflicting inserts fail with `23P01`.

> [!warning] `EXCLUDE` requires a GiST, SP-GiST, GIN, or BRIN index — btree is not enough
> A btree index can answer equality (`=`) and range (`<`, `>`) queries, but it cannot answer "do these two ranges overlap" without scanning. `EXCLUDE` with a range-overlap operator (`&&`) needs a GiST index, which supports range overlap natively. The `btree_gist` extension is required when you want to combine scalar columns (int, text) with range columns in the same `EXCLUDE` constraint — without it, GiST does not know how to index the scalar `=` operator. The error message when you forget the extension is "data type integer has no default operator class for access method gist"; install `btree_gist` and retry.

> [!warning] The constraint does not help with `NULL` boundaries unless ranges are typed
> A `tstzrange` with one bound as `NULL` means "unbounded" — `[2026-01-01 10:00, NULL)` is the range from 10:00 onward, and it overlaps with any range that starts after 10:00. This is usually what you want. The trap is using two separate `timestamp` columns (`start_at`, `end_at`) and trying to express overlap with `<` and `>` operators — that requires a more complex `EXCLUDE` expression and does not handle `NULL` end_at cleanly. Use a range type (`tstzrange`, `daterange`, `int4range`) so the database knows the semantics.

> [!warning] Conflicts surface as `23P01`, not `23505`
> A `UNIQUE` violation is sqlstate `23505` (`unique_violation`). An `EXCLUDE` violation is sqlstate `23P01` (`exclusion_violation`). Application retry logic that catches only `23505` will miss `EXCLUDE` conflicts. If you retry on `23P01`, you typically need to give up (the conflict is real, not transient) or change the input — re-running the same insert will keep failing.

> [!tip] Interview answer
> An exclusion constraint (`EXCLUDE`) guarantees that for any two rows, at least one of the specified operator comparisons returns `FALSE` or `NULL`. It generalizes `UNIQUE`: `UNIQUE (a)` is `EXCLUDE (a WITH =)`, but `EXCLUDE` lets you use any operator, like `&&` for range or geometry overlap. The canonical example is `EXCLUDE USING gist (room WITH =, during WITH &&)` — no two bookings for the same room can overlap in time. It requires a GiST (or SP-GiST, GIN, BRIN) index; btree cannot index range overlap. Use the `btree_gist` extension when combining scalar columns with range columns. Conflicts surface as sqlstate `23P01`, not `23505`. Related: [[How would you explain CREATE TABLE syntax in SQL]] and [[What is foreign key cascading in a relational database]].
