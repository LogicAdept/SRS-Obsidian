<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is the difference between PRIMARY KEY and ORDER BY in ClickHouse

> [!abstract] Short answer
> ORDER BY defines the sorting key: how rows are physically sorted inside each data part, which drives compression and scan locality. PRIMARY KEY defines the sparse index: which of those sorted values get marks. If you specify only ORDER BY, the primary key equals it; a separate PRIMARY KEY must be a prefix of ORDER BY and is rarely needed.

## The two roles, per the engine docs

The MergeTree documentation is explicit: ORDER BY is the sorting key — a tuple of columns or expressions — and if no primary key is defined, ClickHouse uses the sorting key as the primary key. PRIMARY KEY is optional and must be contained in the primary-key prefix relationship with the sorting key; the docs state it is usually unnecessary to specify it separately. The reason a prefix relationship is allowed at all: the index marks need only bound granules, and a shorter key still sorts them usefully, while the full ORDER BY expression can include extra expression columns (the docs' example is SAMPLE BY with intHash32(UserID) appended to ORDER BY) that shape sorting without adding index breadth.

```sql
-- the common case: one key does both jobs
CREATE TABLE events
(
    ts      DateTime,
    user_id UInt64,
    url     String
) ENGINE = MergeTree
ORDER BY (user_id, ts);

-- rare case: index a prefix, sort by more
CREATE TABLE events2
(
    ts      DateTime,
    user_id UInt64,
    url     String
) ENGINE = MergeTree
PRIMARY KEY (user_id)
ORDER BY (user_id, ts);
```

**Listing 1.** In the second form the sparse index marks user_id only, while parts are additionally sorted by ts within each user.

## What each one buys you in queries

The sorting key is what makes `WHERE user_id = 42 AND ts >= ...` cheap twice: granules are pruned by the sparse index built on the key prefix, and within a granule the sortedness improves compression and locality. The primary key alone defines nothing about physical order — its marks only exist because the data is sorted by ORDER BY. That division matters when choosing keys for dashboards and logs, per [[How do you choose ORDER BY in ClickHouse]] and [[How do you search logs in ClickHouse]]; and the read-side verification of both effects is granule accounting in EXPLAIN indexes = 1, per [[How do you verify a ClickHouse index is used]]. The concept map to row-store engines runs through [[What is a sparse primary index in ClickHouse]] versus the clustered-index world of [[What is the difference between clustered and non clustered database indexes]].

> [!warning] "PRIMARY KEY in ClickHouse is like PRIMARY KEY in MySQL" — it is not
> The ClickHouse primary key is not a uniqueness constraint: duplicate key values are allowed and normal. It is also not the storage layout by itself — ORDER BY is. And unlike MySQL's InnoDB, you cannot index arbitrary secondary columns with B-tree-style seeks; everything else falls to skip indexes. Answering this question with OLTP habits is the classic tell of not having read the MergeTree docs.

> [!tip] Interview answer
> ORDER BY is the sorting key: it physically orders rows within each part, driving compression and scan locality. PRIMARY KEY is the sparse index over granules, and if omitted it defaults to the sorting key; when both are given, PRIMARY KEY must be a prefix of ORDER BY. Neither enforces uniqueness — ClickHouse happily stores duplicate keys — and neither enables row-level seeks; they prune granules.
