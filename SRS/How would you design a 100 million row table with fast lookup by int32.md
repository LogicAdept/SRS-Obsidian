<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you design a 100 million row table with fast lookup by int32?

> [!abstract] Short answer
> For "100M rows, instant lookup by int32 id": make the id the **clustered primary key** — `INTEGER PRIMARY KEY` in SQLite (a rowid alias: the table *is* the B-tree keyed by id), the PK of an index-organized/clusters table elsewhere, `WITHOUT ROWID` in SQLite when a non-integer key must lead. Lookup is one B-tree descent (`SEARCH ... USING INTEGER PRIMARY KEY`); the anti-pattern is a heap table with the id in a secondary index (extra hop) or, worse, unindexed ([[What is a query plan in a relational database]]).

The verified demo is the whole argument in one plan pair: `SELECT v FROM big WHERE id = 42` with `id INTEGER PRIMARY KEY` plans as `SEARCH big USING INTEGER PRIMARY KEY (rowid=?)` — the storage itself is ordered by id, so the lookup descends one B-tree and lands on the row; the unindexed lookup on the same-sized table plans as `SCAN big2`. Scale arithmetic: a B-tree of 100M narrow keys is 3-4 levels deep — the seek is a handful of page reads regardless of N; the scan is 100M row evaluations. Design decisions that complete the answer: key type (int32 spans ±2.1 billion — enough for ids that never recycle; int64 for safety), UUID v7/ULID alternatives that are time-ordered (B-tree friendly, unlike v4's random keys), and the secondary-index tax: in rowid tables secondary indexes store rowids (compact); in clustered engines they store the PK (wider keys) ([[How does implicit type conversion hide an index]]). Partitioning composes when the table must also serve range scans ([[How does partition pruning speed up a query]]).

```sql
CREATE TABLE big (id INTEGER PRIMARY KEY, v TEXT);
CREATE TABLE big2 (v TEXT);
INSERT INTO big VALUES (42,'x');
INSERT INTO big2 VALUES ('x');

EXPLAIN QUERY PLAN SELECT v FROM big WHERE id = 42;
-- QUERY PLAN
-- `--SEARCH big USING INTEGER PRIMARY KEY (rowid=?)
EXPLAIN QUERY PLAN SELECT v FROM big2 WHERE v = 'x';
-- QUERY PLAN
-- `--SCAN big2
```

**Listing 1.** Verified on SQLite 3.53.1. The integer primary key *is* the table's ordering: one descent finds id 42 at any table size; the keyless table pays a full scan for the same answer.

```d2
direction: right
k1: "INTEGER PRIMARY KEY
table = B-tree on id" {width: 220; height: 80}
k2: "lookup id = 42
descent: 3-4 page reads" {width: 210; height: 80}
h1: "heap + secondary index
index probe -> row fetch" {width: 230; height: 80}
h2: "no key
full scan of 100M" {width: 160; height: 80}
k1 -> k2
h1 -> h2
```

**Fig. 1.** Three storage shapes, three lookup costs: the clustered integer key lands on the row directly; the heap adds a hop; the keyless table reads everything.

> [!warning] Random UUIDv4 keys shred insert locality on a 100M-row B-tree
> Inserts land on random pages, filling buffer pools with cold leaves and fragmenting the tree — the classic "UUID made inserts slow" incident. If UUIDs are mandated, use time-ordered variants (v7/ULID) or keep a monotonically assigned numeric surrogate as the leading key ([[How would you design a 100 million row table with fast lookup by int32]]).

> [!tip] Interview answer
> I make the int32 id the clustered primary key — in SQLite INTEGER PRIMARY KEY is a rowid alias so the table itself is a B-tree on the id, and the plan shows a single primary-key search instead of a scan. Three to four levels of tree mean any of the 100 million rows is a few page reads. I would note the int32 range decision, that random UUIDv4 keys damage insert locality while v7-style ordered keys do not, and that secondary indexes on clustered tables pay a wider-key tax.
