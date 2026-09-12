<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is a domain service in DDD?

> [!abstract] Short answer
> A domain service is a stateless object that carries domain logic which does not naturally belong to any single entity or value object - typically a rule or calculation that spans several aggregates, needs a policy of its own, or would otherwise be smeared across callers. It speaks the ubiquitous language, holds no request state, and does no I/O. It is not the application service: no use-case orchestration, no transactions, no repositories.

## When a service is the right home

Three signals justify a domain service. The operation spans multiple aggregates or entities (transferring between accounts involves two accounts and their mutual invariants). The rule is a genuine domain concept with a name (a pricing policy, an approval policy, a scheduling algorithm) but no natural owner object. The logic would otherwise be duplicated in several application-layer callers. The service is then named in domain terms - `PricingPolicy`, `TransferService` - and the ubiquitous language gains a word for it. What it must not do: fetch from repositories, decide transaction boundaries, format responses, or accumulate state between calls. A domain service with dependencies beyond other domain objects is usually an application service in disguise.

```java
// Domain service: pure business rule, no I/O, no request state.
static final class PricingPolicy {
    Money priceFor(Cart cart) {
        Money sub = cart.subtotal();
        return sub.cents() >= 10_000 ? sub : sub.add(Money.of(300));   // small-cart fee
    }
}

// Application service orchestrates; the rule stays out of it.
Money checkout(long cartId) {
    Cart cart = repo.get(cartId);              // 1. load aggregate
    Money total = pricing.priceFor(cart);      // 2. delegate the rule to the domain
    repo.remove(cartId);                       // 3. persist the effect
    return total;
}
```

**Listing 1.** Verified on JDK 21.0.12.1: checkout of a 6500-cent cart returns 6800 - the fee rule lives in `PricingPolicy`, so it is testable without any repository and swappable without touching the orchestrator.

```d2
direction: right
app: "Application service\nuse-case orchestration\ntx boundary, repositories" {
  width: 270
  height: 100
  style.fill: "#fff3e0"
}
domsvc: "Domain service\nrule spanning entities\nno I/O, stateless" {
  width: 270
  height: 100
  style.fill: "#e8f5e9"
}
agg: "Aggregates and value objects\nown-state rules" {
  width: 270
  height: 100
  style.fill: "#e3f2fd"
}
app -> domsvc: "delegates the rule"
domsvc -> agg: "operates on"
```

**Fig. 1.** The two service kinds sit on opposite sides of the I/O line: the application service talks to infrastructure, the domain service talks only to domain objects.

## Service vs richer alternatives

A domain service is the third choice, not the first. Logic that belongs to one object's state goes into that entity or value object; logic about creating or looking up aggregates goes to factories and repositories. Reach for the service only when no single object owns the rule - otherwise services become a dumping ground and the model slides into anemia ([[What is an anemic domain model and is it useful]]): entities as data bags, all behavior in services, and the ubiquitous language stranded outside the model. The test: if the service's method could plausibly be a method on one of its arguments, it should be.

The word "service" overloads badly. A domain service is not a microservice (that is a deployment unit) and not an application service (that is the orchestrator layer, [[What is the application layer responsible for in DDD]]). In an interview, name the layer explicitly before answering.

> [!warning] The service-layer swamp
> The classic drift: one `XxxService` per entity with every rule inside, entities reduced to getters and setters. The tell is in the aggregate card's rules - if invariant checks migrated from the aggregate into services, the consistency boundary dissolved ([[What are aggregate aggregate root entity and value object in DDD]]). Domain services are seasoning, not the meal.

> [!tip] Interview answer
> A domain service is a stateless, I/O-free object for domain logic that spans multiple entities or aggregates or represents a named policy - a pricing or approval rule that no single object owns. It differs from an application service, which orchestrates use cases, transactions, and repositories but contains no business rules. Overusing domain services is how anemic domain models happen.

