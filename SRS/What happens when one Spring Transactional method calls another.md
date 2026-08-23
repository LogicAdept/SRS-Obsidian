<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #Java/Annotations #SRS

# What happens when one Spring `Transactional` method calls another?

> [!abstract] Short answer
> **In default proxy mode, a same-class call ignores the inner `@Transactional`.** `outer()` already runs inside the outer interceptor; `this.inner()` hits the target directly, so inner propagation (`REQUIRES_NEW`, `NESTED`, …), isolation, and rollback rules never apply. Work stays in the **outer** physical transaction (or none, if the outer annotation was also bypassed). A **cross-bean** call through the proxy applies the inner attributes normally.

## Same class vs other bean

Spring’s Using `@Transactional` reference: only **external** calls through the proxy are intercepted. Self-invocation — one method on the target calling another on the **same** target — does not start or change a transaction for the callee, even when both methods are annotated.

So two `@Transactional` methods in one class where `A` calls `this.B()`:

* **`B`’s annotation is a no-op** for that call path
* If `A` entered via the proxy with `REQUIRED` (default), `B` runs in **`A`’s** transaction
* `B` with `REQUIRES_NEW` still **does not** suspend/open a new TX on self-call

```java
@Service
public class OrderService {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        this.audit(order); // self-call — REQUIRES_NEW ignored
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void audit(Order order) {
        auditLog.save(AuditEntry.from(order));
    }
}
```

**Listing 1.** Conceptual trap: audit stays in the order transaction and rolls back with it. Contrast [[What is the difference between a self-invocation and a cross-bean Transactional call]].

```d2
direction: down
client: "Client → proxy.placeOrder()" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
outer: "Outer interceptor\nopens REQUIRED TX" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
self: "this.audit()\nskips proxy" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
same: "Still outer TX\nREQUIRES_NEW unused" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

client -> outer -> self -> same
```

**Fig. 1.** Nested annotations only matter when the inner call re-enters through a Spring proxy (or AspectJ weaving).

Fixes when you need the inner boundary: move `audit` to another bean; inject self (`@Lazy` / `ObjectProvider`); or use AspectJ mode so self-calls are woven — [[When should you use AspectJ mode for Transactional self-invocation]], [[How do you make an inner Transactional method honor its annotation]].

The same proxy rule applies during initialization: calling a `@Transactional` method from `@PostConstruct` on the same bean is unreliable because the proxy may not be ready and self-call semantics still apply.

> [!warning] Two annotations ≠ two transactions on `this`
> Interview trap: “`A` and `B` are both `@Transactional`, so two TXs.” On self-invocation you get **at most the outer** interceptor’s transaction.

> [!warning] `REQUIRES_NEW` on the callee does nothing via `this`
> Independent commit for audit/outbox needs a **proxied** call — otherwise outer rollback undoes the “inner” work ([[How does REQUIRES_NEW transaction propagation work]]).

> [!tip] Interview answer
> **Same-class `this` calls bypass the Spring AOP proxy, so the inner `@Transactional` is ignored** — including `REQUIRES_NEW`. Split beans or use AspectJ / self-injection when the callee must have its own transaction semantics. Cross-bean calls through the proxy apply the inner annotation as written.
