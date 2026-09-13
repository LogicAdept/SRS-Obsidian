<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Cache #Persistence/Caching #SRS

# What is the Hibernate query cache and when does it help?

> [!abstract] Short answer
> The query cache stores **result sets of queries**: not entity data, but the **entity ids** (plus scalar values for projections), keyed by the query text and its bound parameter values. A hit therefore still needs the **second-level cache** to resolve those ids into entity state — that is why the query cache only works with L2 enabled and `hibernate.cache.use_query_cache=true`, and per-query with the `org.hibernate.cacheable` hint. Its fatal trade-off is **coarse invalidation**: any committed write to a table the query touches invalidates the whole query region for that table — even if the written row was never in the result. Measured on Hibernate with a JCache provider: a repeat run of the cached query issues **zero SQL** (ids from the query cache, state from L2); after a single unrelated `UPDATE` on the same table, the next run re-executes SQL; the same query without the hint hits the database **every call**. It helps for read-mostly, expensive, repeatedly-executed queries — and quietly wastes memory and invalidation traffic everywhere else.

## Two-phase lookup: ids first, state second

The cache entry is deliberately thin. For an entity-returning query, the cached value is the list of primary keys; for scalar projections it is the raw values. On a hit, Hibernate reconstructs the result by looking each id up in the **entity L2 cache** — if an entity is not cached there, it falls through to a **per-entity SELECT**, which turns a "cache hit" into a fan-out of small queries. This is the trap behind "I enabled the query cache and got slower": caching a query over non-cacheable entities buys you an id list that must be re-fetched row by row. The invalidation bookkeeping lives in the **update-timestamps cache**: each table has a last-write timestamp, and a cached result is fresh only if every table it reads has not been written since the result was stored. That design makes reads cheap and freshness conservative — it never serves stale rows, but it pays for that with **all-or-nothing invalidation per table**.

Measured behavior of one cached query `select p from Person p order by p.id` over three rows, JCache provider enabled:

| Step | exec | hit | put | miss | SQL issued |
| --- | --- | --- | --- | --- | --- |
| first run, `cacheable` hint | 1 | 0 | 1 | 1 | yes — result set cached |
| repeat run, new session | 1 | 1 | 1 | 1 | **none** |
| one row `UPDATE`d, committed | — | — | — | — | — |
| next run after update | 2 | 1 | 2 | 2 | yes — region invalidated |
| query **without** the hint, twice | 4 | 1 | 2 | 2 | yes, **on every call** |

The `exec` counter moving 1→2 after a single unrelated row update is the whole story: the write poisoned the region for every cached query reading `persons`, regardless of which rows they return.

## When it pays off — and when it is pure overhead

| Situation | Verdict | Why |
| --- | --- | --- |
| Reference/rarely-changed data, hot query | **helps** | invalidations are rare; hit rate near 100% |
| Expensive report/paging query, stable filter values | **helps** | one cached result removes an expensive scan |
| Table with frequent writes | **hurts** | every commit invalidates; region never lives long enough to be hit |
| High-cardinality parameters (per-user, per-request ids) | **hurts** | a key per parameter set, each hit once, memory paid for nothing |
| Query over non-cacheable entities | **hurts** | hit → id fan-out of per-entity SELECTs |
| Write-mostly OLTP workload | **do not enable** | invalidation bookkeeping + memory for zero reuse |

The decision rule: the query cache amortizes only when the **ratio of reads to writes on the queried tables is very high and the parameter set is small**. Reference data, config, and slowly changing catalogs are the natural fit; end-user dashboards over transactional tables are the natural anti-fit.

```java
// enable once: hibernate.cache.use_second_level_cache=true,
//              hibernate.cache.use_query_cache=true + a RegionFactory
List<Person> persons = session.createQuery(
        "select p from Person p where p.status = :s order by p.id", Person.class)
    .setParameter("s", Status.ACTIVE)
    .setHint("org.hibernate.cacheable", true)          // opt-in per query
    .getResultList();
```

**Listing 1.** The hint is per query, not global: only explicitly marked queries enter the cache, and each query gets its own region (nameable, so hot queries can get their own TTL/limits).

> [!warning] Native SQL does not invalidate itself
> A cached query is kept fresh through the update-timestamps entries of the tables Hibernate **knows** it reads. A native query has no query-space analysis, so caching one alongside ORM writes requires declaring the affected tables explicitly (`addSynchronizedEntityClass`/`addSynchronizedQuerySpace`) — otherwise the cached result goes stale silently, which is the one failure mode this cache normally excludes.

> [!tip] Interview answer
> The query cache stores query results as entity ids plus scalars, keyed by query text and parameters; a hit resolves ids through the second-level cache, so it requires L2 and the `org.hibernate.cacheable` hint. Freshness is enforced by an update-timestamps cache, which makes invalidation per-table: any committed write to a table the query touches drops the whole region — measured, one unrelated row update forced the next run to re-execute SQL, while a repeat run without writes issued zero SQL. It is a win for read-mostly, small-parameter-set, expensive queries, and a loss for write-heavy tables or high-cardinality parameters; and native queries must declare their synchronized spaces or they bypass the freshness guarantee.

See [[What are Hibernate first and second level cache tiers]], [[What is Hibernate second level cache and its main components]], [[What is the Hibernate query plan cache]], [[What is Hibernate performance tuning]], and [[What are Hibernate named queries]].
