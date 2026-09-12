<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #Patterns/Architecture/CQRS #SRS

# How does CQRS complement a DDD domain model?

> [!abstract] Short answer
> DDD builds the write model to be rich - aggregates with invariants, small consistency boundaries, behavior over data - and that is exactly what makes it expensive to query: a cross-aggregate report would load many whole graphs to extract two fields. CQRS splits the flows: commands go through the application service into aggregates and repositories, and the domain events those aggregates publish feed denormalized read models that serve queries directly. Each side gets the shape it is good at - the write model stays normalized around invariants, the read models stay denormalized around query shapes - and the domain stops pretending to be a query engine.

## Why one model serves neither side

The tension is structural, not stylistic. The write model wants small aggregates: boundaries drawn around transactional invariants, references by identity, one aggregate per transaction ([[How do you choose aggregate boundaries]]). A query wants the opposite shape: wide, flat, many aggregates at once - "orders with customer names, item counts, and payment status, filtered by month". Forcing that query through the domain has only bad endings: load N whole order aggregates plus N customer aggregates (an N+1 parade with no fetch-plan defense, since these are cross-boundary reads), or grow repository methods into a query God-object that no longer resembles a collection of aggregates, or denormalize the write model until the invariants blur. The repository stays honest - aggregate-at-a-time - only if heavy reads stop pretending to belong to it ([[What is the repository pattern in DDD]]).

```d2
direction: right
cmd: "Command
place order" {style.fill: "#fff3e0"}
app: "Application service
one tx" {style.fill: "#fff3e0"}
agg: "Order aggregate
enforces invariants" {style.fill: "#e8f5e9"}
ev: "OrderPlaced
(outbox -> broker)" {style.fill: "#fffde7"}
proj: "Projection
transforms" {style.fill: "#e3f2fd"}
rm: "Read model
flat rows / index" {style.fill: "#f3e5f5"}
qry: "Query
orders by month" {style.fill: "#e3f2fd"}
cmd -> app -> agg
agg -> ev: "published after commit"
ev -> proj
proj -> rm
qry -> rm: "direct read,\nno domain involved"
```

**Fig. 1.** Commands pass through the aggregate; the event it published builds the read model; queries never touch the domain.

## The mechanics of the split

The write side does not change: command, application service loads the aggregate, aggregate method checks invariants, state change plus event row commit atomically in the outbox ([[How does an aggregate persist and publish events without a distributed transaction]]). The read side is built from those same events: a projection subscribes, transforms each fact into rows of the shape its queries need - a flat table, a view, a search index - and rebuilds from scratch by replay if the shape changes ([[What is a projection in CQRS and event sourcing]]). Adoption can start inside one database: separate query objects over the same store, read models as tables or views, and split engines only when a side's scaling actually demands it. The price is named up front: read models lag the write by the relay's delay, so the UI tolerates read-your-writes gaps, and projections must be idempotent because delivery is at-least-once. When that price is not worth paying - plain CRUD, no read/write divergence - the same DDD model serves both sides and CQRS adds nothing ([[What is CQRS]] covers the levels; [[Which kinds of projects benefit most from CQRS]] the fit checklist).

> [!warning] The split must not flow backward
> Two corruptions to refuse. First, business rules leaking into projections: a read model that computes eligibility or defaults is a second, unguarded domain - read models are disposable derivations of facts, and any rule they seem to need belongs in the aggregate that emits the events ([[What is an anemic domain model and is it useful]] is the write-side version of the same disease). Second, rebuilding write truth from read models: the stream of domain events is the history, projections are caches - correcting data means a new event, not an `UPDATE` on the projection.

> [!tip] Interview answer
> DDD optimizes the write model for invariants, which makes it a bad query engine - cross-aggregate reads would load whole graphs for two fields. CQRS resolves the tension: commands run through aggregates and repositories; the domain events they publish feed purpose-shaped read models that queries hit directly. I keep the write side untouched, start with read models in the same store, and accept eventual consistency plus idempotent projections as the cost - and I skip the whole split for CRUD-shaped domains.

