<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What is `UnexpectedRollbackException` in Spring `REQUIRED` propagation?

> [!abstract] Short answer
> **`UnexpectedRollbackException` is thrown when an outer `REQUIRED` scope tries to commit a physical transaction that an inner logical scope already marked rollback-only.** Spring rolls the shared transaction back and throws so the outer caller cannot believe a commit succeeded. It is the classic surprise when you catch an inner exception under nested `REQUIRED` and keep going.

## Logical scopes, one physical transaction

Under `PROPAGATION_REQUIRED`, each advised method gets its own **logical** transaction scope, but nested `REQUIRED` methods map onto the **same physical** transaction. An inner scope that marks rollback-only (typical default: uncaught `RuntimeException` / `Error` leaving the interceptor) therefore dooms the **whole** unit of work.

Spring’s propagation docs: if the outer transaction did not decide on rollback itself, the silent inner rollback-only is **unexpected** for the outer caller who still attempts commit — so Spring throws **`UnexpectedRollbackException`**.

```d2
direction: down
outer: "Outer REQUIRED\nlogical scope A" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
inner: "Inner REQUIRED\nlogical scope B\nsame physical TX" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
mark: "Inner marks\nrollback-only" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}
catch: "Outer catches exception\nand continues" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
commit: "Outer tries commit\n→ UnexpectedRollbackException" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}

outer -> inner -> mark -> catch -> commit
```

**Fig. 1.** Catching the inner failure does not clear rollback-only on the shared physical transaction.

```java
@Service
public class OrderFacade {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        try {
            inventory.reserve(order); // REQUIRED; throws RuntimeException
        } catch (RuntimeException ignored) {
            // business continues — but TX is already rollback-only
        }
        // interceptor commit → UnexpectedRollbackException
    }
}

@Service
public class InventoryService {

    @Transactional // REQUIRED
    public void reserve(Order order) {
        throw new InsufficientStockException(order.sku());
    }
}
```

**Listing 1.** Conceptual cross-bean nested `REQUIRED`: swallowing the exception still leaves the physical transaction rollback-only.

## Not a `REQUIRES_NEW` problem

Independent physical transactions from [[How does REQUIRES_NEW transaction propagation work]] do **not** poison the outer commit this way — the inner rollback stays on the inner TX. `UnexpectedRollbackException` is specifically about **shared** physical transaction + **unexpected** rollback-only for the outer committer.

Programmatic `TransactionStatus.setRollbackOnly()` without rethrowing produces the same outer-commit surprise under `REQUIRED`.

For “catch inner failure and still commit the rest,” use **`NESTED`** savepoints (when supported) rather than nested `REQUIRED` with try/catch — [[What is the difference between NESTED and REQUIRED propagation]].

> [!warning] Catch-and-continue under nested `REQUIRED` is a trap
> Handling the exception in the outer method does **not** rehabilitate the transaction. Expect `UnexpectedRollbackException` at commit time, not a successful commit of the remaining work.

> [!warning] Self-invocation can hide or confuse the story
> If the “inner” method was never advised (`this.reserve()`), there is no separate logical scope marking rollback-only through the interceptor — you may get a different failure mode. Cross-bean `REQUIRED` nesting is the classic path — [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **Under nested `REQUIRED`, one physical transaction is shared. If the inner scope marks it rollback-only and the outer method catches the exception then tries to commit, Spring throws `UnexpectedRollbackException` so you are not lied to about a successful commit.** Fix the design: let the exception propagate, use `NESTED` for partial undo, or `REQUIRES_NEW` for an independent inner boundary — do not catch-and-continue on shared `REQUIRED`.
