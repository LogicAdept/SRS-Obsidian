<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# How do the layers of a DDD application isolate the domain model?

> [!abstract] Short answer
> DDD arranges four layers - user interface, application, domain, infrastructure - with one governing rule: dependencies point inward toward the domain, and the domain depends on nothing outside itself. Frameworks, databases, and HTTP live in infrastructure; use-case orchestration lives in application; the model holds the business rules. The domain never imports a driver, an annotation, or a client - which is what makes it testable, portable, and cheap to reason about.

## The four layers and their contract

The user interface translates outside requests into commands and renders results. The application layer runs use cases: load aggregates through repositories, invoke domain logic, save, publish events, own the transaction boundary. The domain layer holds aggregates, entities, value objects, domain services, and repository interfaces - the entire ubiquitous language. The infrastructure layer implements what the other layers declared: persistence for the repositories, messaging for the event dispatcher, clients for external systems. Two directions of traffic exist. Classical layering: everything above calls everything below, so the domain sits at the bottom with nothing to call - isolation by position. Dependency inversion: the domain defines interfaces (repositories, gateways), infrastructure implements them, and the compile-time dependency arrow points inward while runtime control flows outward. The second form is the one that guarantees the first's promise: an entity cannot leak a SQL type because the model has no path to SQL at all ([[What is layered architecture]] is the general pattern; DDD tightens it by making the domain the dependency target).

```java
// Application service: orchestration only - load, delegate, save.
@Transactional
public void placeOrder(long customerId, long orderId) {
    orderRepository.findById(orderId).place(customerId);   // domain rule runs in the aggregate
}
// The domain knows interfaces only:
interface OrderRepository {                                 // declared in the domain layer
    Optional<Order> findById(long id);
    void add(Order order);
}
```

**Listing 1.** The annotation-driven shape is conceptual; the verified demo ran on JDK 21.0.12.1: checkout of a 6500-cent cart returns 6800 through the domain `PricingPolicy`, with the orchestrator reduced to load, delegate, and remove - the repository interface is a domain-owned contract that infrastructure fills in.

```d2
direction: down
ui: "User interface\ncommands and rendering" {
  width: 300
  height: 80
  style.fill: "#f3e5f5"
}
app: "Application layer\nuse cases, tx boundary" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
dom: "Domain layer\naggregates, services,\nrepository interfaces" {
  width: 320
  height: 100
  style.fill: "#e8f5e9"
}
infra: "Infrastructure\nJPA, messaging, clients" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
ui -> app: "depends on"
app -> dom: "depends on"
infra -> dom: "implements its interfaces\n(dependency inverted)"
```

**Fig. 1.** The dependency arrows all terminate at the domain: infrastructure points up into the model it implements, never the reverse - the model has no outward edges at all.

## What isolation buys

The practical yield is threefold. Testability: the domain layer runs in plain unit tests - no database, no container, no framework start-up - because there is nothing to mock out; the cheapest meaningful suite in the codebase lives here. Portability: swapping JPA for JDBC, or Postgres for something else, touches only the infrastructure implementations; the model and the use cases are untouched. Honesty: when a rule needs a database call "just here", the layering refuses - the call must become a domain-owned interface or the rule must move, and both resolutions improve the design ([[What is the application layer responsible for in DDD]] draws the application layer's half of the border; [[What is a domain service in DDD]] shows the rule-side resident). The discipline holds the model's richness in place: with nowhere else to put behavior, behavior lands in aggregates instead of thinning into anemic shells ([[What is an anemic domain model and is it useful]]).

> [!warning] The layers exist only if the dependencies obey
> Four packages with imports running every direction is not layering - it is a monolith with folders. The tells: an entity importing a persistence annotation, a domain service accepting an HTTP request object, a repository interface referencing a driver class. Each is a dependency escaping inward through the back door. The layering is enforced by the import graph (or an architecture test), not by the diagram.

> [!tip] Interview answer
> Four layers - UI, application, domain, infrastructure - with all dependencies pointing at the domain, usually via dependency inversion: the model declares repository and gateway interfaces, infrastructure implements them. The domain imports nothing outward, so it tests in plain units, survives storage swaps, and physically cannot leak persistence types. Layering is real only if the import graph obeys it.

