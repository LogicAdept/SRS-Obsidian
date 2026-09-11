<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# How do you implement multi-tenancy in PostgreSQL?

> [!abstract] Short answer
> Three standard models, one database engine: shared schema with a tenant_id column plus row-level security enforcing isolation; schema-per-tenant with search_path switching; database-per-tenant for hard isolation. Tradeoffs run along isolation strength versus operational scale: one table to ALTER and VACUUM versus thousands of schemas or databases, shared cache and connections versus per-tenant resources.

## The models

| Model | Isolation | Ops cost | Scales to |
|---|---|---|---|
| shared schema + RLS | row-level, enforced in engine | lowest | many small tenants |
| schema-per-tenant | namespace-level | medium (DDL fan-out) | hundreds per database |
| database-per-tenant | physical per DB | highest (conn pooling, per-DB maintenance) | strong isolation needs |

```sql
-- shared schema + RLS: the engine enforces the tenant boundary
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::int);
```

**Listing 1.** The application sets `app.tenant_id` per connection or transaction; the policy filters every read and write regardless of query shape — including bugs that forgot a WHERE clause ([[What is row-level security in PostgreSQL]]).

```d2
one: "One schema\ntenant_id column + RLS" {width: 300; height: 80}
schem: "Schema per tenant\nsearch_path switch" {width: 300; height: 80}
db: "Database per tenant\nown files, own pool" {width: 300; height: 80}
iso: "isolation grows ->" {width: 220; height: 60}
ops: "ops cost grows ->" {width: 220; height: 60}
one -> schem -> db
```

**Fig. 1.** The spectrum: shared schema is cheapest to operate, database-per-tenant hardest to escape from.

## The mechanics of each

- **Shared schema + RLS**: one set of migrations; indexes stay leading with tenant_id for pruning ([[How do you decide which database indexes to create]]); RLS costs a policy check per row-level access — non-bypassing roles only ([[What is row-level security in PostgreSQL]]); beware poolers with session-level SET ([[Why use pgBouncer with PostgreSQL]] — use SET LOCAL).
- **Schema-per-tenant**: DDL must fan out to every schema ([[What is search_path in PostgreSQL]] for the switching mechanism); per-tenant backup/restore becomes natural; catalog pressure grows with schema count.
- **Database-per-tenant**: connection pools multiply ([[What is the difference between a process and a connection in PostgreSQL]] — every database has its own backends); cross-tenant queries and analytics need aggregation tooling ([[What are Foreign Data Wrappers in PostgreSQL]] is one bridge).

> [!warning] RLS without FORCE protects only non-owners
> Table owners and superusers bypass row security by default; an application role that owns its tables sails through every policy unless ALTER TABLE ... FORCE ROW LEVEL SECURITY is set. The second classic leak: policies that filter reads (USING) but forget the write check (WITH CHECK) — inserts can land in another tenant's rows.

> [!tip] Interview answer
> Three models: shared schema with tenant_id plus row-level security as the engine-enforced default; schema-per-tenant switched via search_path; database-per-tenant for hard isolation. I default to shared schema plus RLS for operational sanity, mind pooler interactions with SET, and force RLS for owners — then escalate isolation per tenant only when the business demands it.
