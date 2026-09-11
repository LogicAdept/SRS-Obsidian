<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What is row-level security in PostgreSQL?

> [!abstract] Short answer
> Row-level security (RLS) attaches per-row policies to a table: every query from a non-bypassing role filters visible rows (USING) and constrains writable rows (WITH CHECK) inside the engine, regardless of how the query was written. It is the mechanism behind multi-tenant data isolation in one schema — with the documented caveats that owners bypass it by default and superusers and BYPASSRLS roles always bypass it.

## Enabling and writing policies

```sql
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY doc_isolation ON documents
  USING (company_id = (SELECT company_id FROM users WHERE name = current_user))
  WITH CHECK (company_id = (SELECT company_id FROM users WHERE name = current_user));
```

**Listing 1.** USING filters which rows a SELECT/UPDATE/DELETE can see or touch; WITH CHECK validates INSERT and the new versions of UPDATEd rows. Omitting WITH CHECK copies USING into it — often what you want.

- Policies are per command (ALL, SELECT, INSERT, UPDATE, DELETE) and per role; PERMISSIVE policies OR together, RESTRICTIVE ones AND into the mix.
- No policy applies for a command type means default-deny for that command on that table.
- Expressions run with the querying user's privileges — wrap privileged lookups in SECURITY DEFINER functions when needed.

```d2
q: "Any query on the table" {width: 260; height: 60}
pol: "Policies evaluated\nper row, before user predicates" {width: 320; height: 80}
vis: "USING: row visible?" {width: 240; height: 60}
wri: "WITH CHECK: row writable?" {width: 280; height: 60}
q -> pol -> vis
q -> pol -> wri
```

**Fig. 1.** Policies sit between the query and the heap: even SELECT * obeys them.

## What it costs

- Performance: policy expressions add per-row evaluation; wrap them as parameterized STABLE functions and keep them index-friendly, or plans degrade ([[Why might PostgreSQL choose a sequential scan instead of an index]]).
- Leaks through side channels: leakproof-function optimization aside, error messages, sequence gaps and timing can hint at hidden rows — RLS is not a security boundary against the DBA.
- Owner semantics: by default the table owner skips RLS entirely; FORCE ROW LEVEL SECURITY makes even the owner obey (superusers and BYPASSRLS never obey).

In the multi-tenancy context RLS is the enforcement layer of the shared-schema model ([[How do you implement multi-tenancy in PostgreSQL]]); schema-level separation alternatives live in [[What is search_path in PostgreSQL]].

> [!warning] RLS is not invisible and not free
> Every policy check appears in plan timing, and a policy calling a volatile or unindexable function can multiply query cost. The security-facing trap: developers test as the table owner, see everything work, ship — and the owner bypass means none of the policies ever fired in their tests. Test with a real application role, always.

> [!tip] Interview answer
> RLS puts per-row policies inside the engine: USING filters visibility, WITH CHECK guards writes, per command and per role, with default-deny when no policy matches. It is how one shared schema serves many tenants safely — provided you FORCE it for owners, test as a non-owner role, and keep policy expressions index-friendly because they run for every row.
