<!--
reps: 0
priority: 0
-->
#ProgrammingLanguages/CSharp #Persistence/ORM #SRS

# What is LINQ lazy execution and what are Entity Framework limitations?

> [!abstract] Short answer
> **LINQ lazy execution (deferred execution)**: a LINQ query builds a **pipeline or expression tree** and executes **nothing** until something **enumerates** it — `foreach`, `ToList()`, `First()`, `Count()`. Two layers matter: over **`IEnumerable`** the pipeline is a chain of delegates executed lazily in memory; over **`IQueryable`** (the ORM case) it is an **expression tree** translated to SQL **at enumeration time**, so composing filters before materialization changes the query, and re-enumerating **re-executes** it against the database. The limits that bite in practice: translation happens **at runtime**, so unsupported constructs fail on execution, not compilation; **partial client-side evaluation** tempts you to mix C# logic into queries until a provider version draws the line at the top level only; **lazy loading is opt-in** (navigations via proxies), so the N+1 pattern is easy to write and must be profiled; and there is **no built-in second-level cache** — every query is a database round trip unless you add one.

## Deferred execution: the two pipelines

Over `IEnumerable`, operators like `Where`/`Select` return a lazy wrapper; the source streams through the chain only while enumerating. Over `IQueryable`, the operators record **what you wrote** as an expression tree; the provider walks the tree when enumeration starts and produces SQL with your parameters bound then. Consequences that interview answers are built from:

- **Composition order is free until materialization** — add `Where` to an `IQueryable` and the SQL gains a predicate; the same trick after `ToList()` filters in memory.
- **Deferred is not cached** — enumerating the same variable twice issues the query twice; `foreach` over a "query" in a loop is the local N+1.
- **Capture semantics apply** — the tree references variables, not values, so the value at enumeration time is the one used.
- **`IQueryable` vs `IEnumerable` is a contract switch** — `AsEnumerable()` below a point deliberately moves the rest of the composition to memory ([[When does the N plus 1 query problem occur and how do you fix it]] shows the round-trip math this trade-off controls).

```csharp
// deferred, translated: SELECT ... WHERE Price > 100 — DB does the work
var cheap = ctx.Products.Where(p => p.Price > 100);
// enumerated now; re-enumerating later re-executes the SQL
var list = cheap.ToList();
// local lambda cannot translate — runtime failure at enumeration time
var bad  = ctx.Products.Where(p => IsPromo(p.Name)).ToList();
```

**Listing 1.** The boundary between server and client evaluation is discovered at execution, which is the core maintenance risk of query-as-tree.

## The limitations, ranked by how often they bite

**Runtime translation failures.** A query compiles as C# and fails when the provider cannot map a construct (custom methods, unsupported functions) — the strongest argument for integration tests around every non-trivial query shape. **Client evaluation boundary**: earlier stacks happily mixed translatable and in-memory parts anywhere in the query, producing unpredictable SQL; the later discipline evaluates client code **only in the final projection**, and everything inside `Where`/`OrderBy`/joins must translate — a restriction that moved a whole class of silent inefficiencies into loud failures. **Lazy loading is opt-in** (virtual navigations with a proxy stack, or explicit loading), so by default navigations are **null until loaded** — the accidental-N+1 of the eager-by-default world is replaced by the accidental-`NullReferenceException` of the lazy-by-default one ([[What are the drawbacks of lazy loading]] generalizes the trade-off). **No second-level cache**: identity is managed per-context by the change tracker, and repeated queries hit the database; caching is an added layer with its own staleness rules ([[What are Hibernate first and second level cache tiers]] shows the full-tier model another stack chose). **Bulk writes** historically loaded entities to change them; set-based update/delete operators arrived late, so older codebases pay entity materialization for mass changes ([[What is Hibernate performance tuning]] contrasts write-behind and batching approaches).

## The change tracker is the model to reason about

The unit of work is the **context**: it tracks loaded entities, computes diffs on `SaveChanges`, and writes in one transaction. That gives the same first-level identity guarantees as any ORM ([[What is object relational mapping ORM]] frames the shared mechanics) with the same costs: contexts are **not thread-safe**, should live **per work unit**, and holding them long means holding snapshots and letting dirty checking grow. Detached-entity graphs (loaded in one context, edited, reattached in another) have the same merge complexity as elsewhere.

> [!warning] Deferred execution delays the failure too
> A query with an untranslatable expression, a typo in a navigation, or a connection problem does not fail where it is built — it fails where it is enumerated, possibly far away, possibly inside a loop where it also becomes N+1. Materialize deliberately (`ToList`, `First`, `Any`) as close to the composition as the design allows, and treat "passed the query around and it threw later" as the default failure mode, not a mystery.

> [!tip] Interview answer
> LINQ defers execution: `IQueryable` builds an expression tree that the ORM translates to SQL when enumerated, so composition before materialization shapes the query, and every enumeration re-executes it. The limitations I design around: translation failures surface at runtime, so hot query shapes need integration tests; client-side evaluation is restricted to the final projection; lazy loading is opt-in so N+1 needs profiling rather than assumption; there is no second-level cache; and bulk updates historically materialized entities. The change tracker gives per-context identity and write-behind in one transaction — the same ORM model as Java stacks, different defaults.

See [[What is object relational mapping ORM]], [[When does the N plus 1 query problem occur and how do you fix it]], [[What are the drawbacks of lazy loading]], and [[What are Hibernate first and second level cache tiers]].
