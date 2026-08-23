<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# Does `NESTED` propagation require JDBC savepoints?

> [!abstract] Short answer
> **For Spring’s usual mapping, yes.** `Propagation.NESTED` keeps **one physical transaction** and marks nested scopes with **savepoints**. Out of the box that means a JDBC `Savepoint` on managers such as `DataSourceTransactionManager`, so the driver (and manager) must support savepoints.

## How Spring maps `NESTED`

When an outer transaction already exists, `NESTED` does **not** open a second independent resource transaction the way [[How does REQUIRES_NEW transaction propagation work]] does. It stays on the same physical transaction and creates a savepoint at the start of the inner scope. If the inner scope fails, Spring can roll back **to that savepoint** and let the outer scope continue. If no transaction exists yet, `NESTED` behaves like `REQUIRED` (start a new physical transaction).

```d2
direction: down
outer: "Outer REQUIRED\nphysical TX open" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
sp: "NESTED begins\ncreate JDBC Savepoint" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
inner: "Inner work\non same Connection" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
ok: "Inner completes\nsavepoint released\nouter continues" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
fail: "Inner fails\nrollback to savepoint\nouter may continue" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}

outer -> sp
sp -> inner
inner -> ok
inner -> fail
```

**Fig. 1.** `NESTED` is one physical transaction plus savepoints, not a second committed transaction.

```java
@Service
public class OrderService {

    @Transactional
    public void placeOrder(Order order) {
        orderRepository.save(order);
        try {
            auditPartial(order); // @Transactional(propagation = NESTED)
        } catch (AuditException ex) {
            // Inner rolled back to its savepoint; outer can still commit
        }
    }

    @Transactional(propagation = Propagation.NESTED)
    public void auditPartial(Order order) {
        auditRepository.save(AuditEntry.from(order));
    }
}
```

**Listing 1.** Conceptual cross-bean call: `NESTED` needs a real Spring proxy boundary; see [[What is the difference between a self-invocation and a cross-bean Transactional call]].

## Which managers actually create savepoints

Spring’s reference docs state that `PROPAGATION_NESTED` is **typically mapped onto JDBC savepoints** and therefore works with **JDBC resource transactions**, pointing at `DataSourceTransactionManager`.

| Manager | Nested / savepoint picture |
| --- | --- |
| `DataSourceTransactionManager` | Supports nested TX via JDBC savepoints; `nestedTransactionAllowed` defaults to **true** (driver must support savepoints). |
| `JpaTransactionManager` / `HibernateTransactionManager` | Can create JDBC savepoints on the underlying connection, but nesting does **not** apply to the JPA/`Session` cache; `nestedTransactionAllowed` often defaults to **false** (version-dependent — Spring Framework 7 aligns JPA default toward **false**). |
| `JtaTransactionManager` | Nested savepoint semantics are **not** available the JDBC way; `PROPAGATION_NESTED` is not supported like on `DataSourceTransactionManager`. |

`Propagation.NESTED`’s own JavaDoc: actual nested creation works only on specific managers; out of the box that is primarily `DataSourceTransactionManager`.

```java
@Transactional(propagation = Propagation.NESTED)
public void nestedWork() {
    // Requires a PlatformTransactionManager that allows nested TX
    // and a JDBC driver that can create Savepoints
}
```

**Listing 2.** Declaring `NESTED` is not enough; the active `PlatformTransactionManager` and driver must support it or Spring throws `NestedTransactionNotSupportedException`.

> [!warning] Outer rollback still undoes nested work
> A successful inner savepoint release does **not** survive an outer rollback. Everything lives in **one** physical transaction: if the outer scope rolls back, nested work that looked “kept” is discarded with it. That is the opposite intuition from [[How does REQUIRES_NEW transaction propagation work]], where the inner physical TX can commit independently.

> [!warning] JPA annotation ≠ JPA nested semantics
> Enabling `nestedTransactionAllowed` on `JpaTransactionManager` only nests at the **JDBC connection** level. JPA entity state / first-level cache does not get true nested-transaction semantics. Prefer `DataSourceTransactionManager` when you need savepoint nesting for plain JDBC, or redesign with `REQUIRES_NEW` when you need an independent commit.

## Adversarial note on “always JDBC”

`AbstractPlatformTransactionManager.useSavepointForNestedTransaction()` defaults to **true** (create a savepoint via `SavepointManager`). A subclass **may** return `false` and attempt a non-savepoint nested begin (the hook meant for JTA-style nesting). In practice, Spring’s JDBC story for `NESTED` **is** savepoints; do not assume every `PlatformTransactionManager` can honor `NESTED`.

> [!tip] Interview answer
> **`NESTED` means one physical transaction with savepoints for partial rollback.** Spring typically implements that with JDBC `Savepoint` on `DataSourceTransactionManager`, so the driver must support savepoints. JTA does not give you that mapping out of the box, and even when a JPA manager can create JDBC savepoints, the EntityManager cache still is not truly nested. Outer rollback still wipes nested work.
