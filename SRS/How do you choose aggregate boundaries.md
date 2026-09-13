<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# How do you choose aggregate boundaries?

> [!abstract] Short answer
> Four rules of thumb drive the boundary. Model true invariants inside the boundary - only rules that must hold transactionally belong in one aggregate. Design small aggregates - every oversized cluster costs memory, locks, and contention. Reference other aggregates by identity, never by object navigation. And modify one aggregate instance per transaction, keeping consistency outside the boundary eventual. The unit of reasoning is the invariant, not the object graph.

## Invariants first

The invariant test sorts everything: list the business rules that must be consistent the instant a transaction commits - "order total never exceeds its limit", "a shipment's packages always sum to its manifest weight" - and draw the boundary around exactly the objects those rules touch. Everything else stays out, however natural the composition felt. The classic counterexample: a Product aggregate holding all its backlog items, releases, and sprints. Nothing in the business requires a backlog item's creation to be atomic with a release's scheduling - the coupling was developer convenience, a false invariant. Once split into four aggregates, formerly colliding user operations stop failing each other's transactions, and the model got smaller at the same time ([[Why should one transaction update only one aggregate]]). The classic interview version of the same analysis is the cart-versus-order decision - two lifecycles, two invariant regimes, one domain event at the transition ([[Are a shopping cart and an order one aggregate or two]] works the case end to end).

```java
static final class Order {
    private static final long LIMIT = 10_000;      // true invariant: total <= LIMIT
    private final List<Line> lines = new ArrayList<>();   // children behind the root

    void addLine(long unitPrice, int qty) {
        long candidate = total() + unitPrice * qty;
        if (candidate > LIMIT)
            throw new IllegalStateException("order total would exceed limit: " + candidate);
        lines.add(new Line(unitPrice, qty));
    }
    List<Line> lines() { return Collections.unmodifiableList(lines); }
    long total() { return lines.stream().mapToLong(l -> l.price * l.qty).sum(); }
}
```

**Listing 1.** Verified on JDK 21.0.12.1: adding a 9000-cent line to a 5999-cent order is rejected with "order total would exceed limit: 14999" and the total stays 5999 - the invariant, not the caller, decides what commits; outside mutation of the lines list throws `UnsupportedOperationException`.

```d2
direction: down
inv: "1. Model true invariants\ninside the boundary" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
small: "2. Design small aggregates\nfewer locks, less memory" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
ref: "3. Reference others by identity\nno deep object graphs" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
ec: "4. One aggregate per transaction\neventual consistency outside" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
inv -> small -> ref -> ec
```

**Fig. 1.** The four rules read as a pipeline: invariants define the boundary, smallness keeps it cheap, identity references keep it closed, and the one-transaction rule keeps cross-aggregate effects explicit.

## Smallness and identity references

Small aggregates are a scalability decision with a modeling face. Loading an aggregate should not load a decade of history: thousands of children in one root mean every operation pays for all of them, in memory and in optimistic-concurrency conflicts, because any child's change bumps the root's version. The cure is the identity reference: hold `CustomerId`, not a `Customer` object. The reference documents that the two aggregates are separate consistency units - you cannot accidentally mutate what you cannot navigate to - and it maps directly onto storage and service boundaries ([[How do aggregates shape data ownership between services]]). Cross-aggregate reads happen in the application layer by explicit lookup; cross-aggregate writes happen through domain events and eventual consistency, which is what the fourth rule buys ([[What are aggregate aggregate root entity and value object in DDD]]).

> [!warning] The graph trap
> "Aggregate" tempts people into modeling composition: parent holds children, children hold grandchildren, everything navigable. That is the false-invariant factory - each association argues for atomicity nobody asked for. When a rule seems to require touching two aggregates in one transaction, first suspect a missing concept in the language; a "reservation" or "allocation" object may own the invariant that two big aggregates were straining to fake. The rules are heuristics, not laws - but the burden of proof sits on whoever crosses them.

> [!tip] Interview answer
> I draw the boundary from invariants: rules that must be transactionally consistent define the cluster, everything else stays out. Then keep the aggregate small, reference other aggregates only by id, and modify one aggregate per transaction - cross-aggregate consistency becomes domain events with eventual consistency. If two aggregates truly need atomic updates, the likely bug is a missing concept, not a bigger boundary.

