<!--
reps: 0
priority: 0
-->
#Databases/Relational/MySQL #Databases/Relational/PostgreSQL #DevOps/Deployment #SRS

# How would you migrate an application from MySQL to PostgreSQL?

> [!abstract] Short answer
> In layers: map the schema and types (AUTO_INCREMENT to identity, unsigned and TINYINT variants, datetime to timestamp/timestamptz, utf8mb4 to UTF8), translate SQL dialect (backticks to double quotes, ON DUPLICATE KEY to ON CONFLICT, ILIKE semantics, strict GROUP BY), port the procedural logic, then move data with a dual-write or logical-replication cutover and verify with parallel runs. The schema is the easy third; behavior and tooling are where migrations fail.

## The mapping checklist

| MySQL | PostgreSQL |
|---|---|
| AUTO_INCREMENT | GENERATED ALWAYS AS IDENTITY |
| TINYINT(1) | boolean (or smallint) |
| unsigned int/bigint | no unsigned: widen (bigint) or constrain |
| DATETIME | timestamp; add timestamptz for instants |
| TEXT/BLOB families | text / bytea |
| backticks `col` | double quotes "col" (usually drop quoting) |
| INSERT ... ON DUPLICATE KEY UPDATE | INSERT ... ON CONFLICT DO UPDATE |
| GROUP_CONCAT | string_agg |
| IFNULL / NOW() | COALESCE / now() |
| FIND_IN_SET | = ANY(array) — better: normalize |

**Listing 1.** The frequent offenders; the identity and timestamp rows are the ones with silent behavior differences ([[What is the difference between SERIAL and IDENTITY in PostgreSQL]], [[What is the difference between timestamp and timestamptz in PostgreSQL]]).

## The semantic traps

- **String comparison**: MySQL collations are usually case-insensitive; PostgreSQL comparisons and unique indexes are case-sensitive by default — decide per column: citext, lower() expression indexes ([[What is an expression index in PostgreSQL]]).
- **GROUP BY strictness**: PostgreSQL rejects non-aggregated columns that MySQL tolerated.
- **Types discipline**: implicit conversions that used an index in MySQL can defeat one in PostgreSQL ([[How does implicit type conversion hide an index]]); empty string versus NULL distinctions differ in behavior.
- **Case of identifiers**: unquoted identifiers fold to lowercase in PostgreSQL.
- **Upsert and pagination dialects**: [[How does UPSERT work in PostgreSQL]]; LIMIT/OFFSET works in both, but keyset patterns port cleanly ([[How would you explain Pagination offset limit vs cursor-based]]).

## The cutover mechanics

1. Freeze schema; migrate DDL; load a snapshot (dump from MySQL, transform, COPY in — [[What is COPY in PostgreSQL]]).
2. Dual-write or replicate changes (CDC tooling, or logical bridges) until parity.
3. Run read verification in parallel (counts, checksums, sampled queries).
4. Switch reads, then writes, with a rollback path; watch plans — the new engine needs fresh statistics and index review ([[How do stale statistics hurt a query plan]], [[How do you decide which database indexes to create]]).
5. Rebuild operational tooling: backups, monitoring, failover ([[How do you take a PostgreSQL backup]], [[How would you explain PostgreSQL replication strategies]]).

> [!warning] Migration tools move data; they do not decide semantics
> Automated converters port syntax; case-sensitivity, NULL semantics, implicit casts, identity behavior and collations are decisions someone must make explicitly per feature. The classic post-migration bug set: duplicated emails that a case-insensitive unique index used to catch, and 32-bit unsigned values that no longer fit. Decide both before the first data load.

> [!tip] Interview answer
> Four phases: map the schema — identity columns, unsigned widening, timestamp semantics, utf8mb4 to UTF8; translate the dialect — quoting, ON CONFLICT, strict GROUP BY, case-sensitive comparisons with citext or expression indexes; port procedural code and verify behavior with parallel runs; then cutover via dual-write or CDC with statistics and index review on the new engine. The data is the easy part; semantics and ops tooling are the project.
