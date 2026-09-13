<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What are aggregate, aggregate root, entity, and value object in DDD?

> [!abstract] Short answer
> These are DDD's tactical building blocks. An entity is an object defined by identity that persists across state changes. A value object is an immutable object defined entirely by its attribute values with no identity. An aggregate is a cluster of entities and value objects that changes together under one transaction, and the aggregate root is the single entity through which the outside world must touch the cluster - it guards the invariants. The rules that follow: outside code references the root, reaches inner members only via the root, references other aggregates by ID only, and one transaction modifies one aggregate.

## How the blocks relate

An entity answers "which one is it?" - two `Customer` objects with different IDs are different customers even if every field matches (see [[In a business context must equals consider all entity fields]] for when business equality should compare fields anyway). A value object answers "what is it worth?" - two `Money(10, USD)` are interchangeable, so it is immutable and compared by value. The focused comparison lives in [[What is the difference between an entity and a value object]]. The aggregate composes them into a consistency unit: `Order` (root entity) plus its `OrderLine` entities and `Address` value object. The root enforces invariants spanning the cluster - line totals match the header, status transitions are legal - because it is the only door in.

```java
public class Order {                                     // aggregate root
    private OrderId id;
    private OrderStatus status = OrderStatus.DRAFT;
    private final List<OrderLine> lines = new ArrayList<>();   // inner entity
    private Address shipTo;                                    // value object

    public void cancel() {
        if (status == OrderStatus.SHIPPED)
            throw new IllegalStateException("Shipped order cannot be cancelled");
        status = OrderStatus.CANCELLED;
    }

    public void addItem(Sku sku, int qty, Money unit) {        // guarded mutation
        if (status != OrderStatus.DRAFT)
            throw new IllegalStateException("Order is sealed");
        lines.add(new OrderLine(sku, qty, unit));
    }
    // deliberately no getLines() returning the mutable list
}
```

**Listing 1.** Conceptual. Every mutation of the cluster goes through a root method that can check invariants first; callers never reach into `lines` directly.

## The consistency rules that make it an aggregate

Three rules turn "a cluster of objects" into an aggregate. First, identity from outside: other aggregates hold the root's ID (`OrderId`), not a reference to the whole graph, which keeps aggregate graphs small and loadable. Second, one transaction per aggregate: commit changes to `Order` or to `Invoice`, never both in one transaction; everything else propagates via domain events eventually (see [[How does an aggregate persist and publish events without a distributed transaction]]). Third, small boundaries: an aggregate spanning dozens of objects becomes a serialization bottleneck - every writer contends on the root. The one-aggregate-per-transaction rule is the practical core of aggregate design, at the architecture scale the same concept becomes the unit of service data ownership - [[How do aggregates shape data ownership between services]].

> [!tip] Interview answer
> Entity: identity-defined and stateful over time. Value object: immutable, identity-free, compared by value. Aggregate: a cluster that changes as one consistent unit; the root is the only entry point and enforces invariants across it. Two rules I always mention: reference other aggregates by ID, and one transaction touches one aggregate - cross-aggregate effects go through domain events. The design discipline behind both rules is in [[How do you choose aggregate boundaries]] and [[Why should one transaction update only one aggregate]].
