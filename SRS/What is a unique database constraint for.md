<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/SQL #SRS

# What is a unique database constraint for?

> [!abstract] Short answer
> A UNIQUE constraint enforces an identifier **other than** the primary key: business invariants (email, national id), external references, and "unique within a group" rules that a single column cannot express. It rejects duplicate non-NULL values among the listed columns, creates a unique B-tree index that also serves lookups, and — the sharp edge — passes NULLs because NULL never equals anything ([[What does NULL mean in SQL]]).

## The jobs UNIQUE does that the primary key cannot

The primary key is one identifier per table; real tables usually need several. PostgreSQL's docs put UNIQUE constraints in exactly that role: a uniqueness restriction on the column or group is declared declaratively, and "adding a unique constraint will automatically create a unique B-tree index on the column or group of columns". In relational vocabulary those enforced-but-not-chosen identifiers are the table's other candidate keys ([[How would you explain candidate keys in relational databases]]), in SQL practice they are alternate keys ([[How would you explain alternate or secondary keys in relational databases]]). Composite forms buy per-group rules — `(tenant_id, email)` unique *per tenant* — and, where the engine supports them, partial unique indexes buy conditional rules ("at most one active owner per tenant") that plain constraints cannot state. PostgreSQL documents the partial-index escape hatch explicitly: "a uniqueness restriction covering only some rows cannot be written as a unique constraint, but it is possible to enforce such a restriction by creating a unique partial index" ([[What is a partial index in PostgreSQL]]).

```sql
CREATE TABLE memberships (
  tenant_id INTEGER NOT NULL,
  email TEXT NOT NULL,
  role TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1
);
CREATE UNIQUE INDEX uq_tenant_email ON memberships (tenant_id, email);
INSERT INTO memberships VALUES (1, 'a@x.io', 'admin', 1);
INSERT INTO memberships VALUES (2, 'a@x.io', 'admin', 1);
-- ok: same email, different tenant -- the rule is per group
INSERT INTO memberships VALUES (1, 'a@x.io', 'viewer', 1);
-- ERROR: UNIQUE constraint failed: memberships.tenant_id, memberships.email
CREATE UNIQUE INDEX uq_one_owner ON memberships (tenant_id, role) WHERE active = 1;
INSERT INTO memberships VALUES (1, 'b@x.io', 'owner', 1);
INSERT INTO memberships VALUES (1, 'c@x.io', 'owner', 1);
-- ERROR: UNIQUE constraint failed: memberships.tenant_id, memberships.role
INSERT INTO memberships VALUES (1, 'd@x.io', 'owner', 0);
-- ok: inactive rows sit outside the partial index predicate
```

**Listing 1.** Verified on SQLite 3.53.1. A composite unique index enforces the per-tenant rule; a partial unique index enforces "one active owner per tenant" while leaving inactive rows free — two rules a single-column constraint could not state.

```d2
direction: right
u: "UNIQUE constraint
or unique index" {width: 190; height: 75; style.fill: "#e3f2fd"}
a: "alternate key
business identifier" {width: 210; height: 70; style.fill: "#e8f5e9"}
b: "composite: unique
within a group" {width: 200; height: 70; style.fill: "#e8f5e9"}
c: "partial: unique
only inside WHERE" {width: 200; height: 70; style.fill: "#e8f5e9"}
u -> a
u -> b
u -> c
```

**Fig. 1.** One mechanism, three jobs: plain alternate keys, per-group composite rules, and conditional rules via partial unique indexes — all enforced by the engine at write time.

> [!warning] Multiple NULLs can hollow out the invariant the constraint was bought for
> Because NULLs are never equal for uniqueness, a UNIQUE email column happily holds any number of "no email yet" rows — usually intended, occasionally the hole that defeats the rule. Two complements close it when needed: add NOT NULL so absence is impossible, or scope the constraint with a partial unique index so it only applies where the invariant makes sense. The same write-time index that enforces the rule also taxes every insert and update on those columns — each UNIQUE is one more B-tree to maintain ([[What is the difference between PRIMARY KEY and UNIQUE]]).

> [!tip] Interview answer
> UNIQUE exists to enforce identifiers beyond the primary key: business invariants like email, external references, per-group composite rules, and — where the engine allows partial unique indexes — conditional rules like "one active owner per tenant". It creates a unique B-tree, so enforcement and fast lookups arrive together, at the cost of index maintenance on writes. And I always mention the NULL semantics: NULLs pass uniqueness, so an invariant that must hold even for missing values needs NOT NULL or a partial index next to it.

