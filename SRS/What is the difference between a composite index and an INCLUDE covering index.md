<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes/Covering #Databases/Indexes/Composite #SRS

# What is the difference between a composite index and an INCLUDE covering index?

> [!abstract] Short answer
> A composite index makes extra columns part of the key: they extend the sorted key space, can be used in index conditions, and affect uniqueness. An INCLUDE column is payload: it is stored in leaf tuples so an index-only scan can return it, but it cannot be searched on and does not count for uniqueness. Key columns also live in upper tree levels; INCLUDE columns do not, which keeps non-leaf pages slim.

## Mechanics

```sql
CREATE INDEX on orders (customer_id, created_at);                 -- composite
CREATE INDEX on orders (customer_id) INCLUDE (created_at, status);-- covering
```

**Listing 1.** Same two data needs, different tool: if you filter or sort by `created_at` within a customer, you need it in the key; if you only need it returned, INCLUDE suffices.

- Composite `(a, b)`: supports conditions on `a`, then `a AND b`; the order defines usefulness ([[How do database indexes work at a high level]]). Unique constraints over `(a, b)` treat both as the key.
- INCLUDE `(a) INCLUDE (b)`: the B-tree is effectively on `a`; `b` rides along in leaves. Constraints and search ignore `b`.

```d2
comp: "Composite (a, b)\nb is sorted inside a\nsearchable + orderable" {width: 330; height: 90}
inc: "INCLUDE (a) + b\nb only in leaf payload\nindex-only scan fuel" {width: 330; height: 90}
key: "Uniqueness / search" {width: 240; height: 60}
comp -> key: "participates"
inc -> key: "no"
```

**Fig. 1.** INCLUDE columns exist to satisfy SELECT lists; key columns exist to satisfy WHERE and ORDER BY.

## Why INCLUDE can be cheaper

Key columns are copied into internal index entries and participate in deduplication and tree navigation; payload columns are not, so the upper levels stay compact and the index is smaller for the same data. INCLUDE also accepts types without a B-tree operator class (within limits) — you can attach a jsonb or a wide text payload to a B-tree on an integer key. This is the machinery behind the concept in [[How would you explain Covering index]] and the optimizer behavior in [[What is an index-only scan in PostgreSQL]].

## When to use which

- Query: `WHERE customer_id = ? ORDER BY created_at` — composite; ORDER BY needs the key order.
- Query: `WHERE customer_id = ?` returning `status`, `total` — INCLUDE; index-only scan without bloating the key.
- Uniqueness on `(tenant_id, email)` — composite (INCLUDE cannot enforce it).
- Both exist in other engines with different names; in PostgreSQL INCLUDE arrived with PostgreSQL 11 on B-tree (later GiST/SP-GiST).

> [!warning] INCLUDE is not a free "just add columns" bag
> Every included column still enlarges leaf tuples and the index on disk and in cache, and it must be maintained on every insert and on updates that touch it. A wide INCLUDE list recreates the "index everything" problem in one structure ([[What goes wrong with indexing every field combination for flexible search]]).

> [!tip] Interview answer
> Composite puts extra columns into the sorted key — searchable, orderable, counted by uniqueness. INCLUDE keeps them as leaf payload only: unusable for search, invisible to constraints, but enough to make the scan index-only and to keep upper tree levels slim. Filter-or-sort by the column: key. Just return it: INCLUDE.
