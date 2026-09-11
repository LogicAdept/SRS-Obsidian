<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/SQL #SRS

# How would you explain foreign keys in relational databases?

> [!abstract] Short answer
> A foreign key is a column (or group of columns) constrained to hold only values that exist in the referenced table's key columns. It is the mechanism that maintains referential integrity between two tables: the engine checks every write against the parent and rejects orphan rows. What happens to children when the parent row disappears is not left to chance — it is chosen per constraint with a referential action.

## The contract and what it may reference

PostgreSQL's documentation states the contract directly: foreign key values "must match the values appearing in some row of another table", and "we say this maintains the referential integrity between two related tables". If you omit the column list, the parent's primary key is the referenced column; an explicit list may target any UNIQUE columns of the parent — the referenced side must carry a uniqueness constraint so the engine can resolve a value to at most one parent row ([[What integrity constraints exist in SQL]]). A foreign key may also be a group of columns referencing a composite unique key, written as a table constraint. And the check is one-sided on NULL: a NULL in the child column is not validated at all, so an optional relationship is expressed by leaving the FK nullable ([[Can a column referenced by a foreign key be NULL]]).

```sql
CREATE TABLE tenants (id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE);
CREATE TABLE invoices (id INTEGER PRIMARY KEY,
  tenant_code TEXT REFERENCES tenants(code) ON DELETE CASCADE,
  total NUMERIC NOT NULL);
INSERT INTO tenants VALUES (1, 'acme');
INSERT INTO invoices VALUES (10, 'acme', 50);
-- ok: references the UNIQUE code column, not the PK
INSERT INTO invoices VALUES (11, 'nope', 50);
-- ERROR: FOREIGN KEY constraint failed
INSERT INTO invoices VALUES (12, NULL, 50);
-- ok: NULL FK = relationship absent, nothing to validate
DELETE FROM tenants WHERE id = 1;
SELECT * FROM invoices;
-- 12| |50   (CASCADE removed invoice 10; the NULL-FK row survives)
```

**Listing 1.** Verified on SQLite 3.53.1 with `PRAGMA foreign_keys = ON`. The FK targets a UNIQUE business column, the bogus reference dies, the NULL passes, and CASCADE cleans up children on parent delete.

```d2
direction: right
w: "write to child row" {width: 170; height: 70; style.fill: "#e3f2fd"}
c: "value in parent
key columns?" {width: 190; height: 70; style.fill: "#e3f2fd"}
ok: "accepted" {width: 120; height: 60; style.fill: "#e8f5e9"}
or: "orphan ->
rejected" {width: 140; height: 60; style.fill: "#ffebee"}
pd: "parent deleted" {width: 160; height: 60; style.fill: "#fff3e0"}
act: "referential action:
CASCADE / SET NULL /
RESTRICT / NO ACTION" {width: 220; height: 80; style.fill: "#fff3e0"}
w -> c
c -> ok
c -> or
pd -> act
```

**Fig. 1.** Two gates: every child write is validated against the parent key, and every parent deletion is routed through the constraint's declared action instead of silently orphaning children.

## Referential actions are part of the design, not a footnote

The default is NO ACTION: the deletion is checked at constraint time and usually errors. RESTRICT is the stricter sibling — same rejection, but it cannot be deferred inside a transaction. CASCADE propagates the delete to referencing rows and fits part-whole relationships (order lines die with the order); SET NULL and SET DEFAULT detach children instead and fit optional relationships. PostgreSQL documents all of these in the constraints chapter, including that SET actions "do not excuse you from observing any constraints" — the detached row must still satisfy everything else declared on it ([[What is foreign key cascading in a relational database]] walks the cascade case in depth).

> [!warning] An unindexed foreign key column punishes the parent
> PostgreSQL creates a unique index for the parent key automatically but indexes nothing on the child: every parent DELETE or key update must scan the child table unless you index the FK column yourself — the classic cause of "a one-row delete took minutes". SQLite, for its part, enforces FKs only with `PRAGMA foreign_keys = ON` per connection, off by default. Both are documented behavior, and both are why [[Why should you index foreign keys]] is its own topic.

> [!tip] Interview answer
> A foreign key ties child values to existing parent values — the mechanism behind referential integrity. It references the parent's primary key by default, or any unique column explicitly; NULLs pass unvalidated, which is how optional relationships are modeled. Deletes follow the declared action: NO ACTION or RESTRICT to block, CASCADE to propagate, SET NULL or SET DEFAULT to detach. The production nuance I always add: PostgreSQL does not index the child column for you, so parent deletes scan it unless you do.

