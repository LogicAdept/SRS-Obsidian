<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is an anemic domain model and is it useful?

> [!abstract] Short answer
> An anemic domain model is a model where domain objects carry only data - public fields or getters/setters - while all business rules live in separate service classes that manipulate that data. It is usually a code smell in a DDD context because invariants stop being enforced by the objects themselves; any code that can touch the object can put it into an invalid state. It is genuinely useful in narrow cases: simple CRUD contexts, integration or read-model layers, and generated transport types - places where there are few rules to model in the first place.

## How to recognize it

The shape is easy to spot. Entities are bags of mutable data with an accessor for everything; a parallel "service" or "manager" layer holds all behavior, typically as long procedural methods. Martin Fowler, who named the pattern in 2003, describes it as the opposite of what encapsulation is supposed to buy you: bundling data with the functions that operate on it. Microsoft's DDD guidance explicitly steers the other way - "domain entities with rich models (no anemic domain model)" - for contexts with real business rules.

```java
// Anemic: every caller decides the rules
Order o = repo.find(id);
o.setStatus(Status.SHIPPED);          // no check that it was PAID first
o.setTotal(Money.of(0));              // who says a total can be zero?
```

**Listing 1.** Conceptual. The "model" cannot refuse anything, so the shipping rule "only paid orders ship" lives in whichever service remembers it. A second code path will eventually forget.

## Why it happens and when it is fine

Anemia usually has structural causes: frameworks and mappers (JPA, Jackson, code generators) push toward default constructors and setters; teams habituate to transaction scripts; and "model" classes get shared across contexts, so behavior that is valid in one flow is wrong in another, and everything mutable gets stripped down to data. The useful cases are the mirror image: a bounded context that genuinely has few invariants (an admin table, a settings store), read models and projections in CQRS that just carry query results, and DTOs at system edges. In those spots the anemic shape is honest - there is little behavior to hide.

> [!warning] "The services enforce the rules, so nothing is lost"
> That claim fails on scale and on time. On scale: the same invariant is now re-implemented in several services, and the next developer adds a fourth copy with a subtle difference. On time: the compiler and the type system no longer know which states are legal, so every future change must rediscover the rules by reading service code. That is exactly the maintenance profile that [[What are coupling and cohesion and how do they affect maintainability|coupling and cohesion]] measures - low cohesion, high coupling - and it is why an anemic core tends to rot into scattered, duplicated checks ([[What is a domain model]]).

> [!tip] Interview answer
> Anemic means data-only domain objects with the logic pushed into services. In a rich DDD model the object guards its own invariants, so illegal states are unrepresentable; in an anemic one, correctness depends on every caller being disciplined. I still use the anemic shape for CRUD-ish contexts, read models, and DTOs at the edges - there the rules are trivial and the simplicity is real, not lost.
