<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceCollaboration #Methodologies/DDD #SRS

# How do aggregates shape data ownership between services

> [!abstract] Short answer
> In the data patterns for microservices, the DDD aggregate is the unit of service ownership: a service owns its aggregates, other services reference them by identity - never by holding a shared copy or joining its tables - and one transaction updates one aggregate. Aggregates turn "whose data is this" from a convention into a rule, which is what makes database-per-service enforceable.

## The three rules that carry across service boundaries

First, one transaction, one aggregate: an aggregate is a consistency boundary - its invariants are enforced atomically inside a transaction, and anything outside the boundary is eventually consistent by design. Across services this becomes the rule that a business transaction touching two services' data cannot be one ACID transaction; it becomes a saga with compensations, and the aggregate boundary tells you where the local part ends. Second, reference by identity: an Order aggregate references a Customer by customerId; it does not carry a synchronized copy of the customer's fields. If Order Service needs customer details to work synchronously, it either calls Customer Service or keeps a projection - an explicitly fed replica - rather than mutating data owned elsewhere. Third, the aggregate is the sharing unit: when services must exchange data, what crosses is an aggregate's identity plus a committed domain event - never direct reads of another service's tables. That last rule is what keeps [[How would you explain the database per service pattern]] honest: shared tables would silently merge two models and re-create the coupling the pattern removed.

```d2
direction: right
osvc: "Order Service
owns Order aggregate" {style.fill: "#e8f5e9"}
o: "Order
+ customerId (identity)
+ lineItems (invariants)" {style.fill: "#e8f5e9"}
csvc: "Customer Service
owns Customer aggregate" {style.fill: "#e8f5e9"}
c: "Customer
address, credit" {style.fill: "#e8f5e9"}
osvc -> o: one tx per aggregate
csvc -> c: one tx per aggregate
o -> c: customerId only
```

**Fig. 1.** Order Service holds the customer's identity, not the customer's data; anything else crosses as an API call or an event.

The definitions - aggregate root, entities, value objects, why the root guards invariants - live in [[What are aggregate aggregate root entity and value object in DDD]]; this card is the architecture-side consequence. The aggregate pattern makes the ownership framing explicit: design the business logic as aggregates so that services can be cut along the same seams and events can be attached to state changes - which is why the aggregate, the domain event and the outbox form one toolkit ([[How does an aggregate persist and publish events without a distributed transaction]] shows the persistence-plus-publication flow end to end).

## Consequences you will be asked about

Sizing: aggregates that are too large (an "Everything" aggregate spanning warehouse, billing and support concerns) block decomposition - every transaction contends, every service wants to own it. Aggregates that are too small (every row its own aggregate) dissolve the invariants and push consistency into compensating logic everywhere. The interview-grade heuristic: an aggregate should be as small as its invariants allow and no smaller. And the honesty point: cross-aggregate, cross-service queries and reports still need composition or event-fed projections - ownership rules do not remove the need for [[What is the API composition pattern in microservices]] on the query side.

> [!warning] A foreign key is not ownership
> The trap: service A's schema has a FK to service B's table, and someone reads that as license to join across the boundary. The FK documents an identity relationship; it does not grant write or read access to another service's store. The second trap: replicating "just a couple of fields" with ad-hoc updates from both sides - that is a shared copy of an aggregate, the exact thing identity references exist to prevent. Replicas are fine when they are one-way projections fed by events, and poisoning happens the moment the copy's owner is ambiguous.

> [!tip] Interview answer
> Aggregates are the unit of data ownership across services: a service owns its aggregates, others reference them by identity, one transaction updates one aggregate. That is what makes database-per-service real instead of nominal - no shared tables, no ad-hoc field copies; anything crossing a boundary is an API call or a domain event. Big aggregates block decomposition, tiny ones dissolve invariants, so I size them by their consistency rules.
