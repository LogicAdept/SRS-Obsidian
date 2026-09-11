<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# Why does LIKE with a leading wildcard not use a B-tree index

> [!abstract] Short answer
> A B-tree stores strings in lexicographic order, and a seek needs the start of the range. LIKE 'abc%' bounds the range below and above, but '%abc' or '%abc%' can match anywhere inside the string, so no contiguous range of the index satisfies the predicate and the engine must check every row.

## The ordering argument

Think of a dictionary: you can jump to all words starting with "smi" because they are physically adjacent in the sort order. Words containing "smith" anywhere are not adjacent — they are scattered across the whole dictionary — so the only way to answer contains-style patterns from the dictionary itself is to read it all. PostgreSQL's B-tree page states the boundary precisely: the planner considers LIKE and regex indexes only when the pattern is a constant anchored to the beginning of the string, col LIKE 'foo%' or col ~ '^foo', but not col LIKE '%bar'. It adds the locale caveat: outside the C locale you need a special operator class (text_pattern_ops) for pattern queries, because default collations order text differently than byte-wise pattern matching requires.

```sql
CREATE INDEX idx_users_email ON users (email text_pattern_ops);
SELECT * FROM users WHERE email LIKE 'larr%';   -- index range scan
SELECT * FROM users WHERE email LIKE '%larr%';  -- seq scan (no range)
```

**Listing 1.** An anchored prefix seeks; a leading wildcard cannot, regardless of the index.

## What to do for contains and suffix patterns

Contains search moves to structures that index substrings or tokens rather than the whole string: pg_trgm builds trigrams and a GIN/GiST index over them, supporting LIKE, ILIKE, and similarity for '%abc%' workloads — the mechanism is in [[How does a trigram index help SQL search]] and the decision menu in [[How do you optimize substring search in SQL]]. Suffix search has the classic reverse-string trick, described in [[How do you search for a suffix efficiently in SQL]]. Natural-language word search belongs to full-text search with tsvector and GIN, per [[How does full-text search work in PostgreSQL]]. The prefix-versus-contains vocabulary this question tests is pinned down in [[What is the difference between prefix search and contains search]], and the general eligibility rule behind all of it is [[What is sargability in SQL]].

> [!warning] "LIKE never uses an index" is as wrong as "LIKE always scans"
> Anchored prefixes on B-trees are the standard fast path, subject to the operator-class/collation precondition. Conversely ILIKE with an anchored prefix still scans a plain B-tree because case folding breaks the stored order — trigram or an indexed lower() expression are the fixes. The precise rule is about the pattern shape and the index's opclass, not about LIKE as an operator.

> [!tip] Interview answer
> B-tree seeks need a contiguous range of the stored sort order. LIKE 'abc%' is a bounded range, so it seeks; '%abc' matches anywhere in the string, so matching rows are scattered and the engine must scan. The fixes are structural: trigram indexes for contains, reversed strings or trigrams for suffixes, and full-text search for word-level queries.
