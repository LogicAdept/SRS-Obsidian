<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is a domain model?

> [!abstract] Short answer
> A domain model is a working software abstraction of a specific business area: the concepts, their data, their rules, and the operations allowed on them. In DDD the model is not a diagram or a database schema - it is executable code (entities, [[What is a value object and why should you use one|value objects]], aggregates, domain services) that enforces the business invariants itself. A good test: if the domain rules change, you change the model classes; if you only ever change controllers and SQL, you have no real domain model.

## What lives inside the model

Within one bounded context the model is built from DDD's tactical pieces. Entities carry identity that survives state changes (a shipment is the same shipment after rerouting). Value objects describe things measured by their attributes and are immutable (an address, a money amount). Aggregates group entities and values under a root that guards consistency. Domain services hold operations that genuinely involve several aggregates and no single owner. The model also speaks the business vocabulary: class and method names come from the ubiquitous language, so a domain expert can roughly follow a code review. The collaborative loop that builds and refines such a model together with the business is [[What is knowledge crunching in DDD]].

```java
public class Order {
    private final OrderId id;
    private CustomerId customer;
    private OrderStatus status = OrderStatus.DRAFT;
    private final List<OrderLine> lines = new ArrayList<>();

    public void addItem(Sku sku, int qty, Money unitPrice) {
        if (status != OrderStatus.DRAFT)
            throw new IllegalStateException("Order already placed");
        lines.add(new OrderLine(sku, qty, unitPrice));
    }

    public Money total() {
        return lines.stream().map(OrderLine::lineTotal)
                    .reduce(Money.ZERO, Money::add);
    }
}
```

**Listing 1.** Conceptual. The rule "no line items after the order is placed" lives in the model, so every caller gets the same protection - not just the ones that remember to ask a service first.

## Rich model vs schema-plus-services

The alternative that DDD argues against is a model reduced to data bags: classes with fields and accessors whose behavior sits in a separate service layer. That is the [[What is an anemic domain model and is it useful|anemic domain model]] - and it quietly moves all invariants into whichever service happens to touch the data, so nothing stops a new code path from bypassing them. A rich model keeps behavior with the data it guards: for contexts with significant rules, the entities carry the behavior - no anemic model.

> [!warning] "Domain model = ER diagram" is the classic trap
> An entity-relationship diagram describes data shape, not behavior. A domain model includes state transitions and invariants: when an order may be cancelled, what makes a price valid, who may approve a refund. If your "model" cannot answer those questions, it is a schema, and the real model is hidden inside service methods.

> [!tip] Interview answer
> A domain model is the executable representation of a business area inside one bounded context: entities with identity, immutable value objects, aggregates protecting invariants, and services for cross-aggregate operations, all named in the business vocabulary. The key property is that rules live in the model itself, so changing business behavior means changing model classes, not hunting through orchestration code.
