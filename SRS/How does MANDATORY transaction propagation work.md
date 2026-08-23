<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# How does `MANDATORY` transaction propagation work?

> [!abstract] Short answer
> **`Propagation.MANDATORY` joins an existing transaction and never starts one.** If no transaction is active on the thread when the advised method runs, Spring throws **`IllegalTransactionStateException`**. Use it on helpers that must stay atomic with a caller that already opened the transaction boundary.

## Behavior compared with `REQUIRED`

Both propagation values **participate** when a transaction already exists. The difference is what happens when **none** exists:

| Propagation | No active transaction |
| --- | --- |
| `REQUIRED` (default) | Creates a new physical transaction |
| `MANDATORY` | Throws `IllegalTransactionStateException` |

Spring’s `TransactionDefinition.PROPAGATION_MANDATORY` and `Propagation.MANDATORY` both state: support a current transaction; **throw an exception if none exists**. Transaction synchronization inside a `MANDATORY` scope is driven by the **surrounding** transaction.

```d2
direction: down
caller: "Caller with @Transactional\n(REQUIRED or outer TX)" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
helper: "Helper @Transactional\n(MANDATORY)" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
same: "Same physical TX\nshared commit/rollback" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
alone: "Helper called with no TX" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
ex: "IllegalTransactionStateException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

caller -> helper -> same
alone -> ex
```

**Fig. 1.** `MANDATORY` is a guard that refuses to become the transaction starter.

```java
@Service
public class OrderFacade {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        outbox.enqueue(order); // MANDATORY helper below
    }
}

@Service
public class OutboxService {

    @Transactional(propagation = Propagation.MANDATORY)
    public void enqueue(Order order) {
        outboxRepository.save(OutboxEvent.from(order));
    }
}
```

**Listing 1.** Conceptual: the facade owns the boundary; the outbox helper insists on joining it.

```java
@RestController
public class OrderController {

    @Autowired OrderFacade orders;

    @PostMapping("/orders")
    public void create(@RequestBody Order order) {
        orders.placeOrder(order); // facade starts REQUIRED TX → MANDATORY succeeds
    }
}

// Direct call with no outer @Transactional:
outbox.enqueue(order); // → IllegalTransactionStateException
```

**Listing 2.** Conceptual: without an active transaction, `MANDATORY` fails fast instead of silently running non-transactionally (contrast [[How does SUPPORTS transaction propagation work]]).

## What the exception means

`IllegalTransactionStateException` is thrown when the **existence or non-existence** of a transaction is illegal for the configured propagation. For `MANDATORY`, Spring reports that no existing transaction was found for a mandatory-marked transaction (the message you see in logs and tests).

That makes `MANDATORY` useful for **internal APIs** that must not run outside a caller’s unit of work — for example outbox writes, invariant checks, or audit rows that must commit or roll back with the business update. It does **not** fix a forgotten `@Transactional` on the facade; it only **detects** the missing boundary loudly.

> [!warning] `MANDATORY` is not the opposite of `REQUIRES_NEW`
> `REQUIRES_NEW` always opens a **separate** physical transaction. The throw-if-wrong-state pair is **`MANDATORY` versus `NEVER`**: `NEVER` throws when a transaction **does** exist. See [[What is the difference between MANDATORY and NEVER propagation]].

> [!warning] Self-invocation skips the mandatory check
> `this.mandatoryHelper()` on the same class bypasses the Spring proxy, so `@Transactional(MANDATORY)` never runs and no mandatory validation occurs. The helper must be invoked through a **cross-bean** proxy call — same rule as [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **`MANDATORY` means “I only run inside someone else’s transaction.”** Spring joins the current physical transaction when one exists; otherwise it throws `IllegalTransactionStateException`. Unlike `REQUIRED`, it never creates a transaction. Pair it with a `@Transactional` facade, and call it through the proxy — not via `this`.
