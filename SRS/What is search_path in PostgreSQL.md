<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is search_path in PostgreSQL?

> [!abstract] Short answer
> search_path is the per-session schema lookup order PostgreSQL uses to resolve unqualified names: the first schema containing the object wins. Default is "$user", public (plus implicitly pg_catalog first). It decides which schema your unqualified tables, functions and operators resolve to — which makes it both the multi-tenancy switch and a security-sensitive setting.

## How resolution works

For an unqualified name, PostgreSQL scans the path schemas in order: pg_catalog is always effectively first (unless explicitly placed later), then "$user" (a schema named like the current user if it exists), then public. CREATE without qualification goes into the first writable schema of the path (the "creation schema"). Schemas themselves are namespaces inside one database ([[How do you implement multi-tenancy in PostgreSQL]] uses this directly).

```sql
SHOW search_path;                 -- "$user", public
SET search_path = tenant_42, public;
SELECT * FROM orders;             -- tenant_42.orders if present
CREATE TABLE notes (t text);      -- lands in tenant_42
```

**Listing 1.** The tenant-switch idiom: one connection pool, path set per session or per transaction (SET LOCAL inside a transaction).

```d2
name: "orders (unqualified)" {width: 260; height: 60}
c: "pg_catalog (always first)" {width: 300; height: 60}
u: "$user schema" {width: 220; height: 60}
p: "public" {width: 180; height: 60}
hit: "First hit wins" {width: 220; height: 60}
name -> c -> u -> p -> hit
```

**Fig. 1.** The lookup is strictly ordered; a name shadowed in an earlier schema silently wins.

## Why it is security-relevant

The path is per-role configurable: `ALTER ROLE reporting SET search_path = reporting, public;` pins the default for a service account instead of relying on every client to SET it correctly. Dumps emit SET search_path at the top for the same reason — keep that line intact when editing dump files.

An attacker (or a careless deploy) can create a like-named object in a schema earlier in the path and hijack unqualified calls — function-resolution hijacking is a documented attack class. Defensive settings: remove public world-writability, qualify names in security-relevant code, and set path per role. Functions run with the invoking user's path unless the code is qualified.

> [!warning] Prepared plans and pooling interact with SET search_path
> With transaction pooling ([[Why use pgBouncer with PostgreSQL]]) a SET search_path may stick to a server connection used by another tenant, or vanish before the next statement — SET LOCAL inside the transaction is the safe form. And in PostgreSQL 15+ the public schema is not writable by everyone by default, closing the classic squatting hole ([[What is row-level security in PostgreSQL]] is the row-level sibling of schema-level isolation).

> [!tip] Interview answer
> search_path is the ordered schema list for resolving unqualified names — pg_catalog, then "$user", then public by default. First match wins for reads, first writable schema gets CREATE. It powers schema-per-tenant designs via SET LOCAL, but it is also a security surface: unqualified names in trusted code and an open public schema are how name-hijacking happens.
