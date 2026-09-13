<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# Should commands and events be immutable?

> [!abstract] Short answer
> Events: yes, unconditionally - an event is a fact that already happened, and mutating a recorded fact destroys audit history, breaks replay and projections, and makes the log untrustworthy; event-sourced stores are append-only by design. Commands: immutable is also the right default - a command is a message that gets queued, retried, and inspected, and a mutable command object that changes while in flight produces races and unreproducible failures. In both cases immutability is what makes retries, debugging, and audit legal and cheap. The two message kinds themselves - request versus fact - are compared in [[What is the difference between a command and an event in DDD]].

## Why events are frozen history

An event is written in past tense - `OrderPlaced`, `InvoiceIssued` - and it is the system's record that this occurred. Three consequences follow. Audit and compliance depend on the stream not changing after the fact. Replay must be deterministic: the same events must always rebuild the same state, which dies if an event's payload can change between replays. And consumers subscribe to facts; a silently edited event invalidates every projection built from the earlier version. That is why event-sourced aggregates never update old events - corrections are new events, and deleted data becomes a tombstone event ([[What is snapshotting in event sourcing]]).

```java
public record OrderPlaced(
        UUID orderId,
        CustomerId customer,
        Instant occurredAt,
        List<OrderLineSnapshot> lines) {   // immutable record, no setters
}

public record OrderLineSnapshot(Sku sku, int qty, long unitPriceMinor) { }
```

**Listing 1.** Conceptual. The event carries a snapshot of the data it describes. Note `unitPriceMinor` copied at occurrence time - the event must not join to "current" prices later, because the fact is about the price then.

## Why commands also default to immutable

Commands are intent, not history, so the requirement is softer - but the operational reality argues for freezing them anyway. A command that sits in a queue can be retried after a timeout, dead-lettered, logged, and replayed in a test; if any of those paths can observe a half-mutated command, reasoning about the failure becomes guesswork. Immutable command records make the handler's input a fixed value, which pairs naturally with idempotent handling on retries. The rejection path also stays clean: a refused command does not get edited into success - the refusal produces a separate event or result ([[What is the difference between a command and an event]]).

> [!warning] "Immutability" does not mean "the event payload holds live references"
> An event that carries a mutable object (a `List` someone appends to, or an entity the caller might keep changing) is mutable in practice even if the field is final - shallow immutability is not immutability ([[How would you explain immutable objects and why they matter]]). Serialize snapshots of the data, not references to shared state. The second trap: fixing a wrong event by editing it. Wrong events are corrected with a compensating event, never by rewriting the stream - that is the whole trust model ([[How do you design a Kafka order event pipeline]]).

> [!tip] Interview answer
> Events must be immutable because they are recorded facts: audit, replay, and projections all assume the stream never changes, and corrections arrive as new events. Commands should be immutable by default too - they get queued and retried, and a frozen input makes retries idempotent and failures reproducible. In both cases I model them as records carrying snapshots of data, not references to mutable state.
