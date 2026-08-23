<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# How does `NESTED` transaction propagation work?

> [!abstract] Short answer
> When a transaction **already exists**, `Propagation.NESTED` stays on the **same physical transaction** and opens a **JDBC savepoint** for the inner scope. Inner failure rolls back **to that savepoint** so the outer method may continue; outer failure still rolls back **everything**, including nested work. With **no** active transaction, `NESTED` behaves like `REQUIRED` and starts one.

## One physical transaction, partial rollback

`NESTED` is not a second committed transaction. Spring’s reference docs describe it as a single physical transaction with savepoints you can roll back to. That differs from [[How does REQUIRES_NEW transaction propagation work]], where the inner scope gets its **own** physical transaction that can commit before the outer method finishes.

```d2
direction: down
outer: "Outer @Transactional\nphysical TX" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
sp: "Inner NESTED\nJDBC Savepoint" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
ok: "Inner succeeds\nrelease savepoint\nouter continues" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
fail: "Inner throws\nrollback to savepoint\nouter may catch & continue" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
outerFail: "Outer rolls back later\nnested work undone too" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}

outer -> sp
sp -> ok
sp -> fail
outer -> outerFail
```

**Fig. 1.** Savepoints allow partial undo inside one commit boundary; they do not survive an outer rollback.

## When no transaction exists yet

`Propagation.NESTED`’s contract: execute within a nested transaction **if** a current transaction exists; otherwise behave like `REQUIRED`. The first `@Transactional(NESTED)` call on a thread with no bound transaction therefore **starts** a new physical transaction rather than throwing.

```java
@Service
public class OrderService {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        try {
            audit.tryRecord(order); // NESTED in AuditService
        } catch (AuditException ex) {
            // Inner rolled back to savepoint; order insert still in outer TX
        }
    }
}

@Service
public class AuditService {

    @Transactional(propagation = Propagation.NESTED)
    public void tryRecord(Order order) {
        auditRepository.save(AuditEntry.from(order));
        if (!deliverable(order)) {
            throw new AuditException("bad audit payload");
        }
    }
}
```

**Listing 1.** Conceptual cross-bean setup. `this.tryRecord(...)` would not honor `NESTED`; see [[What is the difference between a self-invocation and a cross-bean Transactional call]].

## Platform support

Spring maps `NESTED` onto **JDBC savepoints** for JDBC resource transactions — primarily `DataSourceTransactionManager` with a driver that supports savepoints. See [[Does NESTED propagation require JDBC savepoints]] for the manager/driver requirements.

`JtaTransactionManager` does **not** provide the same nested savepoint semantics out of the box. `JpaTransactionManager` / `HibernateTransactionManager` may create JDBC savepoints on the connection when `nestedTransactionAllowed` is enabled, but JPA/Hibernate session state does **not** get true nested-transaction semantics.

> [!warning] Inner “success” does not commit independently
> Only **`REQUIRES_NEW`** can commit inner work while the outer transaction is still open. With `NESTED`, nested changes live inside the outer physical transaction until the **outer** commits. If the outer later rolls back, nested rows disappear even if the inner scope completed without error.

> [!warning] Do not confuse `NESTED` with `REQUIRES_NEW`
> Interview shorthand: **`NESTED` = savepoint inside one TX**; **`REQUIRES_NEW` = suspend outer, new TX, independent commit/rollback**. Compare [[What is the difference between NESTED and REQUIRES_NEW propagation]].

> [!tip] Interview answer
> **`NESTED` uses one physical transaction plus JDBC savepoints for partial rollback.** If there is no current transaction it acts like `REQUIRED`. Inner failure can roll back to the savepoint while the outer method continues, but an outer rollback still undoes nested work. It is not an independent commit — that is `REQUIRES_NEW`.
