<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DML #SRS

# How does UPSERT work in PostgreSQL?

> [!abstract] Short answer
> The native form is INSERT with an ON CONFLICT clause: for each proposed row, either the insert proceeds, or — if it violates an arbiter unique or exclusion constraint named by conflict_target — DO NOTHING skips it or DO UPDATE rewrites the existing row, referencing proposed values through the special excluded table. MERGE (SQL standard, PostgreSQL 15+) is the second, more general upsert.

## The mechanics

```sql
INSERT INTO stock (sku, qty) VALUES ('A-1', 5)
ON CONFLICT (sku) DO UPDATE
  SET qty = stock.qty + excluded.qty;   -- existing row + proposed row
```

**Listing 1.** The classic counter: conflict on the unique index of sku; the update reads the old value and adds the new one from `excluded`.

- conflict_target names the arbiter: columns backed by a unique index, or a constraint name, or nothing (any unique violation; DO NOTHING only).
- DO UPDATE can have a WHERE clause — when it fails, the row is silently skipped, and it will not appear in RETURNING.
- Uniqueness is checked against unique or exclusion constraints only; there is nothing to arbitrate on a plain table.

```d2
ins: "INSERT row" {width: 180; height: 60}
chk: "Unique/exclusion\nindex hit?" {width: 240; height: 70}
ok: "Insert" {width: 160; height: 60}
dn: "DO NOTHING\nskip" {width: 200; height: 60}
du: "DO UPDATE\nrewrite, excluded = proposed" {width: 300; height: 70}
ins -> chk
chk -> ok: no
chk -> dn: yes + DO NOTHING
chk -> du: yes + DO UPDATE
```

**Fig. 1.** Per-row arbitration: one statement mixes inserted and updated outcomes freely.

## Concurrency semantics

Under Read Committed, if a concurrent transaction has inserted or updated the conflicting row but not yet committed, the upsert waits; after the other commits, the DO UPDATE branch applies its update to the row the other transaction wrote, even though that version was not visible at statement start. Under Repeatable Read, the same race raises a serialization failure instead. This is documented behavior and the reason upserts are retry-safe under RC ([[What are SQL transaction isolation levels]]).

## MERGE as the alternative

MERGE (PostgreSQL 15+) matches source rows against the target with a full join condition and can INSERT, UPDATE, or DELETE per match, with NOT MATCHED branches. More expressive; heavier to reason about for the single-row upsert case, and its concurrency interactions are stricter — for a pure key-based upsert, ON CONFLICT remains the recommendation.

> [!warning] ON CONFLICT does not arbitrate on "any difference"
> It fires only on unique/exclusion constraint violations of the arbiter you name. A foreign-key violation, a CHECK failure, or a conflict on a different unique index than the one you named raises an error. Assuming "upsert handled everything" is how deadlocked batches and constraint errors reach production ([[What is a unique database constraint for]]).

> [!tip] Interview answer
> PostgreSQL upsert is INSERT ON CONFLICT: name an arbiter unique index, then DO NOTHING or DO UPDATE with the excluded pseudo-row for proposed values. Under Read Committed it waits out concurrent writers and updates their committed row; under Repeatable Read it serialization-fails. MERGE since PostgreSQL 15 covers richer match-and-apply logic.
