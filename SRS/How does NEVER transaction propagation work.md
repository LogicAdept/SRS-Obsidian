<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# How does `NEVER` transaction propagation work?

> [!abstract] Short answer
> **`Propagation.NEVER` runs the method non-transactionally** and **refuses to run inside an existing transaction.** If a transaction is already active on the thread when the advised method is entered, Spring throws **`IllegalTransactionStateException`**. It is a strict guard, not a way to start or join a transaction.

## Guard semantics

Spring’s `TransactionDefinition.PROPAGATION_NEVER` and `Propagation.NEVER` both say: do not support a current transaction; **throw an exception if a current transaction exists**. Transaction synchronization is **not** available inside a `NEVER` scope.

That makes `NEVER` the mirror of [[How does MANDATORY transaction propagation work]]:

| Propagation | Active transaction present? | No active transaction |
| --- | --- | --- |
| `MANDATORY` | Join it | Throw |
| `NEVER` | Throw | Run non-transactionally |

```d2
direction: down
ok: "No TX on thread\nNEVER method runs\nnon-transactionally" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
bad: "Outer @Transactional active\nNEVER method invoked" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
ex: "IllegalTransactionStateException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

bad -> ex
```

**Fig. 1.** `NEVER` fails fast when called inside an existing transaction boundary.

```java
@Service
public class ReportingService {

    @Transactional(propagation = Propagation.NEVER)
    public ReportSnapshot buildSnapshot(UUID tenantId) {
        // Must not participate in a caller's JDBC/JPA transaction
        return jdbc.queryForObject("select ...", ReportSnapshot.class, tenantId);
    }
}

@Service
public class OrderFacade {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        reporting.buildSnapshot(order.tenantId()); // → IllegalTransactionStateException
    }
}
```

**Listing 1.** Conceptual: `NEVER` protects code that must not inherit the caller’s transactional resources.

## `NEVER` versus `NOT_SUPPORTED`

Both end up executing **without** joining the surrounding transaction, but the reaction to an **existing** transaction differs:

| Propagation | Transaction already active |
| --- | --- |
| `NOT_SUPPORTED` | **Suspends** the current transaction and runs non-transactionally |
| `NEVER` | **Throws** `IllegalTransactionStateException` |

Most production code that needs “run outside the caller’s TX” chooses **`NOT_SUPPORTED`** (suspend) rather than **`NEVER`** (fail). Reserve `NEVER` when accidentally entering a transaction is a **bug** you want to detect immediately — for example a read-only report helper that must never enlist in a write transaction.

> [!warning] Self-invocation hides `NEVER`
> Calling `this.neverMethod()` from a `@Transactional` method on the **same** class bypasses the proxy, so the `NEVER` check never runs and no exception appears. Only a **cross-bean** proxied call enforces propagation — see [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!warning] Rare in everyday services
> `NEVER` is uncommon compared with `REQUIRED`, `REQUIRES_NEW`, or `NOT_SUPPORTED`. Reaching for it in an interview usually means explaining a **deliberate guard**, not a default choice.

> [!tip] Interview answer
> **`NEVER` means “this method must not run inside a transaction.”** With no active transaction it executes non-transactionally; if a transaction exists, Spring throws `IllegalTransactionStateException`. Unlike `NOT_SUPPORTED`, it does not suspend the outer transaction — it rejects the call. Invoke it through the proxy, not with `this`.
