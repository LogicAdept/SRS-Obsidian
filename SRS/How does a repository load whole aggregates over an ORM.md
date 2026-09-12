<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #Java/Persistence/JPA #SRS

# How does a repository load whole aggregates over an ORM?

> [!abstract] Short answer
> The repository promises whole, invariant-valid aggregates in and out - and over an ORM that promise is a fetch-strategy decision. The aggregate's internal graph (root plus its own entities and value objects) must load eagerly, ideally in one query via a fetch join or entity graph; the ORM's default lazy loading dissolves the boundary into proxies, and navigating them outside the session or across a collection produces `LazyInitializationException` or the N+1 query shape. References to other aggregates stay identity-only, so there is nothing to fetch across the boundary at all - which is why correctly sized aggregates make most N+1 disappear by design.

## The contract versus the proxy reality

The domain-side contract says: `findById` returns a reconstituted aggregate whose invariants hold now ([[What is the repository pattern in DDD]]). The ORM-side default says the opposite: associations load lazily, so what the repository hands back is a shell - a real root row plus proxies for everything under it. Two failure modes follow. Outside the persistence session, the first proxy touch throws `LazyInitializationException`; inside it, every element of a lazy collection costs its own query. One root plus three lines becomes one root query plus three line queries - the N+1 shape - and the aggregate boundary has silently dissolved into per-row access that no longer matches any transactional unit.

```java
// Same "findById", two disciplines (in-memory simulation of the fetch plans):
queries = 0;
Order lazy = lazyRepo.findById(1);            // root row only
int afterLoad = queries;                      // 1; lines are proxies
int n = lazy.lines().size();                  // first navigation pays for the rows
// lazy load:   queries after findById=1, proxy initialized=false; reading 3 lines
//              cost 3 more -> total 4 (N+1 shape)

queries = 0;
Order eager = eagerRepo.findById(1);          // one query: root JOIN FETCH lines
// eager fetch: queries=1, lines initialized=3, fully reconstituted=true

queries = 0;
var cid = eager.customer();                   // CustomerId held as identity
// cross-aggregate: customerId=7 held as id, fetches=0
```

**Listing 1.** Verified on JDK 21.0.12.1 (scripts/empirics/ddd/D15): the lazy discipline costs one query per line at navigation time, the eager discipline loads the whole graph in one query, and the cross-aggregate identity reference costs nothing to "load".

```d2
direction: right
repo: "Repository
findById(orderId)" {style.fill: "#e8f5e9"}
q1: "One query:
root + lines
(fetch join / entity graph)" {style.fill: "#fff3e0"}
agg: "Reconstituted aggregate
invariants hold now" {style.fill: "#e8f5e9"}
id: "CustomerId
identity only" {style.fill: "#eceff1"}
cust: "Customer aggregate
other boundary" {style.fill: "#f3e5f5"}
repo -> q1: "eager inside the boundary"
q1 -> agg
agg -> id: "holds"
id -> cust: "nothing fetched across;\nlookup when actually needed"
```

**Fig. 1.** Eager within the aggregate, identity across aggregates: the fetch plan mirrors the boundary.

## The fetch discipline that keeps the boundary honest

Three rules turn an ORM into a delivery mechanism for aggregates instead of a boundary solvent. First, eager within the boundary: every query path that returns an aggregate declares its fetch plan - a fetch join for root-plus-lines, an entity graph for a wider graph - so the returned object is complete and session-independent ([[What is JOIN FETCH and EntityGraph in Spring Data JPA]] covers the mechanics; [[What is lazy fetch in JPA or Hibernate]] the defaults being overridden). Second, identity across boundaries: `CustomerId`, not a navigable `Customer` - there is no association to lazy-load, no accidental join, and no temptation to walk from an order into another aggregate's graph ([[How do you choose aggregate boundaries]] is where that decision is made). Third, one aggregate per transaction with optimistic locking on the root's version, so the fetch plan and the concurrency plan describe the same unit. The bonus is structural: most N+1 problems come from navigating object graphs that cross what should have been aggregate boundaries - fix the boundary and the query pattern fixes itself ([[What is the N plus 1 problem in Spring Data JPA]] is the general mechanics).

> [!warning] Eager-everywhere and the masks
> The cure has its own overdoses. Fetching two independent collections with fetch joins in one query multiplies rows into a Cartesian product; broad eager graphs load data callers never use. Eager is scoped to one aggregate's own graph, not to the whole model. Two masks hide the disease instead of curing it: open-session-in-view keeps a session alive so lazy access "works" while shipping the N+1 cost into request rendering; and a repository that returns DTOs or partial rows quietly abandons the aggregate contract - callers can no longer tell a consistent unit from a shape convenient for one screen.

> [!tip] Interview answer
> The repository contract - whole aggregates in and out - maps onto fetch strategy: the aggregate's own graph loads eagerly in one query via fetch join or entity graph, so what comes back is reconstituted and session-independent. Lazy proxies are the enemy: they dissolve the boundary into N+1 and `LazyInitializationException`. Cross-aggregate references stay identity-only, so nothing needs fetching across boundaries, and genuinely complex reads bypass the repository entirely into read models - I don't stretch it into a query API.

