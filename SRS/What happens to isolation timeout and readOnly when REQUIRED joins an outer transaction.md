<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What happens to isolation, timeout, and readOnly when `REQUIRED` joins an outer transaction?

> [!abstract] Short answer
> **The outer transaction’s settings win.** When `REQUIRED` participates in an existing physical transaction, Spring **silently ignores** the inner method’s `isolation`, `timeout`, and `readOnly` attributes by default. Only propagation values that **start a new** physical transaction — notably `REQUIRES_NEW` — can apply their own isolation, timeout, and read-only flags.

## Participating join inherits the outer scope

Spring’s propagation reference for `PROPAGATION_REQUIRED` states that a participating transaction **joins the characteristics of the outer scope**, ignoring local isolation, timeout, and read-only declarations unless you configure the transaction manager otherwise.

`TransactionDefinition` also notes that **isolation** and **timeout** apply only when a **new** transaction is actually started — which, for joining behavior, means `REQUIRED` on an existing TX does not re-apply those attributes.

```d2
direction: down
outer: "Outer @Transactional\nisolation=READ_COMMITTED\nreadOnly=false" {
  width: 320
  height: 90
  style.fill: "#e3f2fd"
}
inner: "Inner REQUIRED join\nisolation=SERIALIZABLE\nreadOnly=true" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
result: "Shared physical TX\nouter settings effective\ninner attrs ignored" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}

outer -> inner -> result
```

**Fig. 1.** Nested `REQUIRED` scopes share one physical transaction and one set of resource characteristics.

```java
@Service
public class OrderFacade {

    @Transactional(isolation = Isolation.READ_COMMITTED, readOnly = false)
    public void placeOrder(Order order) {
        orders.save(order);
        reports.summary(order.id()); // inner REQUIRED below
    }
}

@Repository
public class ReportRepository {

    @Transactional(propagation = Propagation.REQUIRED,
                   isolation = Isolation.SERIALIZABLE,
                   readOnly = true,
                   timeout = 5)
    public OrderSummary summary(UUID orderId) {
        return jdbc.queryForObject("select ...", OrderSummary.class, orderId);
    }
}
```

**Listing 1.** Conceptual: inner `SERIALIZABLE`, `readOnly=true`, and `timeout=5` do **not** upgrade or narrow the shared transaction — the outer `READ_COMMITTED` read-write TX remains in force.

## Strict mode: `validateExistingTransaction`

Set **`validateExistingTransaction`** to **`true`** on the `PlatformTransactionManager` if mismatches should **fail** instead of being ignored. In that non-lenient mode Spring rejects participating in an existing transaction when isolation differs, and also rejects read-only mismatches (for example an inner read-write `REQUIRED` joining a read-only outer scope).

## Contrast with `REQUIRES_NEW`

`PROPAGATION_REQUIRES_NEW` opens an independent physical transaction that **can** declare its own isolation, timeout, and read-only settings instead of inheriting the outer ones — see [[How does REQUIRES_NEW transaction propagation work]].

`NESTED` savepoint semantics still share the **same** physical transaction as the outer scope, so the same inheritance rules apply as for joining `REQUIRED`.

> [!warning] Inner `readOnly=true` does not protect a shared write transaction
> Marking a joining `REQUIRED` repository method `readOnly=true` does **not** make the shared JDBC/JPA transaction read-only. Writes in the outer facade still run in a read-write physical transaction.

> [!warning] Inner isolation is not a per-method upgrade
> `Isolation.SERIALIZABLE` on an inner joining `REQUIRED` method does **not** raise isolation for the whole unit of work. To run at a different isolation level, use a propagation that starts a new physical transaction (typically `REQUIRES_NEW`) or restructure the boundary.

> [!tip] Interview answer
> **When `REQUIRED` joins an outer transaction, isolation, timeout, and readOnly on the inner `@Transactional` are ignored by default — the outer physical transaction’s settings apply.** Turn on `validateExistingTransaction` if you want mismatches to fail. For independent settings, use `REQUIRES_NEW`, not nested `REQUIRED`.
