<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What happens if `NESTED` is used when no current transaction exists?

> [!abstract] Short answer
> **Spring starts a new physical transaction**, the same as **`REQUIRED`**. No savepoint is created because there is no outer transaction to nest inside. The savepoint path applies only when a current transaction already exists on the thread.

## The `NESTED` fallback rule

`Propagation.NESTED`’s contract (mirrored on `TransactionDefinition.PROPAGATION_NESTED`): execute within a nested transaction **if** a current transaction exists; **behave like `REQUIRED` otherwise**.

So the first `@Transactional(NESTED)` call on a thread with no bound transaction does **not** throw and does **not** open a JDBC savepoint — it becomes the transaction starter.

```d2
direction: down
none: "No TX on thread\n@Transactional(NESTED)" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
required: "Same as REQUIRED\nstart physical TX" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
exists: "Outer TX already active\n@Transactional(NESTED)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
sp: "Create JDBC Savepoint\npartial rollback path" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}

none -> required
exists -> sp
```

**Fig. 1.** Savepoints appear only in the nested-within-existing-TX case.

```java
@Service
public class AuditService {

    @Transactional(propagation = Propagation.NESTED)
    public void recordStandalone(AuditEntry entry) {
        // No outer TX → behaves like REQUIRED; one physical TX for this method
        auditRepository.save(entry);
    }
}

@Service
public class OrderService {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        audit.recordNested(order); // outer TX exists → savepoint semantics
    }
}
```

**Listing 1.** Conceptual: the same `NESTED` annotation follows different paths depending on whether a caller transaction is already active. Full savepoint behavior: [[How does NESTED transaction propagation work]] and [[Does NESTED propagation require JDBC savepoints]].

## Interview trap

Saying “`NESTED` always uses a savepoint” is wrong. Savepoints require **both** `NESTED` propagation **and** an existing physical transaction (plus a manager/driver that supports savepoints). A standalone `NESTED` method is indistinguishable from `REQUIRED` at startup.

Compare [[What is the difference between NESTED and REQUIRED propagation]] — when no outer TX exists, that difference collapses.

> [!warning] Do not confuse with `MANDATORY`
> `MANDATORY` **throws** when no transaction exists. `NESTED` **starts** one instead. See [[How does MANDATORY transaction propagation work]].

> [!warning] Self-invocation still bypasses propagation
> Calling `this.nestedHelper()` from the same class skips the proxy, so neither the savepoint path nor the REQUIRED fallback runs through Spring’s interceptor. Cross-bean calls only — [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **With no current transaction, `NESTED` falls back to `REQUIRED` and opens a normal physical transaction — no savepoint.** Savepoints appear only when an outer transaction is already active. “NESTED always savepoints” misses the standalone entry case.
