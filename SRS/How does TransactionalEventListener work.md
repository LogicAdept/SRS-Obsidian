<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #Java/Annotations #SRS

# How does `TransactionalEventListener` work?

> [!abstract] Short answer
> **`@TransactionalEventListener`** registers a listener that runs only at a chosen **transaction phase** — default **`AFTER_COMMIT`**. The handler sees the outcome of the transaction that was active when the event was **published**, so side effects like email or messaging can wait until DB work actually commits.

## Transaction phase binding

Since Spring 4.2, an event listener can be tied to a phase of the **publisher’s** transaction instead of firing immediately like `@EventListener`.

`@TransactionalEventListener` defaults to **`TransactionPhase.AFTER_COMMIT`**. The `phase` attribute also accepts **`BEFORE_COMMIT`**, **`AFTER_ROLLBACK`**, and **`AFTER_COMPLETION`** (commit or rollback).

Spring Framework reference: if **no transaction is running** when the event is published, the listener is **not invoked**, because the phase semantics cannot be honored. Set **`fallbackExecution = true`** to run anyway (same timing as a plain `@EventListener`).

```java
@Service
public class OrderService {

    private final ApplicationEventPublisher events;

    @Transactional
    public Order placeOrder(OrderRequest request) {
        Order order = orders.save(buildOrder(request));
        events.publishEvent(new OrderCreatedEvent(order));
        return order;
    }
}

@Component
public class OrderNotifications {

    @TransactionalEventListener
    public void onOrderCreated(OrderCreatedEvent event) {
        mailer.sendConfirmation(event.order());
    }
}
```

**Listing 1.** Conceptual pattern from Spring Framework reference — notification runs only after the publishing `@Transactional` method’s transaction commits.

```d2
direction: right
pub: "@Transactional\npublisher" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
evt: "publishEvent\n(in TX)" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
commit: "TX commits" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}
listen: "@TransactionalEventListener\nAFTER_COMMIT" {
  width: 280
  height: 80
  style.fill: "#fce4ec"
}

pub -> evt -> commit -> listen
```

**Fig. 1.** The listener is deferred until commit; if the transaction rolls back, an `AFTER_COMMIT` handler never runs.

The publisher must expose a real transaction boundary — typically `@Transactional` on the method that calls `publishEvent` — so Spring can register the listener against that transaction. That is the same declarative demarcation described in [[How do you use AOP to manage transactions]].

Events still flow through the application event multicaster described in [[How does ApplicationContext publish events]]; `@TransactionalEventListener` only changes **when** the handler runs relative to the active transaction.

> [!warning] No transaction means no listener (by default)
> Publishing outside any transaction skips `@TransactionalEventListener` handlers unless `fallbackExecution = true`. A forgotten `@Transactional` on the publisher looks like a “broken” listener.

> [!warning] `AFTER_COMMIT` is not a distributed guarantee
> The listener runs after the local transaction commits. Cross-service delivery still needs idempotency, retries, or an outbox if the process crashes after commit but before the side effect finishes.

> [!warning] Rollback-sensitive work needs the right phase
> Use **`AFTER_ROLLBACK`** or **`AFTER_COMPLETION`** when the handler must react to failure, not **`AFTER_COMMIT`**.

> [!tip] Interview answer
> **`@TransactionalEventListener` delays handling until a transaction phase — default after successful commit.** Publish the event inside a `@Transactional` method so Spring knows which transaction to bind. If the DB rolls back, an `AFTER_COMMIT` listener never fires, which keeps notifications aligned with persisted state.
