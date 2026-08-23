<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What is the difference between `REQUIRED` and `REQUIRES_NEW` propagation?

> [!abstract] Short answer
> **`REQUIRED` joins or creates one shared physical transaction** — inner failure typically rolls back the caller too. **`REQUIRES_NEW` suspends the outer transaction and starts a second physical one** that can commit even if the outer later rolls back. Use `REQUIRES_NEW` when inner work must survive outer failure (audit, outbox).

## Shared vs independent physical transactions

| | `REQUIRED` (default) | `REQUIRES_NEW` |
| --- | --- | --- |
| Outer TX exists | **Join** same physical TX | **Suspend** outer; **new** physical TX |
| No outer TX | **Start** one | **Start** one (no suspend) |
| Inner failure | Marks shared TX **rollback-only** | Rolls back **inner only** |
| Inner success before outer fails | Lost on **outer rollback** | **Survives** if inner **committed** |
| Connections (typical JDBC) | **One** | **Two** while inner runs |

Spring’s propagation reference: `REQUIRED` never creates a second independent physical transaction for an outer scope; `REQUIRES_NEW` always does.

```d2
direction: right
req: "REQUIRED\none physical TX" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
new: "REQUIRES_NEW\nouter suspended\ninner commits alone" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
audit: "Audit row\nsurvives outer rollback" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

req -> new
new -> audit
```

**Fig. 1.** `REQUIRES_NEW` is the independent-commit pattern; `REQUIRED` is the default unit-of-work join.

```java
@Service
public class OrderService {

    private final AuditService audit;

    @Transactional // REQUIRED
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

**Listing 1.** Conceptual cross-bean setup — audit can commit while the order transaction rolls back. Test pattern: [[How do you test that REQUIRES_NEW commits independently of the outer transaction]].

## Pitfalls that blur the comparison

Two `@Transactional(REQUIRED)` methods on the **same class** still share the outer transaction when called as `this.inner()` — not because `REQUIRED` “joined correctly,” but because the inner interceptor **never ran**. See [[What is the difference between a self-invocation and a cross-bean Transactional call]].

`REQUIRES_NEW` is **not** a savepoint mechanism — that is `NESTED`. It **does** hold a **second connection** while the outer TX is suspended and can **deadlock** if inner and outer touch the same rows — [[Why can REQUIRES_NEW exhaust the connection pool]] and [[Why can REQUIRES_NEW deadlock when inner and outer touch the same rows]].

Inner `REQUIRES_NEW` invoked via self-call still rolls back with the outer transaction — [[Why can a self-invoked REQUIRES_NEW method still roll back the outer transaction]].

Rollback-only surprises with nested `REQUIRED`: [[What is UnexpectedRollbackException in Spring REQUIRED propagation]].

> [!warning] Do not use `REQUIRES_NEW` for every helper
> The extra connection and suspension cost is real. Default to `REQUIRED`; reach for `REQUIRES_NEW` only when inner persistence must **commit independently** of outer outcome.

> [!tip] Interview answer
> **`REQUIRED` shares one physical transaction — inner and outer succeed or fail together. `REQUIRES_NEW` suspends the outer TX and opens a new one that can commit on its own, so audit/outbox rows can survive an outer rollback.** It needs a proxied cross-bean call, a second connection, and is not the same as `NESTED` savepoints.
