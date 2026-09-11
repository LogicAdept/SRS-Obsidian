<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/CQRS #SRS

# What is a command handler in CQRS

> [!abstract] Short answer
> A command handler is the single component registered for one command type: it loads the target aggregate, checks the business invariants the command implies, mutates the aggregate, persists it in one transaction, and publishes the resulting domain events. In the bus style every command maps to exactly one handler — the handler is the write side's public API ([[What is a command in CQRS]] defines the message it receives).

## Responsibilities, in order

The handler is a transaction script around an aggregate, and its steps are strict. Validate the command's shape (required fields, parsed values). Load the aggregate the command targets — or fail with a not-found reply. Enforce invariants: the handler is where "cannot ship an unpaid order" lives, because it sees the aggregate's current truth, not a stale read model. Mutate and persist in one local transaction — the aggregate's own store, not the read models. Publish what happened as events, atomically with the save via the outbox when a broker is involved ([[How does an aggregate persist and publish events without a distributed transaction]]). Handlers stay thin: no orchestration of other services inside one handler — that is a saga's job ([[What is a saga and how would you explain one with a real-world example]]).

```java
class CancelOrderHandler implements CommandHandler<CancelOrder> {
    private final OrderRepository repo;
    private final EventPublisher events;

    public void handle(CancelOrder cmd) {
        Order order = repo.byId(cmd.orderId());          // load current truth
        if (order.status() == OrderStatus.SHIPPED)        // invariant lives here
            throw new IllegalStateException("shipped orders cannot be cancelled");
        order.cancel(cmd.reason());                       // mutate the aggregate
        repo.save(order);                                 // one local transaction
        events.publish(new OrderCancelled(order.id(), cmd.reason()));
    }
}
```

**Listing 1.** Verified on JDK 21 (G01_CqrsCommandBus in empirics): the command bus routes each command type to exactly one handler; the ship handler rejects an order that is not PAID, mutating and publishing only after the check (out/G01_CqrsCommandBus.txt).

## One handler per command — and why

The registry pattern — a map from command class to handler — gives three guarantees. Discoverability: to find what `CancelOrder` does, there is exactly one place to look; no hidden side effects in interceptors or controllers. Testability: the handler is a plain object with injected repositories; unit tests drive it with commands and assert on the aggregate and events, no HTTP or messaging layer needed. Single-writer discipline: two handlers answering for the same invariant would race; the bus makes that mistake unrepresentable. In Richardson's chassis framing, the bus, dispatch and reply plumbing are cross-cutting machinery that belongs in the microservice chassis ([[What is the microservice chassis pattern]]), keeping each handler focused on its invariant. The read side never calls handlers — queries go to projections ([[What is a projection in CQRS and event sourcing]]).

> [!warning] A handler must not assume the command is unique
> Retries, redeliveries and double clicks resend commands. A handler that runs `CancelOrder` twice because the transport redelivered it must end in the same state — reject the second cancel as a no-op or a domain error, never cancel twice. That is the same idempotency discipline as an HTTP API ([[What is idempotency in HTTP and in messaging]]) applied one layer deeper: at the command boundary.

> [!tip] Interview answer
> The command handler is the one component that owns a command type: it loads the aggregate, enforces the invariants, persists the change in one local transaction and publishes the events that describe what happened — atomically with the save via an outbox. One command, one handler keeps the write side discoverable and race-free, and the handler must stay idempotent because retries will replay it.
