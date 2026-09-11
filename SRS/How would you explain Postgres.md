<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How would you explain Postgres?

> [!abstract] Short answer
> The leading open-source relational database: SQL-standard compliant, ACID with MVCC concurrency, process-per-connection architecture, extensible through types, operators, index methods and extensions. In one sentence: a single engine that covers OLTP, JSON documents (jsonb), full-text and vector search, and serious analytical queries — which is why whole products are built on it.

## The identity in bullets

- **Lineage**: derived from the Berkeley POSTGRES research project; PostgreSQL is the SQL-era name. Licensed under the permissive PostgreSQL License — free to use, embed and sell services around.
- **Concurrency**: MVCC — writers and readers never block each other; isolation by snapshots ([[What is MVCC in PostgreSQL]]), paid for by vacuum ([[What is autovacuum in PostgreSQL]]).
- **Durability**: WAL-first design — crash safe, replicable, the substrate of streaming and logical replication ([[What is the PostgreSQL WAL]]).
- **Extensibility**: custom types, functions, operator classes, index access methods; the extension ecosystem (PostGIS, pgvector, pg_trgm, TimescaleDB...) is its superpower ([[What are PostgreSQL extensions]]).
- **Process model**: one forked backend per connection — simple, robust isolation; the reason poolers exist ([[What is the difference between a process and a connection in PostgreSQL]]).

```d2
core: "PostgreSQL\nMVCC + WAL + planner" {width: 320; height: 80}
feats: "Native breadth\njsonb, FTS, trigram, vectors,\npartitioning, RLS, FDW" {width: 360; height: 100}
ext: "Extensions\nPostGIS, pgvector, TimescaleDB,\ncitus..." {width: 340; height: 100}
core -> feats
core -> ext
```

**Fig. 1.** The pitch: one engine, broad native surface, and extensions where the surface ends.

## Where it sits in interviews

Against MySQL: richer types and SQL features, stricter standards compliance, MVCC without storage-engine plurality ([[What is the difference between PostgreSQL and MySQL]]). Against Oracle: the open-source alternative with different tooling and operational history ([[How would you explain PostgreSQL vs Oracle]]). Against ClickHouse: the OLTP generalist versus the OLAP columnar specialist ([[What is the difference between PostgreSQL and ClickHouse]]). The honest framing: Postgres is the default OLTP choice unless a workload specifically outgrows it.

## Version notes worth having ready

As of 2026 the current major line is 18 (with 17 widely deployed): identity columns standard practice, declarative partitioning mature, logical replication the upgrade path, UUIDv7 generation native in 18, CTE inlining default since 12.

Standards compliance is high but honest: PostgreSQL implements the standard plus documented extensions (DISTINCT ON, ON CONFLICT, jsonb), and its documentation is one of the strongest assets of the project — every mechanism discussed in interviews has a definitive chapter. The upgrade story splits into minor versions (drop-in restart) and major versions requiring a real migration ([[How do you do a PostgreSQL major version upgrade]]).

In an interview, name the three subsystems before anything else — MVCC, WAL, planner — then the extensibility story. That ordering signals you know where behavior actually comes from; feature lists (jsonb, partitioning, FTS) then read as consequences rather than memorized bullets ([[What is MVCC in PostgreSQL]], [[What is the PostgreSQL WAL]]).

> [!warning] "Postgres" and "PostgreSQL" name the same product
> The shorthand Postgres is officially blessed; pronunciation debates are noise. The real naming traps are elsewhere: PostgreSQL is not "MySQL but stricter" (no storage-engine plurality, different replication models), and it is not NoSQL despite jsonb — document storage rides on relational foundations with real constraints and transactions ([[What is the difference between JSON and JSONB in PostgreSQL]]).

> [!tip] Interview answer
> PostgreSQL is the leading open-source relational engine: ACID and MVCC — no read-write blocking, snapshots for isolation — WAL-backed durability and replication, a cost-based planner, and deep extensibility through types, index methods and extensions. It covers OLTP, documents, search and vectors in one system, which is why it has become the default backend for new products.
