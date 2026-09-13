<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the repository pattern in DDD?

> [!abstract] Short answer
> A repository is a domain-level abstraction that pretends a collection of one aggregate type exists in memory: `add`, `findById`, `remove` - as if you could just take an order off the shelf. It loads and saves whole aggregates, hides how they are stored, and lets the domain model stay persistence-ignorant. Typically one repository interface per aggregate root, defined in the domain, implemented in infrastructure.

## The collection illusion

The metaphor is the contract: the caller thinks in terms of a set of orders, not rows, tables, or queries. A repository takes a whole valid aggregate and stores it; hands back a whole reconstituted aggregate on lookup; deletes by identity. What it never does: return half an aggregate (a list of order lines without their root), expose query builders up into the domain, or leak persistence vocabulary - no session, no entity manager, no row maps in the interface. Reconstitution is the quiet half of the job: on load, the store returns flat data, and a factory rebuilds the aggregate with its history intact - the same invariants checked as on creation, just from stored state ([[What is the factory pattern in DDD]]).

```java
// REPOSITORY: collection-like interface over aggregates.
interface OrderRepository {
    void add(Order order);
    Optional<Order> findById(long id);
    boolean remove(long id);
}

// In-memory implementation: "persistence" flattens the aggregate; loading reconstitutes it.
@Override public Optional<Order> findById(long id) {
    String[] row = store.get(id);
    if (row == null) return Optional.empty();
    return Optional.of(Order.reconstitute(id, row[0], historyStore.get(id)));
}
```

**Listing 1.** Verified on JDK 21.0.12.1: saving an order and loading it back yields a different instance with the same history (`same instance after save+load: false`), which is exactly the promise - a collection of aggregates, not a cache of objects.

```d2
direction: right
dom: "Domain model\nOrderRepository interface" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
impl: "Infrastructure\nJPA / JDBC / in-memory impl" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
db: "Storage\nrows, tables, indexes" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
dom -> impl: "depends on\nits own interface"
impl -> db
agg: "Whole aggregates\nin, whole aggregates out" {
  width: 250
  height: 80
  style.fill: "#f3e5f5"
}
dom -> agg: "the illusion"
```

**Fig. 1.** The interface lives in the domain and the implementation in infrastructure; across the seam travel only whole, valid aggregates.

## Scope and limits

One repository per aggregate root, not per entity: lines, items, and children come and go through their root, so a `OrderLineRepository` is a design smell - the aggregate boundary and the repository boundary coincide by construction. The interface belongs to the domain, the implementation to infrastructure; that inversion is what lets the model run against an in-memory fake in tests and against a real store in production. Repositories are for the write side's aggregates - loading by identity, saving whole changesets. Complex reads across many aggregates do not belong to them: that is a query model or a read side of its own (CQRS-style), and stretching the repository into a reporting API bloats it into an anemic query God-object - the split done right is [[How does CQRS complement a DDD domain model]].

Spring Data's repository abstraction shares the name and the collection metaphor, but a DDD repository is a modeling decision - one per aggregate root, whole-aggregate discipline - not something the framework grants for free ([[What are Spring Data Repository interfaces]]).

> [!warning] The leaky repository
> Three classic leaks: returning lazy-loading proxies so the domain triggers SQL by navigation (the aggregate boundary dissolves into N+1s - the fetch-side discipline that prevents this is [[How does a repository load whole aggregates over an ORM]]); adding a query method per UI screen until the interface is a query language (the read side has no boundary at all); and letting the implementation hand out DTOs - then callers cannot tell whether they hold an aggregate or a projection. If a repository method returns something that is not an aggregate, the pattern has already failed ([[What are aggregate aggregate root entity and value object in DDD]]).

> [!tip] Interview answer
> A repository gives the domain a collection-like abstraction over one aggregate type: add, find by id, remove - whole aggregates in, whole aggregates out, reconstituted through a factory. The interface lives in the domain, the implementation hides infrastructure, and the aggregate root is the unit of persistence. It is not a query API or a DAO over tables - it is the persistence face of the aggregate boundary.

