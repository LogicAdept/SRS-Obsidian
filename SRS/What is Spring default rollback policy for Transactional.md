<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #Java/Annotations #SRS

# What is Spring default rollback policy for `Transactional`?

> [!abstract] Short answer
> By default Spring rolls back a declarative transaction on **`RuntimeException` and `Error`**, and **commits** if only a **checked exception** leaves the advised method. Override with **`rollbackFor` / `noRollbackFor`** (or class-name patterns). As of Spring **6.2**, you can flip the global default with **`@EnableTransactionManagement(rollbackOn = ALL_EXCEPTIONS)`**.

## Default matches EJB-style “system vs application” exceptions

`@Transactional` javadoc and the Rolling Back a Declarative Transaction reference: with **no custom rollback rules**, the infrastructure marks rollback only for unchecked failures — instances of **`RuntimeException`** (and subclasses) and **`Error`**. Checked exceptions that propagate out of the transactional method do **not** trigger rollback unless you configure them.

That mirrors classic EJB CMT: system exceptions roll back; application (checked) exceptions commit unless customized.

```java
@Service
public class OrderService {

    @Transactional
    public void place(Order order) throws InventoryException {
        orders.save(order);
        if (!stock.reserve(order)) {
            throw new InventoryException("out of stock"); // checked → commit by default
        }
    }

    @Transactional(rollbackFor = InventoryException.class)
    public void placeStrict(Order order) throws InventoryException {
        orders.save(order);
        if (!stock.reserve(order)) {
            throw new InventoryException("out of stock"); // now rolls back
        }
    }

    @Transactional(noRollbackFor = SoftWarningException.class)
    public void placeLenient(Order order) {
        orders.save(order);
        throw new SoftWarningException("warn only"); // RuntimeException but keep commit
    }
}
```

**Listing 1.** Conceptual defaults and overrides from `@Transactional` / reference docs.

```d2
direction: down
leave: "Exception leaves\n@Transactional method" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
rt: "RuntimeException / Error" {
  width: 260
  height: 60
  style.fill: "#ffebee"
}
ch: "Checked Exception" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
rb: "rollback" {
  width: 140
  height: 50
  style.fill: "#ffebee"
}
cm: "commit (default)" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}

leave -> rt -> rb
leave -> ch -> cm
```

**Fig. 1.** Default policy without `rollbackFor` / `noRollbackFor`. Mechanism still requires a working AOP proxy — [[How do you use AOP to manage transactions]].

Customize with type-safe **`rollbackFor` / `noRollbackFor`**, or string patterns **`rollbackForClassName` / `noRollbackForClassName`** (patterns can over-match — prefer class literals). Spring **6.2+**: `@EnableTransactionManagement(rollbackOn = ALL_EXCEPTIONS)` makes **every** exception roll back by default; per-method rules still override for listed types.

Caught-and-swallowed exceptions never reach the interceptor, so they do not apply rollback rules. Nested `REQUIRED` scopes that mark rollback-only can still surprise the outer commit with [[What is UnexpectedRollbackException in Spring REQUIRED propagation]].

> [!warning] Checked exceptions commit by default
> Throwing a domain `Exception` without `rollbackFor` leaves the transaction eligible to **commit**. Interviewers often expect this EJB-legacy default.

> [!warning] Proxy / self-invocation bypasses rollback rules entirely
> Private methods, same-class `this` calls, and non-Spring-managed instances never hit the interceptor — `rollbackFor` cannot help. Fix the call boundary first ([[What is the difference between a self-invocation and a cross-bean Transactional call]]).

> [!warning] Swallowing the exception skips rollback
> `try { … } catch (RuntimeException ex) { log(ex); }` inside the method means the interceptor sees a normal return and may **commit**.

> [!tip] Interview answer
> **Default: roll back on `RuntimeException` and `Error`; commit on checked exceptions.** Use `rollbackFor` / `noRollbackFor` to change that, or Spring 6.2’s `rollbackOn = ALL_EXCEPTIONS` for a global flip. The exception must leave the proxied method — catching it yourself or skipping the proxy leaves the transaction unmarked.
