<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Queries #Java/Persistence/JPA #SRS

# What is the Hibernate query plan cache?

> [!abstract] Short answer
> Every HQL/JPQL/Criteria query must be **parsed, semantically analyzed and compiled into an executable plan** before SQL is produced. Hibernate caches those plans — the **query plan cache** — keyed by the **query text / shape**, so repeating the same query skips compilation. The cache is bounded (**`hibernate.query.plan_cache_max_size`**, default **2048**, with strong/soft reference tiers). The senior problem is **cache churn** from shape variance, and the measured sources are: **literal-inlined values** (a string-built query with the ids inlined compiles a plan **per value set**) and **Criteria trees assembled per request** (a plan **per predicate combination**). A **bound named parameter is safe** — `where id in (:ids)` with a different list size each call reuses **one plan**, because list expansion happens at execution, not at compile time. `Statistics` exposes **plan cache hit/miss counters** — measure the ratio before tuning anything.

## Compile once, execute many

Compilation is real work: parse the query tree, resolve entity/field names against the metamodel, decide the SQL shape for the dialect, build the result-row reader. The plan cache makes that a **one-time cost per query shape**. A bounded cache with reference tiers means hot plans survive in the strong tier, colder ones fall to soft references, and the map never grows unbounded — so the failure mode is not a leak, it is **throughput loss**: every miss re-parses, and a churning workload keeps the compiler busy at exactly the request rate.

| Setting | Default | Role |
| --- | --- | --- |
| `hibernate.query.plan_cache_max_size` | 2048 | max plans held |
| `hibernate.query.plan_cache_max_strong_reference_count` | 128 | plans kept strongly |
| `hibernate.query.plan_cache_max_soft_reference_count` | 2048 | soft tier bound |

## What actually churns the cache — measured

| Query style | Sizes 1–25 of one logical query | Plans compiled |
| --- | --- | --- |
| `id in :ids`, **bound** list, new size each call | 24 hits / 1 miss | **one** |
| `id in (1,2,3)` — **literal** text per size | 0 hits / 50 misses | one **per text** |
| **Criteria**, 1→5 predicates built per request | 0 hits / 5 misses | one **per tree** |

The table is the answer to "does a variable `IN` list churn the plan cache?": **only if the values are inlined into the text**. A bound named parameter compiles once — the list length is execution state, not query shape. Literal inlining (string concatenation "just to build the list") and per-request Criteria assembly are the two real generators; both are design smells that the cache makes visible as CPU and GC pressure. The database's own statement cache suffers the same way for the same reason: each distinct SQL text is a distinct prepared statement there.

`hibernate.query.in_clause_parameter_padding=true` acts on the **JDBC layer**: for expanded parameter lists it pads the number of `?` marks to powers of two (1, 2, 4, 8, 16), collapsing the distinct **SQL texts** the driver and database see — it does not change plan-cache behavior for bound parameters (the plan was already single), and it is irrelevant for text inlining, where padding cannot save a per-size text.

```java
// one plan, any list size — the safe pattern
List<Order> byStatuses(EntityManager em, List<Status> statuses) {
    return em.createQuery("select o from Order o where o.status in :ss",
                          Order.class)
             .setParameter("ss", statuses)
             .getResultList();
}
```

**Listing 1.** A fixed query text with a bound parameter: the plan cache sees one shape; the list is data, not syntax.

## Detection and the fix hierarchy

Plan compilation is CPU-bound; nobody notices one parse. It shows up as **aggregate load**: high CPU under bursty query variety, GC pressure from freshly built plan trees, and thousands of distinct prepared statements on the database. The detection path: enable `Statistics`, compare **`getQueryPlanCacheHitCount`/`getQueryPlanCacheMissCount`** — the hit rate is the first number to look at when query-heavy endpoints burn CPU. Then fix by source: replace literal concatenation with bound parameters (always a win, also for injection safety), stabilize Criteria shapes (build the skeleton per logical shape, vary only bound values), and only then consider a bigger cache — enlarging `plan_cache_max_size` hides symptoms while memory pays. Native SQL skips this cache entirely — it goes to the database as-is ([[What kinds of queries can Hibernate run]] sorts the query kinds; [[What is Hibernate performance tuning]] groups this with the other round-trip levers).

> [!warning] Criteria is not free even when cached
> The Criteria API is chosen for type safety, then rebuilt per request including the parts that never change. Rebuilding is exactly what produces a new tree, a new key, a new plan — the cache measures your query-construction discipline, not your workload. If every request yields a different tree, the hit rate goes to zero and compilation cost becomes a line item on every call.

> [!tip] Interview answer
> The query plan cache stores compiled HQL/Criteria plans keyed by query shape, bounded at 2048 plans by default. The churn question is about shape: a bound named parameter — including `in (:ids)` with a different list size per call — compiles one plan, because the list expands at execution. What really multiplies plans is literal-inlined values and Criteria trees rebuilt per request; I measure that with the Statistics hit/miss counters, replace concatenation with parameters, stabilize Criteria skeletons, and leave `in_clause_parameter_padding` for the JDBC statement-cache layer it actually targets.

See [[What kinds of queries can Hibernate run]], [[What is Hibernate Query Language HQL]], [[What is the JPA Criteria API]], and [[What is Hibernate performance tuning]].
