<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is a domain event in DDD?

> [!abstract] Short answer
> A domain event is a record of a domain-significant occurrence, named in past tense - OrderPlaced, InvoiceIssued - immutable once created, and recorded by the aggregate at the moment its state changes. It is vocabulary before it is machinery: the event exists because the business says "an order was placed", and the model now says the same. Delivery happens after the transaction commits; handlers react in their own transactions.

## Recording and dispatching

The aggregate owns its events. A state change that matters to the business registers the fact alongside the mutation - `place()` sets status to PLACED and records OrderPlaced with the ids and totals it implies. The aggregate neither publishes nor knows the subscribers; it collects. The application layer, after the transaction commits, pulls the recorded events and hands them to a dispatcher. Two consequences fall out. First, no phantom facts: an event can never describe a change that was rolled back, because it leaves the aggregate only after the commit. Second, exactly-once visibility per transaction: the pull drains the buffer, so a retried use case re-records rather than re-publishes stale facts. When the broker must also survive a crash between commit and publish, the recorded-events buffer graduates into a transactional outbox row - same concept, durable storage ([[How would you explain the transactional outbox pattern]]).

```java
static abstract class Aggregate {
    private final List<Object> recordedEvents = new ArrayList<>();
    protected void register(Object event) { recordedEvents.add(event); }
    List<Object> pullEvents() { List<Object> out = List.copyOf(recordedEvents); recordedEvents.clear(); return out; }
}

order.place(42);
List<Object> delivered = order.pullEvents();
System.out.println(delivered);   // [OrderPlaced[orderId=77, customerId=42, totalCents=0]]
order.cancel("customer request");
System.out.println(order.pullEvents());   // [OrderCancelled[orderId=77, reason=customer request]]
System.out.println(order.pullEvents().isEmpty());   // true - drained
```

**Listing 1.** Verified on JDK 21.0.12.1: events are named in past tense, emerge only after the (simulated) commit, batch per transaction, and drain exactly once - the third pull is empty.

```d2
direction: right
agg: "Aggregate\nmutates state,\nrecords event" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
commit: "Transaction commit" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
disp: "Dispatcher\npulls recorded events" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
h1: "Local handler\nprojection, policy" {
  width: 220
  height: 80
  style.fill: "#f3e5f5"
}
h2: "Integration event\nother contexts" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
agg -> commit
commit -> disp: "after commit"
disp -> h1
disp -> h2
```

**Fig. 1.** The chain has a hard gate: nothing leaves the aggregate before the commit, and what leaves is a past-tense fact, not a request.

## Internal facts vs integration messages

A domain event starts life inside one bounded context - it coordinates projections, policies, and other aggregates there ([[Why should one transaction update only one aggregate]]). When a fact also matters to other contexts, it travels outward as an integration event through the messaging infrastructure, translated at the boundary into each consumer's language ([[What is the domain event pattern in microservices]] covers that outward face). Keeping the two roles distinct matters: internal events may carry fine-grained model details; integration events are a published contract that evolves slowly and deliberately ([[What are the open host service and published language patterns]]). The modeling payoff is the same at both scales - history becomes a first-class part of the language, and temporal logic ("when the invoice was issued") gets a concrete object to live in. Event sourcing is the far end of the same idea, where the recorded facts become the primary store ([[What is snapshotting in event sourcing]] names its one big cost and cure).

> [!warning] A fact is not a command in costume
> Two inversions ruin the pattern. Publishing before commit promises facts that rollback un-happens. And "events" addressed to a specific service with an expectation it will run - those are commands wearing past-tense names; the consumer's autonomy dies the same way it would with a direct call ([[Can you send a command or publish an event across bounded contexts]] contrasts the two). If the emitter requires a particular reaction, it must say so in imperative voice and accept rejection.

> [!tip] Interview answer
> A domain event is an immutable, past-tense fact recorded by the aggregate when its state changes - OrderPlaced, not PlaceOrder. The aggregate buffers it, the application layer publishes after commit, and handlers react in their own transactions, which is how cross-aggregate consistency becomes eventual. Inside a context they drive projections and policies; across contexts they graduate to translated integration events.

