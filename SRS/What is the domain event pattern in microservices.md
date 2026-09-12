<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceCollaboration #Patterns/Enterprise/Integration/Messages/EventMessage #SRS

# What is the domain event pattern in microservices

> [!abstract] Short answer
> A domain event is something that happened inside a service's business domain, published so other services can react: OrderCreated, OrderCancelled, CreditReserved. The pattern: structure business logic as DDD aggregates that record these events as their methods run, and have the service publish them reliably after committing - the backbone of choreography and of event-fed read models.

## Mechanism: the aggregate records, the service publishes

The pattern has two halves. Inside the service, business logic is organized as [[What are aggregate aggregate root entity and value object in DDD]]-style aggregates whose behavior methods append events: Order.createOrder() records OrderCreated; Order.cancel() records OrderCancelled. The event names a completed fact in the domain's language - past tense, meaningful to the business, not a table delta. The aggregate collects them in memory; nothing has been published yet. After the aggregate is persisted in the local transaction, the service publishes the drained events so other services consume them. The ordering matters and is the classic interview probe: the event must be announced only if the transaction that produced it commits. That is exactly the dual-write problem the [[How would you explain the transactional outbox pattern]] solves - events go to an outbox table in the same transaction as the entity, and a relay ships them to the broker. My verified micro-case: the aggregate drains events only after save, and the drain clears them so nothing publishes twice (MS02 in empirics).

```d2
direction: right
m: "Order.createOrder()" {style.fill: "#e8f5e9"}
agg: "Order aggregate
records OrderCreated" {style.fill: "#e8f5e9"}
tx: "local transaction
order + outbox rows" {style.fill: "#fff3e0"}
relay: "event relay
(outbox / tailing)" {style.fill: "#ffe0b2"}
broker: "Message broker" {style.fill: "#eceff1"}
others: "Consumer services" {style.fill: "#eceff1"}
m -> agg: business method
agg -> tx: persist together
tx -> relay: committed rows
relay -> broker: publish
broker -> others: deliver
```

**Fig. 1.** Events are born in the aggregate, committed with the business data, and only then released to the broker - never before the transaction commits.
```java
void cancel(long id, String reason) {
    Order o = store.get(id);
    o.cancel(reason);            // aggregate records OrderCancelled
    publish(o);                  // service publishes after save
}
private void publish(Order o) {
    for (Object e : o.drainDomainEvents())
        brokerOut.add("publish: " + e.getClass().getSimpleName() + " -> " + e);
}
```

**Listing 1.** Verified on JDK 21 (MS02_DomainEventEmit in empirics): the aggregate drains clean after save — `publish: OrderCreated -> OrderCreated[orderId=7, customer=Ada]`, `publish: OrderCancelled -> OrderCancelled[orderId=7, reason=out of stock]`, then `order status: CANCELLED` and `unpublished events left on aggregate: 0 (drained)`.


Domain events are the payload of the communication styles: choreography-based sagas chain local transactions by reacting to them, and CQRS projections build read models by consuming them. They differ from commands - "OrderCancelled" says what happened, "CancelOrder" asks something to happen; confusing the two is the message-versus-event trap ([[What is the difference between a command and an event]] separates the vocabulary). Within a process, Spring's application events or CDI events can deliver the same aggregate-recorded events to local listeners - the pattern is about the reliable cross-service publication, which is what the outbox adds ([[How does an aggregate persist and publish events without a distributed transaction]] walks that persistence path).

> [!warning] Publishing before commit invents facts
> The classic bug: a listener or interceptor fires the event at method-call time - before the transaction commits - and a consumer on another machine reacts to an order the transaction then rolls back. The event announced a fact that never happened, and the consumers' compensations are ugly to write. The second trap: anemic "CRUD events" - OrderUpdated with a field dump. Nobody downstream can build business logic on those; events should carry domain meaning (which fields changed why), or consumers end up diffing snapshots.

> [!tip] Interview answer
> A domain event is a past-tense business fact - OrderCreated, CreditReserved - recorded by a DDD aggregate as its methods run and published by the service after the local transaction commits. Aggregates generate the events; the transactional outbox makes publication atomic with persistence; choreography sagas and CQRS projections are the main consumers. Never publish before commit, and name events in domain language, not as CRUD deltas.
