<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/Indexes #SRS

# Is a primary key implemented as an index and why

> [!abstract] Short answer
> Yes. A primary key is a constraint, and every mainstream engine enforces it with a unique index: PostgreSQL and SQLite create a unique B-tree, InnoDB makes the PK the table's clustered index, and SQL Server creates a clustered index for the PK unless one already exists. The index is what makes duplicate checks and lookups by key logarithmic instead of a table scan.

## What the constraint does under the hood

The PK declares identity: unique, non-null. Enforcement must answer two questions fast: does this key already exist (every INSERT/UPDATE), and where is the row for this key (every FK check and indexed lookup). Both are tree searches, hence the unique index. PostgreSQL's docs state that PRIMARY KEY constraints get a unique B-tree index; uniqueness itself is deferred-capable per transaction, but the index is immediate. InnoDB is the strongest version of "yes": the PK is the clustered index that stores the rows, and with no PK it synthesizes a hidden one (GEN_CLUST_INDEX) because the engine's storage model requires a key — see [[How many clustered indexes can a table have and what is a clustered index physically]]. SQL Server builds a clustered index for a new PK by default, falling back to nonclustered if a clustered index already exists.

```sql
CREATE TABLE users (
    id   BIGINT GENERATED ALWAYS AS IDENTITY,
    nick TEXT NOT NULL,
    CONSTRAINT users_pk PRIMARY KEY (id)
);
-- PostgreSQL catalog:
-- users_pkey  btree unique index on (id)
```

**Listing 1.** Declaring the constraint yields an index you can see in the catalog; nothing else enforces uniqueness on every write.

## Why it is an index and not something else

An enforcement structure must handle concurrent inserts, ranges, and arbitrary key shapes, and it must return the row location once uniqueness passes — a B-tree does all of it, which is why deduplication tricks like hash sets are reserved for specialized engines (Adaptive Hash in InnoDB is a hot-page accelerator, not the enforcement structure). The same index then serves WHERE id = ?, joins, and ORDER BY id. Costs follow: every secondary structure duplicates the PK (InnoDB), inserts into random PKs fragment the clustered layout, and UUID keys are discussed for exactly this reason in [[Should you use UUID as a primary key in PostgreSQL]]. The constraint-versus-index distinction has practical value too: UNIQUE constraints and PKs can also be declared with INCLUDE payload columns in PostgreSQL, per the covering design in [[How would you explain Covering index]].

> [!warning] "PK is just a unique index" is half-right and can fail the follow-up
> The correct layering: the PK is a logical constraint; the unique index is its implementation detail, chosen by the engine. Consequences differ per engine — InnoDB clusters storage on it and synthesizes one if absent; PostgreSQL requires it to exist and names the index; a heap-based SQL Server table can enforce PK nonclustered. Saying "so a PK and a unique index are the same thing" ignores NULL handling (PK columns are NOT NULL, single-column UNIQUE allows NULL in SQL standard engines) and clustering behavior.

> [!tip] Interview answer
> Yes: the primary key is a constraint enforced through a unique index — unique B-tree in PostgreSQL and SQLite, the clustered index itself in InnoDB, clustered-by-default in SQL Server. It is an index because enforcement must find existing keys on every write and locate rows on every lookup, and both are tree searches. The nuance is that the index is the engine's choice, and in InnoDB the PK is literally the table storage.
