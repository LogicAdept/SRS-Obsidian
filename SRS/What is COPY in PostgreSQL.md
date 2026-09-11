<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DML #SRS

# What is COPY in PostgreSQL?

> [!abstract] Short answer
> COPY is PostgreSQL's bulk load and unload command: it streams rows between a table (or a query) and a file, STDIN/STDOUT, or a program in text, CSV, or binary format. It is an order of magnitude faster than row-by-row INSERT because it parses once, fills pages directly, and writes far less WAL per row than equivalent single inserts. Client-side drivers expose it (JDBC CopyManager, psql \copy).

## The two directions

```sql
COPY measurements FROM STDIN WITH (FORMAT csv, HEADER);   -- bulk load
COPY (SELECT * FROM measurements WHERE ts < '2020-01-01')
  TO STDOUT WITH (FORMAT csv);                            -- bulk export
```

**Listing 1.** Table-side FROM/TO or a parenthesized query for export; STDIN/STDOUT keep file permissions server-side clean.

- **text**: PostgreSQL's own escaping, fastest to parse, tab-separated.
- **csv**: standard CSV with quoting rules; the exchange format for external systems.
- **binary**: native wire format, fastest, not portable across type layouts — for machine-to-machine PostgreSQL data.

```d2
src: "Stream: file / STDIN\nrows + format" {width: 300; height: 70}
parse: "One parse pass\nper-column conversion" {width: 280; height: 70}
heap: "Fill pages directly\nminimal WAL, no per-row round trips" {width: 360; height: 80}
idx: "Indexes updated at end of load" {width: 320; height: 70}
src -> parse -> heap -> idx
```

**Fig. 1.** Why COPY wins: one parse, direct page filling, no per-row client-server chatter.

## Performance playbook

- Load into a table without indexes, then create them — index maintenance is often the dominant cost ([[How do you create an index without blocking writes in PostgreSQL]] constrains that in production).
- Raise `maintenance_work_mem` for the following index builds; batch in transactions of manageable size.
- `COPY (FREEZE)` pre-freezes rows when loading into a freshly created or truncated table in one transaction — skips a later full-table vacuum pass ([[What is autovacuum in PostgreSQL]]).
- Drop and re-add foreign keys around huge loads if dependencies allow.
- psql's `\copy` runs the copy through the client (no server file access needed); server-side COPY needs superuser or pg_read_server_files.

> [!warning] COPY is all-or-nothing per transaction — and that is a feature
> A failed COPY rolls back with its transaction; there is no "load the good rows" mode. Parsing errors in row 9 million of an unbatched copy mean reloading everything. Batch files or use staging tables with validation, and remember that a single giant COPY holds one transaction — the snapshot and wraparound implications of [[Why do long-running transactions hurt PostgreSQL]] apply to it too.

> [!tip] Interview answer
> COPY is the bulk loader: streams rows in text, CSV or binary between clients or files and the table, one parse pass, direct page filling, minimal WAL — typically ten times faster than INSERTs. Tune by deferring indexes and FKs, batching, and COPY FREEZE on fresh tables. Failures roll back per transaction, so stage and batch.
