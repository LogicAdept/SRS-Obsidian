<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/Relational/Oracle #SRS

# How would you explain PostgreSQL vs Oracle?

> [!abstract] Short answer
> Both are mature MVCC relational engines; the divide is licensing and ecosystem versus openness and extension model. Oracle ships an integrated commercial stack (RAC multi-instance clustering, Multitenant container databases, PL/SQL tooling, AWR diagnostics) with enterprise contracts; PostgreSQL ships an open-source permissively-licensed engine where clustering, sharding and diagnostics come from the extension and tools ecosystem. Syntactically they differ in identity, pagination and procedural languages.

## The factual comparison

| Dimension | PostgreSQL | Oracle |
|---|---|---|
| License | PostgreSQL License (permissive, free) | commercial, per-core/user contracts |
| Autoincrement | IDENTITY / sequences | SEQUENCE + triggers / identity (12c+) |
| First N rows | LIMIT / FETCH FIRST | FETCH FIRST (12c+), ROWNUM |
| Procedural SQL | PL/pgSQL, plus Python/Perl/etc | PL/SQL (deep tooling), Java in-DB |
| Clustering | extension/tooling based | Oracle RAC (multi-instance shared data) |
| Multitenancy | schemas, databases, FDW | Multitenant CDB/PDB architecture |
| Diagnostics | pg_stat_* views, extensions | AWR/ASH reporting packs |
| Concurrency | MVCC via versions in the heap | MVCC via undo segments |

Both engines are genuinely MVCC — the implementation differs: PostgreSQL leaves old versions in the table for vacuum, Oracle keeps undo in separate segments for read consistency ([[What is MVCC in PostgreSQL]] vs the undo-based model described in Oracle's own concepts documentation).

```d2
pg: "PostgreSQL\nopen core + extensions\npermissive license" {width: 300; height: 80}
ora: "Oracle\nintegrated commercial stack\nRAC, Multitenant, AWR" {width: 300; height: 80}
pick: "Choice drivers: contracts, existing skills,\nHA requirements, ecosystem lock-in" {width: 420; height: 90}
pg -> pick
ora -> pick
```

**Fig. 1.** The decision is rarely a single feature; it is contracts, operations and skills.

## Migration realities (both directions)

Syntax ports are the easy part: sequences and identity, pagination, NVL to COALESCE, CONNECT BY to recursive CTEs ([[How do you implement a recursive query in PostgreSQL]]), DECODE to CASE. The hard parts: PL/SQL packages (business logic volume), proprietary hints and optimizer expectations, AWR-equivalent monitoring rebuilds, and HA topology changes. The same methodology applies to the MySQL direction ([[How would you migrate an application from MySQL to PostgreSQL]]).

> [!warning] "PostgreSQL is a free Oracle" sets up the wrong expectations
> The gaps are operational, not just syntactic: no RAC-equivalent in core (active-active multi-instance on shared storage is an Oracle-defining feature), no AWR-style built-in history without extensions and processes, PL/pgSQL is not PL/SQL in tooling or ecosystem. Conversely Oracle teams underestimate PostgreSQL's extension-based HA and the operational simplicity of its single storage engine ([[What is the difference between PostgreSQL and MySQL]] — engine plurality is a different comparison).

> [!tip] Interview answer
> Both are serious MVCC RDBMSes; Oracle is a commercial integrated stack — RAC clustering, Multitenant, PL/SQL tooling, AWR diagnostics — while PostgreSQL is permissively licensed with its capability coming from an extension ecosystem: different clustering, monitoring and procedural-language stories. MVCC is implemented differently (versions versus undo), syntax ports are mechanical, and the real costs are tooling, operations and skills.
