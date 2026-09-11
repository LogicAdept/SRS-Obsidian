<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/CQRS #SRS

# What is a projection in CQRS and event sourcing

> [!abstract] Short answer
> A projection in CQRS and event sourcing is a consumer of domain events that builds and maintains one read model: it applies each event to a denormalized view shaped for a specific query — an order summary, a search index, a report table. Projections are rebuildable: delete the view, replay the event history from the store, and the same code reconstructs it.

## The mechanism: fold events into a view

A projection is a left fold over the event stream. For each event, in order: switch on the event type, apply the state delta to the view, record the position in the stream so the next batch resumes there. Events are immutable facts ([[What is the difference between a command and an event]]), so the fold is deterministic — the same events always produce the same view, which is exactly what makes rebuilds safe. In event-sourced systems the event log is the only source of truth and projections are the only way to query efficiently ([[How would you explain the event sourcing pattern]]); in plain CQRS the read side may be fed by the same events without full event sourcing ([[What is CQRS]]).

```d2
direction: right
log: "Event log
OrderCreated, OrderPaid, OrderShipped" {shape: cylinder; style.fill: "#fffde7"}
p1: "Summary projection
order #7 [paid] [shipped]" {style.fill: "#e3f2fd"}
p2: "Search projection
full-text index" {style.fill: "#e8f5e9"}
p3: "Reporting projection
revenue per day" {style.fill: "#f3e5f5"}
log -> p1: apply in order
log -> p2
log -> p3
```

**Fig. 1.** One log, many projections: each consumer folds the same events into a differently shaped view at its own pace.

## Operational properties that decide the design

Lag and consistency: a projection consumes asynchronously, so its view trails the write side — the UI needs read-your-writes handling for the gap ([[What is eventual consistency]]). Idempotency and ordering: replays and resharding re-deliver events, so applying the same event twice must be a no-op, and events for one aggregate must apply in order ([[What is idempotency in HTTP and in messaging]] for the general discipline). Rebuildability is the safety net: change the read model's shape, deploy the projection with a blank store, replay history — schema migrations on a read side become "re-run the fold" instead of online DDL. Snapshots bound replay cost for the aggregate state itself ([[What is snapshotting in event sourcing]]), while projections can also start from a checkpoint plus recent events.

```java
class OrderSummaryProjection {
    record Summary(int id, String label, double total) {}
    private final Map<Integer, Summary> view = new HashMap<>();

    void apply(OrderEvent e) {
        if (e instanceof OrderCreated c) view.put(c.id(), new Summary(c.id(), "order #" + c.id(), c.total()));
        else if (e instanceof OrderPaid p) {
            Summary s = view.get(p.id());
            view.put(p.id(), new Summary(s.id(), s.label() + " [paid]", s.total()));
        }
    }
}
```

**Listing 1.** Verified on JDK 21 (G01_CqrsCommandBus in empirics): after applying OrderCreated, OrderPaid and OrderShipped in order, the read model answers with `Summary[id=7, label=order #7 [paid] [shipped], total=199.0]` (out/G01_CqrsCommandBus.txt).

> [!warning] A projection is a copy, never the truth
> If the projection's data can also be written by anything else, rebuilds are impossible and the view drifts from the log. The projection must be the only writer of its view, and its event source must be authoritative. Teams that "fix" a broken projection by hand-editing rows have corrupted the fold — the next replay silently reverts the fix.

> [!tip] Interview answer
> A projection is an event consumer that folds domain events, in order, into one denormalized read model — an order summary, a search index, a report table — storing its stream position as a checkpoint. Because events are immutable facts, the fold is deterministic: I can rebuild the view by replaying history. Projections trail the write side, so consumers must be idempotent and the UI must tolerate the consistency gap.
