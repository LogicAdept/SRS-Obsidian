<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #SRS

# What happens when a non-transactional method calls a `Transactional` method in the same class?

> [!abstract] Short answer
> **No Spring transaction starts for the inner call.** In default **proxy** mode, `this.processItem()` is a direct invoke on the target object, so the `@Transactional` interceptor never runs — even though the inner method is annotated. The same `processItem` **would** run inside a transaction if another bean called it through the proxy.

## Self-invocation bypasses the interceptor

Spring’s `@Transactional` docs: in **proxy** mode, only calls **through the proxy** are intercepted. Self-invocation — a method on the target calling another method on the **same** target — does not create a transaction at runtime, even when the callee carries `@Transactional`.

That applies whether the caller is transactional or not. A **non-transactional** public method that loops `this.processItem()` therefore never opens a per-iteration transaction boundary.

```d2
direction: down
entry: "Client calls\nnon-@Transactional method\nthrough proxy" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
target: "Target instance\n(no TX interceptor yet)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
self: "this.processItem()\nbypasses proxy" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
ignored: "@Transactional on processItem\nignored" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

entry -> target -> self -> ignored
```

**Fig. 1.** The proxy advised the entry method only; internal `this` calls stay inside the raw target.

```java
@Service
public class BatchProcessor {

    public void runBatch(List<Item> items) {
        for (Item item : items) {
            processItem(item); // this.processItem → no TX per item
        }
    }

    @Transactional
    public void processItem(Item item) {
        repository.save(item);
    }
}
```

**Listing 1.** Conceptual: a batch loop expecting per-item rollback will not get it via self-invocation.

```java
@Service
public class OrderFacade {

    @Transactional
    public void placeOrder(Order order) {
        validate(order); // plain helper on same class
        orders.save(order);
    }

    void validate(Order order) {
        // Still executing inside the outer TX that started at placeOrder's proxy entry
    }
}
```

**Listing 2.** Contrast: once a **transactional** method entered through the proxy, a **non-annotated** helper on the same class still runs **inside** that outer transaction — you never left the advised call stack. See [[What happens when one Spring Transactional method calls another]].

## What breaks without a Spring transaction

If `processItem` runs non-transactionally, JDBC/JPA work is not wrapped in a Spring-managed unit of work. Repository calls may **autocommit statement by statement** (depending on connection settings), so a later exception in the loop does **not** roll back earlier iterations.

The fix is the same as for any self-invocation case: extract a bean, inject a self-proxy, use AspectJ mode, or use programmatic demarcation — [[How do you make an inner Transactional method honor its annotation]].

> [!warning] Another bean call is not the same path
> `@Autowired BatchProcessor self; self.processItem(item)` **does** hit the proxy and starts a real transaction (subject to propagation). Interview demos often hide the bug by testing through a controller while production loops with `this`.

> [!warning] Do not blame propagation first
> A missing transaction here is usually **self-invocation**, not wrong `REQUIRED` / `REQUIRES_NEW` settings. Compare [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **A non-transactional method that calls `this.someTransactionalMethod()` does not start a transaction — the inner `@Transactional` is ignored in proxy mode.** JDBC work may autocommit per statement inside a loop. The annotated method works when another Spring bean invokes it through the proxy, not when the same instance calls itself.
