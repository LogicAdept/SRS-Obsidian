<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What are PostgreSQL extensions?

> [!abstract] Short answer
> Packaged add-on modules — SQL objects plus compiled C libraries with metadata — installed into a database with a single CREATE EXTENSION. They are the mechanism behind PostGIS, pgvector, pg_trgm, pg_stat_statements and dozens more: the server's type system, index methods and functions are designed to be extended, and extensions are the supported way to ship such extensions.

## What an extension is

An extension bundles a control file (name, version, relocatability), an SQL script (creates the objects: types, functions, operators, operator classes), and shared libraries. `CREATE EXTENSION vector;` runs the script and records the membership of every created object in pg_extension/pg_depend — so `DROP EXTENSION` removes them all cleanly, and upgrades go through ALTER EXTENSION UPDATE.

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;      -- contrib: ships with PostgreSQL
CREATE EXTENSION vector;                     -- third-party: PostGIS-style install
SELECT * FROM pg_available_extensions;       -- what this installation offers
```

**Listing 1.** Discovery and installation; contrib modules ship inside the PostgreSQL distribution itself ([[What is pg_trgm]], [[What is pg_stat_statements]], [[What is pgvector in PostgreSQL]]).

```d2
srv: "Server extension points\ntypes, functions, operators,\nindex access methods" {width: 340; height: 100}
ext: "Extension package\ncontrol file + SQL + .so" {width: 300; height: 90}
db: "CREATE EXTENSION\nobjects tracked in catalogs" {width: 320; height: 90}
ext -> db
srv -> db: "plugs into"
```

**Fig. 1.** Extensions are first-class: catalog-tracked, versioned, cleanly removable.

## Why the model matters

- The core stays small and stable; niche functionality lives in extensions (geospatial, vectors, crypto, foreign data wrappers [[What are Foreign Data Wrappers in PostgreSQL]]).
- Version pinning per database: `ALTER EXTENSION ... UPDATE TO 'x.y'` gives controlled upgrades.
- Trusted extensions (since PostgreSQL 13) can be installed by non-superusers with CREATE privilege — relevant for managed platforms.
- Operational cost: extension binaries must match server upgrades ([[How do you do a PostgreSQL major version upgrade]] — extensions often lag major releases and need their own upgrade steps); managed providers curate the allowed list.

## The names to know

PostGIS (geospatial), pgvector (embeddings), pg_trgm (fuzzy text), pg_stat_statements (workload stats), postgres_fdw (federated queries), TimescaleDB/Citus (time-series and sharding), pgcrypto, pg_repack ([[What is pg_repack]] — an extension itself).

> [!warning] CREATE EXTENSION is not "install a library"
> The compiled library must already exist on the server host and match the server version; on managed clouds you get the provider's catalog, not the internet's. The second trap: extension objects look like ordinary objects but belong to the extension — renaming or dropping them individually breaks the catalog bookkeeping; ALTER/DROP EXTENSION is the supported path.

> [!tip] Interview answer
> Extensions are the packaged extension mechanism of PostgreSQL: a control file, an SQL script and a shared library, installed with CREATE EXTENSION and tracked in the catalogs so upgrades and drops are clean. They add types, functions and whole index methods — PostGIS, pgvector, pg_trgm — and their binaries must match server upgrades, which matters in every major-version migration.
