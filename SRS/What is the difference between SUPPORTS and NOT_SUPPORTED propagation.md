<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What is the difference between `SUPPORTS` and `NOT_SUPPORTED` propagation?

> [!abstract] Short answer
> **`SUPPORTS` joins a current transaction when one exists; otherwise it runs non-transactionally.** **`NOT_SUPPORTED` never participates** — it **suspends** any active transaction and always runs non-transactionally. Both avoid **starting** a transaction; the difference is whether an existing outer transaction is **joined** or **suspended**.

## Optional join vs forced non-transactional

| | Transaction already active | No active transaction |
| --- | --- | --- |
| **`SUPPORTS`** | **Join** outer physical TX | Run **non-transactionally** |
| **`NOT_SUPPORTED`** | **Suspend** outer TX; run non-transactionally | Run **non-transactionally** |

Spring’s definitions:

* `PROPAGATION_SUPPORTS` — support a current transaction; execute non-transactionally if none exists.
* `PROPAGATION_NOT_SUPPORTED` — do not support a current transaction; **rather always execute non-transactionally** (suspending an existing one when present).

```d2
direction: down
supports: "SUPPORTS + outer TX\njoin same TX" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
notSup: "NOT_SUPPORTED + outer TX\nsuspend outer TX" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
alone: "No outer TX\nboth non-transactional" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

supports -> alone
notSup -> alone
```

**Fig. 1.** With no outer transaction the paths converge; with one active they diverge (join vs suspend).

```java
@Service
public class OrderFacade {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        products.findById(order.productId());   // SUPPORTS → joins facade TX
        metrics.recordLatency(order.id());      // NOT_SUPPORTED → suspends facade TX
        payments.charge(order);
    }
}
```

**Listing 1.** Conceptual: `SUPPORTS` read sees the same uncommitted unit of work as the writer; `NOT_SUPPORTED` work runs outside that JDBC/JPA transaction while the outer TX waits suspended.

## Choosing between them

Use **`SUPPORTS`** for read helpers that should participate when the caller already opened a transaction but need no boundary when called alone — [[How does SUPPORTS transaction propagation work]].

Use **`NOT_SUPPORTED`** when code must **not** enlist in the caller’s transaction — long external I/O, cache warming, or anything that should not hold the database transaction open — [[How does NOT_SUPPORTED transaction propagation work]].

If an **active transaction must be rejected** rather than suspended, use **`NEVER`** — [[What is the difference between MANDATORY and NEVER propagation]].

> [!warning] `NOT_SUPPORTED`, not `SUPPORTS`, suspends
> Only **`NOT_SUPPORTED`** (and propagation values that start new TXs like `REQUIRES_NEW`) suspend the outer transaction. **`SUPPORTS` does not suspend** — it joins when a transaction exists.

> [!warning] Side effects under `NOT_SUPPORTED` may survive outer rollback
> Work done while the outer transaction is suspended commits outside that unit of work (for example autocommit JDBC). Outer failure after resume does not roll back those side effects.

> [!warning] Proxy-only semantics
> Same-class `this` calls skip propagation for both values — [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **`SUPPORTS` joins an existing transaction or runs without one. `NOT_SUPPORTED` always runs non-transactionally and suspends any active outer transaction first.** Neither starts a transaction. Use `SUPPORTS` for optional participation; use `NOT_SUPPORTED` to step out of the caller’s TX without throwing like `NEVER`.
