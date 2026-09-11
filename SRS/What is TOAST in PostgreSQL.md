<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is TOAST in PostgreSQL?

> [!abstract] Short answer
> TOAST (The Oversized-Attribute Storage Technique) is how PostgreSQL stores values that do not fit in an 8 kB page: large values are compressed and/or moved out of line into a per-table TOAST table, leaving only a small pointer in the main tuple. It is automatic and transparent, with a 1 GB hard limit per field value.

## Why it exists

The heap cannot span pages: a tuple must fit in one 8 kB page. A wide `text`, `jsonb`, or bytea column would be impossible without out-of-line storage. TOAST handles it transparently: only variable-length (varlena) types are TOAST-able, and the varlena header encodes whether the value is inline, compressed, or a pointer.

```d2
row: "Main heap tuple\npointer to TOAST entry" {width: 280; height: 80}
toast: "pg_toast.pg_toast_<oid>\nchunks of ~2 kB,\nindexed for random reads" {width: 400; height: 90}
row -> toast: "value > ~2 kB after compression check"
```

**Fig. 1.** The TOAST table lives in a separate relation and stores the big value in chunks; the main tuple keeps a compact pointer.

## The decision ladder

For each oversized value the engine tries, in order: keep it in line if it fits; compress in line (pglz by default, or lz4 via `COMPRESSION` column option); move it out of line to the TOAST table; finally compress out-of-line. Thresholds are per-type strategy constants, roughly around 2 kB for a typical 8 kB page. Either way, reading the column later requires reassembly — a "detoast".

## Operational consequences

- `SELECT *` on wide rows pays detoast cost even when you need one narrow column; project explicitly.
- Updating any part of a wide value rewrites its TOAST representation; wide `jsonb` blobs behave poorly under frequent small updates.
- Compression is configurable per column since PostgreSQL 14: `ALTER TABLE t ALTER COLUMN c SET COMPRESSION lz4;` — lz4 decompresses much faster than pglz.
- The 1 GB per-value ceiling is a hard limit; even in-line compressed values cannot exceed it ([[What is the difference between CHAR VARCHAR and TEXT in PostgreSQL]]).
- You can measure before restructuring: `pg_column_size(value)` versus `octet_length(value)` shows the stored size including compression, and the pg_toast relation's size in pg_total_relation_size tells you how much of the table is really TOAST.
- Slices matter: selecting a substring of a TOASTed value still detoasts the whole chunk set on the server unless the type supports slicing — another reason wide blobs belong in object storage, not in hot relational tables.
- The TOAST table inherits nothing from your indexes: only its own primary key on chunk id serves reads, so "the index made it fast" reasoning does not cross the TOAST boundary. Wide-column access patterns deserve their own review during schema design ([[What is the difference between CHAR VARCHAR and TEXT in PostgreSQL]] for which types are TOAST-able in the first place).

## Reading it from the catalog

Per-column storage strategies are visible in `pg_attribute.attstorage`, and the relations involved are the main table plus its `pg_toast.pg_toast_<oid>` companion — both count toward `pg_total_relation_size`. `pg_column_size()` on a value shows what it actually costs stored (compression included), which is the honest number when debating whether a column belongs in the database at all.

The threshold behavior also explains a common production observation: a table with wide jsonb columns can have a main relation of a few gigabytes and a TOAST relation several times larger. Sums over pg_total_relation_size include the TOAST table — reporting "table size" from pg_relation_size alone quietly misses most of the storage, and any cleanup decision based on that number starts from the wrong baseline.

> [!warning] TOAST tables are invisible in most plans
> EXPLAIN shows one scan of the main table; the TOAST lookups happen underneath. A query "reading one row" can issue dozens of extra index scans into the TOAST table. When a wide-column query is mysteriously slow, check `pg_stat_user_tables` for the `pg_toast` relation's I/O — [[How do you debug a slow PostgreSQL query]].

> [!tip] Interview answer
> TOAST is the out-of-line storage mechanism for values too big for an 8 kB page: big text, jsonb or bytea values are compressed and chunked into a hidden per-table TOAST relation, with a pointer in the main tuple. It is automatic, capped at 1 GB per value, and its cost — detoasting on read, rewriting on update — is why wide columns need deliberate schema design.
