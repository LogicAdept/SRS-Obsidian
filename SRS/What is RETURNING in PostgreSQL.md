<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DML #SRS

# What is RETURNING in PostgreSQL?

> [!abstract] Short answer
> RETURNING is a clause on INSERT, UPDATE, DELETE and MERGE that makes the statement return the rows it actually affected — like a SELECT run against the changed rows, evaluated after the change. It kills the extra round trip of "write, then select by id": defaults, sequence values, computed columns and audit data come back in the same call.

## What it returns

- INSERT: the rows as inserted — defaults and generated values resolved (the canonical use: fetching the identity value).
- UPDATE: the rows as updated (new values; PostgreSQL 18 adds OLD/NEW aliasing to see both).
- DELETE: the rows as they were before deletion.
- With ON CONFLICT DO UPDATE: the rows actually inserted or updated; rows skipped by a failed WHERE are not returned.

```sql
INSERT INTO orders (customer_id, total)
VALUES (42, 199.00)
RETURNING id, created_at;              -- server-generated values

UPDATE stock SET qty = qty - 1
WHERE sku = 'A-1' AND qty > 0
RETURNING sku, qty;                    -- zero rows if the guard failed
```

**Listing 1.** The two workhorses: getting generated keys, and turning a conditional update into an atomic read-modify-write whose outcome you can inspect.

```d2
stmt: "DML statement" {width: 200; height: 60}
apply: "Apply change\nper row" {width: 220; height: 60}
ret: "RETURNING\nemit affected row\n(post-change values)" {width: 300; height: 70}
net: "No second round trip\nno SELECT ... WHERE id = ..." {width: 320; height: 70}
stmt -> apply -> ret -> net
```

**Fig. 1.** RETURNING closes the loop in one statement; the alternative is a second query plus its race window.

## Where it shines

- Idempotent upserts that must report what happened: RETURNING plus ON CONFLICT tells the caller which rows were created versus updated ([[How does UPSERT work in PostgreSQL]]).
- Atomic guarded updates: the `qty > 0` pattern returns zero rows when the guard rejected, instead of selecting first.
- Batch deletes with audit: DELETE ... RETURNING feeds a log in one statement.
- ORM and query-builder support is broad; JDBC returns them as a result set ([[How are database query results processed in JDBC]] covers the JDBC side).

> [!warning] RETURNING is evaluated per affected row, not a full SELECT
> You cannot join it against arbitrary tables or order it as a query plan of its own — it projects the mutated rows. Also under Read Committed, an UPDATE re-evaluates its WHERE against rows concurrently changed mid-statement ([[What are SQL transaction isolation levels]]); the returned rows are the final ones of that statement, which can surprise people replaying the same statement twice.

> [!tip] Interview answer
> RETURNING makes DML return the rows it changed — defaults and generated keys after INSERT, new values after UPDATE, pre-images after DELETE — evaluated per affected row. It removes the write-then-select round trip, powers atomic guarded updates and upsert reporting, and pairs with ON CONFLICT to distinguish created from updated rows.
