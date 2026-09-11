<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Indexes/Partial #SRS

# What is a partial index in PostgreSQL?

> [!abstract] Short answer
> A partial index is a regular index built over a subset of the table, defined by a WHERE clause at creation time. It indexes only rows matching the predicate — for example, only unprocessed orders — so it is smaller, faster, and cheaper to maintain than a full index, as long as queries carry the same predicate.

## How it works

```sql
CREATE INDEX pending_orders_idx ON orders (created_at)
  WHERE status = 'pending';
CREATE INDEX active_users_email ON users (email)
  WHERE deleted_at IS NULL;
```

**Listing 1.** Two classic uses: a work-queue slice and soft-delete exclusion. The index contains entries only for matching rows.

The planner uses a partial index when it can prove from the query's own conditions that every row it needs is inside the index predicate — the query predicate must imply the index predicate. `WHERE status = 'pending' AND created_at > now() - interval '1 day'` matches the first index; a bare `WHERE created_at > ...` does not.

```d2
table: "orders\nall rows" {width: 220; height: 70}
full: "Full index\nentry per row" {width: 220; height: 70}
part: "Partial index\nentry per pending row only" {width: 300; height: 70}
table -> full: "typical"
table -> part: "status = pending slice"
```

**Fig. 1.** The partial index is a workload-shaped index: it covers the hot slice the queries actually touch.

## When it wins

- One hot value dominates: "pending", "unprocessed", "NULL end-date" rows are few compared to history.
- Soft delete: indexing `WHERE deleted_at IS NULL` removes tombstones from the index.
- Column with mostly one value: pairs with the general low-cardinality reasoning in [[Does it make sense to index low-cardinality columns]] — a partial index is often the honest answer there.
- Enforce uniqueness only on a slice: partial UNIQUE indexes (for example, one active subscription per user) — where a full unique index cannot express the rule.

## Cost model

Smaller index means: fewer pages to read, cheaper updates (only matching rows change the index), faster builds. The price is precision: queries without the predicate fall back to other plans ([[Why might PostgreSQL choose a sequential scan instead of an index]]), and matching depends on the planner seeing the literal predicate or a provably implied one.

> [!warning] A tiny predicate mismatch silently disables the index
> `status = 'PENDING'`, a missing condition, or a functionally equivalent but differently written clause can make the planner refuse the partial index. Test with EXPLAIN ([[How do you read EXPLAIN ANALYZE in PostgreSQL]]); do not assume similarity of meaning is enough — implication must be provable.

> [!tip] Interview answer
> A partial index stores entries only for rows matching a WHERE clause fixed at creation — think "only pending orders" or "only not-deleted users". It is smaller and cheaper to maintain, and the planner uses it when the query's predicates imply the index predicate. It is also the clean way to enforce unique-on-a-subset rules.
