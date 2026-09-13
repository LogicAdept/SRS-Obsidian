<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the application layer responsible for in DDD?

> [!abstract] Short answer
> The application layer coordinates use cases: it receives a command, loads the relevant aggregates through repositories, invokes the domain logic, saves changes, publishes recorded events, and draws the transaction boundary - and it writes no business rules of its own. It is the thinnest layer with the clearest definition of failure: any `if` about domain behavior inside it is a rule that leaked out of the model.

## The anatomy of one method

A well-formed application service method reads as a script of the use case, not an algorithm. Place an order: load the customer (a different aggregate - read-only here), load or create the order aggregate, call `order.place(...)` so the aggregate enforces its invariants, save through the repository, dispatch whatever events the aggregate recorded after the transaction commits, return a result. Every meaningful decision in that sequence belongs to someone else: invariants to the aggregate, lookup mechanics to the repository, publication to the event dispatcher. The layer's own decisions are technical - isolation level, idempotency of the entry point, retry semantics, security checks - and those are legitimate here precisely because they are not domain rules.

```java
// Application service: orchestration only.
@Transactional
public void placeOrder(long customerId, long orderId) {
    orderRepository.findById(orderId).place(customerId);   // domain does the rule
    // @Transactional commits; events publish after the commit
}
// vs the domain service it calls into - pure logic, no I/O.
Money total = pricing.priceFor(cart);                       // rule lives in the domain
```

**Listing 1.** The `@Transactional` shape is the standard Spring idiom (conceptual here). The verified half is the domain-vs-application demo on JDK 21.0.12.1: checkout total 6800 comes back from the domain service, and every rule - the small-cart fee - lives in `PricingPolicy`.

```d2
direction: down
ui: "API / UI" {
  width: 200
  height: 60
  style.fill: "#f3e5f5"
}
app: "Application service\nuse case: place order" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
repo: "Repositories\nload / save aggregates" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
domain: "Domain model\naggregate enforces invariants" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
events: "Event dispatch\nafter commit" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
ui -> app
app -> repo
repo -> domain
app -> domain: "invoke"
app -> events: "after commit"
```

**Fig. 1.** Everything hangs off the application service, but nothing domain-shaped stays in it: rules run in the model, storage runs behind repositories, events publish after the commit.

## Why thin matters

Thickness here is not a style issue; it is where anemic models are born. When invariants creep into the orchestrator - "if cart total is under threshold, add fee" - the aggregate stops guarding them, and every new caller reimplements or forgets the rule. The domain model becomes DTOs with getters and the codebase becomes a transaction script in an object costume ([[What is an anemic domain model and is it useful]]). The reverse leak matters too: the application layer is the only place allowed to know that placing an order and reserving stock are separate transactions on separate aggregates ([[Why should one transaction update only one aggregate]]) - the model should not contain that orchestration knowledge either.

The layer also justifies itself in testing: an application service test needs the domain plus fake repositories, no HTTP, no serialization - the use-case suite is the cheapest meaningful suite in the codebase.

> [!warning] Two directions of leakage
> Rules leaking up (invariants in the orchestrator) kill the model. Infrastructure leaking down (HTTP concerns inside entities, persistence calls inside domain services) kills reuse and testability. The application layer is the border between them: it may touch infrastructure and the domain, and must let each stay ignorant of the other - which is the layered arrangement DDD inherits and tightens ([[What is layered architecture]], [[What is a domain service in DDD]]).

> [!tip] Interview answer
> The application layer orchestrates use cases: load aggregates via repositories, call domain logic, save, publish events after commit, own the transaction boundary. It contains no business rules - the moment an invariant appears in it, that invariant belongs in an aggregate. Thin application layer plus rich domain model is what keeps DDD from collapsing into anemic services.

