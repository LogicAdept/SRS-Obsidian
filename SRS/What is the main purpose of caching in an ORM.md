<!--
reps: 0
priority: 0
-->
#Persistence/ORM #Persistence/Caching #SRS

# What is the main purpose of caching in an ORM?

> [!abstract] Short answer
> An ORM caches for two different reasons at two different layers. The **first-level cache** — the persistence context itself — exists for **correctness first**: it is an identity map (one database row → one object instance per session), it deduplicates repeated loads of the same row, and it is the memory in which dirty checking accumulates changes so that ten setter calls become one `UPDATE` at flush. The **second-level cache** exists for **throughput**: it removes repeated row round-trips across sessions for data that is read far more often than it is written. Neither layer is a method-result memoization like the application-level cache abstractions: keys are entity ids, entries are disassembled entity state, and invalidation is driven by the ORM's own write path (and update timestamps), not by hand-written eviction. That is also the boundary of the idea — an ORM cache cannot safely serve stale data across transactions without an explicit opt-in, so it is never a substitute for an application cache with its own freshness policy; it is a mechanical accelerator for object access.

## First level: identity map and write-behind

Strip the persistence context down and you find three jobs that only make sense together. **Identity**: loading row 42 twice must return the same instance, otherwise two references to "the same" order inside one transaction could disagree — object-graph consistency in memory depends on this. **Deduplication**: every load and every association walk first checks the context, so a lazy graph revisits cost nothing and N+1 smells become visible instead of being silently paid. **Write-behind**: changes are detected against a snapshot at flush time and batched into an ordered action queue, so the number of SQL statements depends on how many rows you actually changed, not how many setters you called. Because this cache lives and dies with the session, it never needs invalidation and never leaks across transactions — its cost profile is the opposite: a large context makes every flush-time dirty check more expensive, which is why "keep the session small" is the first tuning advice ([[What is Hibernate dirty checking]]).

## Second level: round-trip elimination with a price tag

The L2 cache is opt-in per entity type and per workload. It pays when the same rows are read across sessions repeatedly — reference data, product catalogs, config-like entities — and it costs on every write: invalidation must run, and in a cluster it must propagate, or the nodes diverge. Unlike the first level it **can** serve stale data in some configurations (strictness depends on the cache strategy and the provider), which is precisely why it is a trade-off to be measured, not a checkbox. The natural failure mode is enabling it for a write-heavy entity "for speed" and getting invalidation traffic plus stale reads instead ([[What are Hibernate first and second level cache tiers]] separates the tiers; [[What is Hibernate second level cache and its main components]] details the machinery).

| | First-level (persistence context) | Second-level | Application/method cache |
| --- | --- | --- | --- |
| Purpose | identity + change tracking | skip row round-trips | skip arbitrary computation |
| Scope | one session | session factory / cluster | whole application |
| Keys | entity ids (implicit) | entity ids (implicit) | anything you define |
| Invalidation | none needed (dies with session) | on ORM writes, per entity | manual, TTL, or explicit |
| Correctness risk | none (within its guarantees) | staleness across sessions | staleness by design |
| Always on? | yes | opt-in | opt-in |

The third column is the comparison that makes the first two meaningful: a method cache ([[What is the Spring cache abstraction]]) caches **the answer to a question you asked**, with your keys and your eviction policy; the ORM caches **object state**, with the ORM's invalidation guarantees. They solve different problems and stack: an application cache in front of an ORM-backed service does not replace either ORM tier, it just moves the hit ratio problem one layer up ([[What is caching used for]] covers the general idea, and multi-level setups stack all of them).

> [!warning] An ORM cache is not a substitute for understanding isolation
> L1 makes in-memory reads consistent within the session; it says nothing about what other transactions see. L2 under relaxed strategies can surface values that a plain database read would never return. Reading the isolation level of the database and the concurrency strategy of the cache together is mandatory before trusting either.

> [!tip] Interview answer
> The first-level cache is the persistence context — an identity map that guarantees one row is one object per session, deduplicates loads, and buffers dirty-checking so writes batch at flush; it is correctness machinery and always on. The second-level cache is throughput machinery — opt-in per entity, cross-session, invalidated through the ORM's write path and update timestamps, with real staleness and cluster costs when misapplied. Neither is a method-level cache: keys and entries are entity state, not arbitrary results, and that difference defines when each is the right tool. I keep the session small, measure L2 hit ratios before trusting it, and never use a cache to paper over an isolation question.

See [[What are Hibernate first and second level cache tiers]], [[What is Hibernate dirty checking]], [[What is the Spring cache abstraction]], [[How would you explain cache hit rate and cache miss rate]], and [[What are the drawbacks of lazy loading]].
