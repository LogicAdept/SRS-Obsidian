<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# When should you use `SUPPORTS` transaction propagation?

> [!abstract] Short answer
> Use **`Propagation.SUPPORTS`** for methods that should **join a caller’s transaction when one exists** but need **no transaction of their own** when called standalone — typically **read-only** queries or reports. Called from a `@Transactional` facade, they participate in that unit of work; called alone, they run non-transactionally without starting a boundary.

## Optional participation, never the starter

`SUPPORTS` fits **read helpers** and idempotent lookups that:

* should see **uncommitted caller changes** when invoked inside a write transaction
* should **not** pay the cost of opening a transaction when invoked directly (CLI, test, or non-transactional entry)

```java
@Service
public class ProductQueryService {

    @Transactional(propagation = Propagation.SUPPORTS, readOnly = true)
    public Product findById(UUID id) {
        return repository.findById(id).orElseThrow();
    }
}

@Service
public class OrderFacade {

    @Transactional
    public void placeOrder(Order order) {
        Product p = products.findById(order.productId()); // joins facade TX
        orders.save(order.withPrice(p.price()));
    }
}
```

**Listing 1.** Conceptual: the same query joins the writer’s transaction or runs bare when called alone. Mechanism: [[How does SUPPORTS transaction propagation work]].

## When not to use it

Do **not** use `SUPPORTS` for **multi-statement writes** that must roll back as one unit when there is **no** outer transaction — standalone calls autocommit statement-by-statement. Use **`REQUIRED`** (default) on the entry service instead.

Do **not** confuse with **`NOT_SUPPORTED`**, which **suspends** an outer TX, or **`NEVER`**, which **throws** if a TX exists — [[What is the difference between SUPPORTS and NOT_SUPPORTED propagation]].

With transaction synchronization enabled, `SUPPORTS` is **not identical** to omitting `@Transactional` — it still defines a scope where the caller’s JDBC connection or Hibernate session may be shared for the method’s duration.

> [!warning] Standalone writes under `SUPPORTS` are not atomic
> A repository `save` loop with `SUPPORTS` and no outer TX has **no** unit-of-work rollback if a later statement fails.

> [!warning] Reads inside a writer still see dirty data
> A `SUPPORTS` read invoked from a `@Transactional` writer participates in that transaction — including uncommitted changes — which is usually what you want for in-facade lookups, not a separate snapshot isolation guarantee.

> [!warning] Self-invocation skips propagation
> `this.findById(...)` from the same class does not apply `SUPPORTS` through the proxy — [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **Use `SUPPORTS` for read-style methods that should join an existing transaction but do not need to start one when called alone.** Do not use it for writes that must be atomic without a caller-owned boundary. For stepping outside an active TX, use `NOT_SUPPORTED`, not `SUPPORTS`.
