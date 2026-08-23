<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# How does `REQUIRES_NEW` transaction propagation work?

> [!abstract] Short answer
> **`Propagation.REQUIRES_NEW` always opens a new physical transaction.** If one already exists, Spring **suspends** the outer transaction until the inner method finishes. The inner transaction **commits or rolls back on its own**, independent of the outer outcome — which is why audit/outbox helpers use it.

## Independent physical transaction

Spring’s reference docs state that `REQUIRES_NEW`, unlike `REQUIRED`, **never participates** in an outer scope’s physical transaction. Underlying resource transactions are different, so they can commit or roll back independently. The inner scope may also declare its own isolation, timeout, and read-only settings instead of inheriting the outer ones.

When the outer transaction is suspended, its resources stay bound to it while the inner scope acquires **its own** connection (or equivalent). That is why [[Why can REQUIRES_NEW exhaust the connection pool]] matters under load.

```d2
direction: down
outer: "Outer REQUIRED TX\n(suspended)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
inner: "Inner REQUIRES_NEW TX\nnew connection" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
commit: "Inner commits\nbefore outer returns" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
resume: "Outer resumes\nmay still roll back" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}

outer -> inner -> commit -> resume
```

**Fig. 1.** Inner work can survive an outer rollback because it committed in a separate physical transaction.

```java
@Service
public class OrderService {

    private final AuditService audit;

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        audit.record(order); // REQUIRES_NEW in AuditService
        throw new PaymentException("charge failed");
    }
}

@Service
public class AuditService {

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void record(Order order) {
        auditRepository.save(AuditEntry.from(order));
    }
}
```

**Listing 1.** Conceptual cross-bean call: audit row can remain after the order transaction rolls back. Test pattern: [[How do you test that REQUIRES_NEW commits independently of the outer transaction]].

## Contrast with `NESTED`

| | `REQUIRES_NEW` | `NESTED` |
| --- | --- | --- |
| Physical TX | **New**, independent | **Same**, with savepoint |
| Inner commit before outer ends | **Yes** | **No** — lives in outer TX |
| Outer rollback undoes inner | **No** (if inner committed) | **Yes** |

See [[What is the difference between NESTED and REQUIRES_NEW propagation]] and [[Does NESTED propagation require JDBC savepoints]].

> [!warning] Self-invocation ignores `REQUIRES_NEW`
> `this.record(order)` stays on the outer transaction because the proxy is bypassed. Only a **cross-bean** call (or AspectJ weaving / self-proxy) applies the inner propagation — [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!warning] Two connections while outer is suspended
> The suspended outer transaction keeps its JDBC connection; the inner transaction takes another. Size the pool for concurrent threads plus suspended outers, or risk deadlock — see [[Why can REQUIRES_NEW deadlock when inner and outer touch the same rows]].

> [!warning] JTA suspension is not automatic everywhere
> `Propagation.REQUIRES_NEW` notes that actual suspension may not work out of the box on all managers — especially **`JtaTransactionManager`** without a configured Jakarta `TransactionManager`.

> [!tip] Interview answer
> **`REQUIRES_NEW` suspends any outer transaction and starts a fresh physical one.** The inner scope commits or rolls back independently, so audit or outbox rows can persist even when the caller rolls back. It needs a proxied cross-bean call and costs an extra connection while the outer TX stays suspended.
