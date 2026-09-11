<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> Spring Data JPA's `@Query` accepts two dialects: **JPQL** (default) — a database-independent object-query language over *entities and their fields*, translated by Hibernate into SQL at startup; and **native SQL** (`nativeQuery = true`) — literal SQL sent to the database as written. JPQL buys portability, entity-graph awareness and rename safety; native buys engine features (window functions, hints, CTEs, dialect-specific types) at the price of portability and mapping control ([[What is the difference between Nested Loop Hash Join and Merge Join]]).

The verified listing shows the *shape* both must ultimately produce — per-customer aggregates via a LEFT JOIN (chosen so customers without orders still appear with 0) — which is exactly the SQL Hibernate generates from the JPQL equivalent `SELECT c.id, COUNT(o.id), COALESCE(SUM(o.amount), 0) FROM Customer c LEFT JOIN c.orders o GROUP BY c.id`. The Spring Data JPA reference documents the two forms and their mechanics: JPQL queries are validated against entity metadata and parsed at bootstrap (typos fail at startup — a real safety property), while native queries pass through untouched (with the `nativeQuery = true` attribute), supporting `COUNT`-projections, named parameters (`:param`), and pagination via `Pageable` for both. The decision rules that survive interviews: default to JPQL/derived queries — they refactor with entity renames and stay engine-portable; go native for what JPQL cannot express — window functions (Hibernate 6 adds some), recursive CTEs, engine-specific functions, index-hint-driven plans, or when the generated SQL is demonstrably worse ([[What is the N plus 1 problem in SQL]]). The mapping nuance: native queries return Object[] tuples unless mapped via an interface projection or `@SqlResultSetMapping` — JPQL returns entity types naturally.

```sql
SELECT c.name, COUNT(o.id) AS order_cnt, COALESCE(SUM(o.amount), 0) AS total
FROM customers c LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id ORDER BY c.id;
-- Alice|2|200
-- Boris|1|45.5
-- Carla|3|370.5
-- Dmitri|1|25
-- Elena|2|300
-- Fedor|0|0
-- (the shape both dialects target; JPQL writes Customer/c.orders entities,
--  native SQL writes this statement verbatim with nativeQuery = true)
```

**Listing 1.** Verified on SQLite 3.53.1. The LEFT JOIN keeps zero-order customers (Fedor|0|0) — the semantic detail JPQL's `LEFT JOIN c.orders` preserves identically; the native form is this exact text.

```d2
direction: right
j: "JPQL
entities + fields
validated at startup" {width: 200; height: 90}
n: "native SQL
verbatim, engine features" {width: 200; height: 90}
h: "Hibernate translates
JPQL -> SQL" {width: 190; height: 80}
d: "database" {width: 120; height: 60}
j -> h -> d
n -> d
```

**Fig. 1.** Two dialects, two paths: JPQL is translated (and checked) by the ORM on the way to SQL; native SQL arrives as written — trading safety checks for full engine access.

> [!warning] Native queries bypass the entity mapping — including its safety nets
> Column renames break native strings silently (no startup validation), result shapes are positional tuples without projections, and dialect switching (test H2, production PostgreSQL) can break engine syntax that JPQL would have translated. Contain native SQL in repository methods with projections and integration tests on the real engine ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> @Query has two dialects: JPQL by default — an entity-field language Hibernate translates to SQL and validates at startup, so renames and portability are safe — and nativeQuery = true, which sends SQL verbatim for what JPQL cannot express: window functions, recursive CTEs, engine hints. My example is per-customer aggregates where the LEFT JOIN keeps zero-order customers in both dialects. My rules: JPQL first for portability and refactor safety, native for engine power with projections and tests on the production engine, because native strings bypass the mapping's safety nets.
