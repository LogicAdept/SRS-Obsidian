<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What are Foreign Data Wrappers in PostgreSQL?

> [!abstract] Short answer
> The SQL/MED layer: FDWs let PostgreSQL treat external data sources — other PostgreSQL servers, other databases, CSV files, APIs — as local tables. You declare a foreign data wrapper, a server, a user mapping and foreign tables, then query them with ordinary SQL; postgres_fdw (the built-in one for cross-PostgreSQL access) pushes predicates and even joins to the remote server when it can.

## The object ladder

```sql
CREATE EXTENSION postgres_fdw;
CREATE SERVER remote_app FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host 'db2.internal', dbname 'app');
CREATE USER MAPPING FOR app_user SERVER remote_app
  OPTIONS (user 'reader', password '...');
IMPORT FOREIGN SCHEMA public LIMIT TO (orders)
  FROM SERVER remote_app INTO reporting;

SELECT * FROM reporting.orders WHERE created_at > now() - interval '1 day';
```

**Listing 1.** Wrapper, server, user mapping, foreign tables — then plain SQL. IMPORT FOREIGN SCHEMA mirrors remote DDL automatically.

```d2
lq: "Local query\nFROM foreign table" {width: 300; height: 70}
fdw: "postgres_fdw\nplan, push down, fetch" {width: 280; height: 80}
rem: "Remote PostgreSQL\nexecutes narrowed scan" {width: 300; height: 70}
lq -> fdw -> rem
```

**Fig. 1.** The wrapper translates between the local planner and the remote engine, pushing work down where the operator support allows.

## What postgres_fdw pushes down

WHERE clauses on supported operators, and — for newer remote versions — joins and aggregates; otherwise rows are fetched and processed locally, which is the performance cliff to watch. Cost estimates of remote scans are approximations tunable per server/table; ANALYZE on foreign tables samples remotely or locally per options. Authentication lives in user mappings (or the library's own password file).

## The wider family

- file_fdw: read server-side files and program output as tables (log analysis in SQL).
- dblink: the older sibling — raw SQL calls to remote databases returning result sets (function call semantics rather than tables).
- Third-party wrappers for MySQL, Oracle, MongoDB, S3, HTTP APIs — the FDW interface is a public extension point ([[What are PostgreSQL extensions]]).
- The standard cross-engine bridge in multi-database estates ([[What is the difference between PostgreSQL and ClickHouse]] — foreign tables into analytical stores are a common integration), and one bridge between tenant databases in [[How do you implement multi-tenancy in PostgreSQL]].

> [!warning] A foreign table is not a replica
> Reads are live remote queries with network latency and remote failure modes; writes depend on the wrapper (postgres_fdw supports them, transactionally within limits); there is no local caching by default. Treating FDW as "sync" or "copy" produces mysterious production latency — it is federation, not replication ([[What is the difference between streaming and logical replication in PostgreSQL]] is the replication answer).

> [!tip] Interview answer
> FDW is SQL/MED federation: declare a wrapper, server and user mapping, and external sources appear as local tables. postgres_fdw is the built-in PostgreSQL-to-PostgreSQL one, pushing filters, joins and aggregates to the remote side when possible; file_fdw reads files, and the ecosystem covers other engines and APIs. Powerful for cross-system queries — but it is live federation with network costs, not replication.
