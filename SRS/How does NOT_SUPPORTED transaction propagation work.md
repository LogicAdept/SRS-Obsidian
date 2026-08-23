<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# How does `NOT_SUPPORTED` transaction propagation work?

> [!abstract] Short answer
> **`Propagation.NOT_SUPPORTED` always executes non-transactionally.** If a transaction is already active, Spring **suspends** it for the duration of the method and **resumes** it afterward. Side effects performed while suspended are **outside** the outer transaction’s rollback scope.

## Suspend, run, resume

Spring’s `TransactionDefinition.PROPAGATION_NOT_SUPPORTED` and `Propagation.NOT_SUPPORTED` both state: do not support a current transaction; **always execute non-transactionally**. When a transaction exists, the transaction manager suspends it, runs the method without transaction synchronization, then resumes the suspended transaction.

Transaction synchronization is **not** available inside a `NOT_SUPPORTED` scope; existing synchronizations are suspended and resumed with the outer transaction.

```d2
direction: down
outer: "Outer @Transactional\nTX active" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
suspend: "NOT_SUPPORTED method\nsuspend outer TX" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
run: "Non-transactional work\n(no TX sync)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
resume: "Resume outer TX\nouter continues" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

outer -> suspend -> run -> resume
```

**Fig. 1.** `NOT_SUPPORTED` temporarily steps out of the caller’s transaction boundary.

```java
@Service
public class OrderFacade {

    @Autowired MetricsClient metrics;

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        metrics.recordLatency(order); // NOT_SUPPORTED below
        payments.charge(order);
    }
}

@Service
public class MetricsClient {

    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void recordLatency(Order order) {
        http.post("/metrics", order.id()); // slow external call without holding DB TX
    }
}
```

**Listing 1.** Conceptual: keep a long external call from extending the database transaction opened by the facade.

## Contrast with `NEVER` and `SUPPORTS`

| Propagation | Transaction already active |
| --- | --- |
| `SUPPORTS` | Join it if present; otherwise run non-transactionally |
| `NOT_SUPPORTED` | **Suspend** it and run non-transactionally |
| `NEVER` | **Throw** `IllegalTransactionStateException` |

See [[How does NEVER transaction propagation work]] and [[How does SUPPORTS transaction propagation work]].

> [!warning] Suspension is not universal
> Actual suspension requires a transaction manager that supports it. **`JtaTransactionManager`** needs access to the Jakarta **`TransactionManager`**, which is server-specific — suspension may not work out of the box. Do not assume `NOT_SUPPORTED` behaves identically on every stack.

> [!warning] Non-transactional side effects may survive outer rollback
> Writes performed while the outer transaction is suspended are **not** rolled back when the resumed outer transaction fails. Use `NOT_SUPPORTED` only when that independence is acceptable (metrics, cache warming, read-only external calls) — not for data that must stay atomic with the business update.

> [!warning] Self-invocation skips suspension semantics
> `this.notSupportedHelper()` from the same class bypasses the proxy, so propagation is not applied. Call through another bean or an injected self-proxy; see [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **`NOT_SUPPORTED` runs without a transaction and suspends any existing one for the call.** When the method returns, the outer transaction resumes. Unlike `NEVER`, it does not throw when a transaction exists — it steps outside it. Side effects during the suspended window are outside the outer rollback.
