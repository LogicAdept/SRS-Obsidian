<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# When should you use `MANDATORY` transaction propagation?

> [!abstract] Short answer
> Use **`Propagation.MANDATORY`** on **internal helpers** that must run **only inside a caller-owned transaction** and should **fail fast** if no transaction is active — for example outbox writes, invariant checks, or audit rows that must commit or roll back with the business update. It **does not** start a transaction; the facade (or entry point) must already open the boundary.

## Guard helpers that must stay atomic with the caller

`MANDATORY` means: support a current transaction; **throw if none exists** (`IllegalTransactionStateException`). It is a **contract enforcement** propagation, not a way to create a unit of work.

Good fits:

* **Outbox / event staging** that must not run standalone
* **Audit or ledger rows** that must share the caller’s commit/rollback
* **Repository-style helpers** in a layered design where only facades own `@Transactional(REQUIRED)`

```java
@Service
public class OrderFacade {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        outbox.enqueue(OrderPlaced.from(order)); // MANDATORY helper
    }
}

@Service
public class OutboxService {

    @Transactional(propagation = Propagation.MANDATORY)
    public void enqueue(OutboxEvent event) {
        outboxRepository.save(event);
    }
}
```

**Listing 1.** Conceptual cross-bean call: the facade owns the transaction; the helper refuses to run without it. Mechanism: [[How does MANDATORY transaction propagation work]].

```d2
direction: down
ok: "Facade @Transactional\nhelper MANDATORY joins" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
bad: "Direct outbox.enqueue()\nno active TX" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
ex: "IllegalTransactionStateException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

ok -> bad -> ex
```

**Fig. 1.** `MANDATORY` turns “called outside a transaction” into an immediate failure instead of silent non-transactional work.

## When not to use it

Do **not** use `MANDATORY` to compensate for a **missing `@Transactional`** on the facade — it **detects** the bug; it does **not** fix it. Default `REQUIRED` on the entry service is still required.

Do **not** expect enforcement from **`this.helper()`** on the same class — the proxy is bypassed. Only **cross-bean** calls apply `MANDATORY`; see [[What is the difference between a self-invocation and a cross-bean Transactional call]].

If the method should run **without** a transaction when none exists but **must not** join when one exists, that is **`NEVER`**, not `MANDATORY` — [[What is the difference between MANDATORY and NEVER propagation]].

If you need to **step out** of the caller’s transaction without throwing, use **`NOT_SUPPORTED`** (suspend), not `MANDATORY`.

> [!warning] `MANDATORY` is not `REQUIRED`
> `REQUIRED` **creates** a transaction when none exists. `MANDATORY` **throws**. Do not mark a standalone REST-facing service `MANDATORY` unless every entry path already opens a transaction.

> [!warning] Rare compared with `REQUIRED` / `REQUIRES_NEW`
> Reach for `MANDATORY` when accidental non-transactional invocation is a **design bug** you want to catch in tests, not as a default for all repository methods.

> [!tip] Interview answer
> **Use `MANDATORY` on internal helpers that must only run inside an existing transaction — outbox, audit, invariants — so calling them with no TX throws immediately.** The facade still needs `@Transactional`. Invoke through another bean; `this`-calls skip the guard.
