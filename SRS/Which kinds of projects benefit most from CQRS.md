<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/CQRS #SystemDesign/Tradeoffs #SRS

# What is CQRS for and when is it worth its cost

> [!abstract] Short answer
> CQRS (Command Query Responsibility Segregation) pays off when the read and write sides diverge sharply: very different data shapes for queries versus updates, massive read/write ratio asymmetry, collaborative domains with concurrent updates, or queries requiring denormalized views a normalized model cannot serve cheaply. Simple CRUD systems — where reads and writes use the same shape anyway — gain complexity and lose nothing; Fowler's caution is explicit that the pattern is for cases that need it, not a default.

## Where the payoff is real

The benefiting projects share measurable divergence. Read/write asymmetry: catalogs, feeds and dashboards are read millions of times per write — separate query models (denormalized, precomputed, cached in their own store) can be indexed and shaped for the query without contorting the write model; the write side stays normalized and consistent ([[What is database denormalization for]] is the mechanics of the read side). Shape divergence: the write model wants aggregates enforcing invariants ([[What are aggregate aggregate root entity and value object in DDD]]-style consistency boundaries), while queries want wide, flat projections joining many entities — when both live in one model, every change compromises one side. Collaborative domains: many concurrent actors updating the same entities (booking systems, editors) benefit from explicit commands plus events, where optimistic concurrency and event-driven projections manage contention. Event sourcing synergy: when the system already persists events, projections ARE query models — CQRS is the natural companion. Scale divergence: reads scaled by replicas and caches, writes by sharding — separating the sides lets each scale independently ([[How do NoSQL databases scale compared with SQL databases]]'s engine choice becomes per-side).

```text
strong fit:  read/write ratio extreme; query shape != write shape;
             collaborative contention; event sourcing already present
weak fit:    CRUD with 1:1 form-to-table mapping; small team;
             no measured read/write divergence
cost to accept: two models to maintain + sync pipeline (events/outbox)
                 + eventual consistency on the read side
```

**Listing 1.** The fit checklist against the standing costs.

## The costs that disqualify

CQRS is two models, a synchronization pipeline (events, outbox — [[How does an aggregate persist and publish events without a distributed transaction]]), eventual consistency on reads ([[What is eventual consistency]] and its UX consequences — "I saved it, where is it?"), and more moving parts for ops. Fowler's article frames the default skepticism: most systems' CRUD works fine with one model, and the pattern's complexity is justified only when read/write divergence is real and measured. The migration path also matters: adopting CQRS does not require two databases on day one — the segregation can start within one store (separate query objects, read models as tables or views) and graduate to separate engines only when a side's scaling demands it ([[How would you explain CQRS]] covers the pattern's mechanics; [[Which kinds of projects benefit most from CQRS]]-adjacent tradeoffs mirror the layered-architecture story in [[What is layered architecture]]: structure follows measured need, not fashion).

> [!warning] CQRS applied to CRUD is architecture tourism
> Splitting a one-form-one-table domain into commands, events, projections and two stores adds a distributed pipeline to sync data that never diverged. If reads and writes share shape and scale, CQRS is pure overhead — adopt it where divergence is measured, not where talks were watched.

> [!tip] Interview answer
> CQRS pays when read and write sides genuinely diverge: extreme read ratios, query shapes a write model cannot serve, collaborative contention, or event sourcing already in place. It costs two models, a sync pipeline and eventual read consistency — so for plain CRUD I keep one model. Start segregation inside one store and split engines only when a side demands it.
