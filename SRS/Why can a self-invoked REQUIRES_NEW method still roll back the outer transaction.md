<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #SRS

# Why can a self-invoked REQUIRES_NEW method still roll back the outer transaction?

> [!abstract] Short answer
> **`this.inner()` bypasses the Spring proxy**, so **`@Transactional(propagation = REQUIRES_NEW)` on the inner method is ignored.** The inner work joins the **same physical transaction** as the outer method (if one exists). When the call fails, that **shared** transaction rolls back — including work you expected `REQUIRES_NEW` to have already committed independently (audit rows, per-item refunds).

## The popular lie vs proxy reality

Interview folklore: “`REQUIRES_NEW` always starts a new transaction.” That is true **only when the call enters through the proxy** — another Spring bean, or a self-injected proxy reference.

Default **`@EnableTransactionManagement`** mode is **proxy**. Spring's AOP docs: once execution is inside the target, **`this.method()`** is a plain Java call — **no `TransactionInterceptor`**, so propagation attributes on the callee never apply. Same boundary as [[Why does a self-invocation skip Spring AOP advice]] and [[What is the difference between a self-invocation and a cross-bean Transactional call]].

```java
@Service
public class OrderService {

    @Transactional // REQUIRED — physical TX starts here
    public void placeBatch(List<Order> orders) {
        for (Order order : orders) {
            this.placeOne(order); // REQUIRES_NEW ignored
        }
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void placeOne(Order order) {
        orders.save(order);
        if (order.isBad()) {
            throw new IllegalStateException("bad item");
        }
    }
}
```

**Listing 1.** One failure in the loop marks the **outer** transaction rollback-only — every prior `placeOne` that looked “independent” rolls back with it.

```d2
direction: right
outer: "Outer @Transactional\nREQUIRED" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
self: "this.placeOne()\n(no proxy hop)" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
shared: "Same physical TX\nREQUIRES_NEW ignored" {
  width: 200
  height: 60
  style.fill: "#fce4ec"
}
rb: "Inner failure →\nouter rolls back all" {
  width: 200
  height: 60
  style.fill: "#ffcdd2"
}

outer -> self -> shared -> rb
```

**Fig. 1.** Self-invocation collapses “independent” inner work into the outer transaction.

## What changes after a cross-bean call

Move `placeOne` (or an audit helper) to **another `@Service`** and inject it. The call hits the proxy → **`REQUIRES_NEW` suspends the outer TX**, opens a new physical transaction, and can **commit** before the outer resumes. Later outer rollback **does not undo** that committed inner work — the behavior people expect from `REQUIRES_NEW`. See [[How does REQUIRES_NEW transaction propagation work]].

Alternatives: **`@Lazy` self-injection**, AspectJ transaction mode, or `TransactionTemplate` with `PROPAGATION_REQUIRES_NEW` — see [[How do you make an inner Transactional method honor its annotation]].

> [!warning] Loop of self-invoked REQUIRES_NEW is not isolation
> A batch that calls **`this.placeOrder()`** with `REQUIRES_NEW` on `placeOrder` still shares one transaction. **One bad item rolls back every prior item** in that outer scope. Fix the proxy boundary first; only then reason about pool size and same-row locks ([[Why can REQUIRES_NEW exhaust the connection pool]], [[Why can REQUIRES_NEW deadlock when inner and outer touch the same rows]]).

> [!tip] Interview answer
> REQUIRES_NEW only applies when the call goes through the Spring proxy. this.inner() skips the interceptor, so the inner method stays in the outer physical transaction and its failure rolls everything back. Move the method to another bean (or self-inject the proxy) if you need a truly independent commit.
