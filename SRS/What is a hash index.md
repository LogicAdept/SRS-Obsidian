<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# What is a hash index

> [!abstract] Short answer
> A hash index stores a hash of each key in a hash table and answers only equality predicates: it can say "rows with exactly this key" in effectively constant time, but it cannot serve ranges, sorting, or prefix matching at all, because hashing destroys the key order.

## How it works and what it cannot do

The index computes a hash of the indexed value and places the entry in a bucket. A lookup hashes the probe value and reads that bucket directly, so equality is a constant-depth operation instead of a tree descent. The cost is that the structure knows nothing about ordering: `>`, `<`, `BETWEEN`, `ORDER BY`, and `LIKE 'abc%'` are all out of scope, and duplicate handling plus resizing are the implementation's real work. PostgreSQL's hash index stores 32-bit hash codes derived from the indexed column and the planner considers it only for the `=` operator. Historically PG hash indexes were not WAL-logged and therefore not crash-safe; they were made durable and replicated in PostgreSQL 10, which is why older advice to avoid them had a factual basis.

```sql
CREATE INDEX idx_sessions_token ON sessions USING hash (session_token);
SELECT * FROM sessions WHERE session_token = 'eyJhbGciOi...';
```

**Listing 1.** Equality-only lookups on a high-entropy token are the textbook hash index use case.

## Where the idea appears in engines

MySQL's InnoDB does not expose user-managed hash indexes but builds an Adaptive Hash Index automatically: it watches which B-tree pages are repeatedly reached with the same search pattern and adds in-memory hash entries pointing at those pages, guarded by `innodb_adaptive_hash_index` (off by default in recent versions because of its contention cost under high concurrency). Memory-store engines and embedded key-value stores use hash tables as their primary lookup structure. The interview-relevant contrast is with B-trees: a B-tree lookup is O(log n) with ordered leaves, a hash lookup is O(1) with no order, so the choice is exactly whether you ever need ranges or sorting, which connects to [[What types of database indexes exist]] and to the predicate-shape test in [[What is sargability in SQL]].

> [!warning] "Hash is O(1) so always use it" ignores collisions and workloads
> Hash indexes help only pure equality on long keys where the tree depth or key size is the bottleneck. Hash collisions still require rechecking the actual values, resizing is expensive, and any range or sort need forces a different structure. Also do not conflate a hash index with a hash join or with the hashing in hash-partitioning; they share the primitive, not the structure.

> [!tip] Interview answer
> A hash index hashes the key and jumps straight to a bucket, so equality lookups are very cheap, but it cannot do ranges, ORDER BY, or prefix search because order is lost. PostgreSQL supports hash indexes for equality only, and InnoDB implements the idea automatically as the Adaptive Hash Index over hot pages. Use it for pure point lookups on long tokens; otherwise B-tree is the safer default.
