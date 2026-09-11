<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS

# What are IMMUTABLE, STABLE and VOLATILE functions in PostgreSQL?

> [!abstract] Short answer
> Volatility categories are promises to the optimizer about a function's behavior. VOLATILE (the default) can do anything and is re-evaluated at every row; STABLE cannot modify the database and returns the same result for the same arguments within one statement; IMMUTABLE cannot modify the database and always returns the same output for the same input, so it can be pre-evaluated with constant arguments. Category choice changes plans, index usability, and correctness.

## The three contracts

| Category | Writes allowed? | Same result within | Optimizer freedom |
|---|---|---|---|
| VOLATILE | yes | nothing promised | re-evaluate every row |
| STABLE | no | one statement | evaluate once per statement inputs |
| IMMUTABLE | no | forever | pre-evaluate constants; use in index conditions |

```d2
imp: "IMMUTABLE\nlower(x), a+b\npre-evaluated, index-safe" {width: 320; height: 90}
st: "STABLE\nnow() per statement, lookups\ncall once per statement" {width: 320; height: 90}
vol: "VOLATILE\nrandom(), writes, side effects\nnever optimized away" {width: 320; height: 90}
```

**Fig. 1.** The ladder of promises: each rung up grants the optimizer more freedom and demands more purity.

## Where it bites in practice

- **Index conditions**: an index scan evaluates its comparison value once, so a VOLATILE function cannot appear in an index-scan condition at all; STABLE and IMMUTABLE can. An expression index ([[What is an expression index in PostgreSQL]]) requires the expression be immutable.
- **Constant folding**: `WHERE created_at > now() - interval '1 day'` is stable — computed once per statement; a volatile wrapper would defeat it.
- **Correctness traps**: marking a function IMMUTABLE when it reads a table or the session timezone produces plans that cache wrong answers. `date_trunc('day', timestamptz)` is stable, not immutable, precisely because the session TimeZone affects it — the zone-dependence of timestamptz itself is in [[What is the difference between timestamp and timestamptz in PostgreSQL]].

```sql
CREATE FUNCTION total(p numeric, q numeric)
RETURNS numeric LANGUAGE sql
IMMUTABLE AS $$ SELECT p * q $$;   -- honest: pure arithmetic
```

**Listing 1.** A correct IMMUTABLE declaration; the documentation's rule: label with the strictest category that is actually true.

## The default is the trap

Unannotated PL/pgSQL functions are VOLATILE, so planners re-call them per row and refuse index use. Read-only helper functions that could be STABLE or IMMUTABLE silently degrade every query that uses them in filters or joins.

> [!warning] Lying about IMMUTABLE is a correctness bug, not a tuning miss
> An IMMUTABLE function that reads a table, touches now(), or depends on locale/session settings lets the planner fold it into constants — including during index builds — and the cached value may be wrong forever. Performance tricks that misdeclare volatility produce data-dependent heisenbugs that only appear after plans are cached or indexes are built.

> [!tip] Interview answer
> Three volatility promises: VOLATILE does anything and re-runs per row; STABLE is read-only with one answer per statement; IMMUTABLE is read-only with an answer fixed forever, enabling constant folding and index conditions. Default is VOLATILE, so unannotated helpers quietly kill plans — and falsely claiming IMMUTABLE is a correctness landmine, since the optimizer will cache its results.
