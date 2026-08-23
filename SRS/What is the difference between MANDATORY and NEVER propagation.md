<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What is the difference between `MANDATORY` and `NEVER` propagation?

> [!abstract] Short answer
> **`MANDATORY` and `NEVER` are opposite guards on transaction presence.** `MANDATORY` **requires** an active transaction and throws if none exists. `NEVER` **forbids** an active transaction and throws if one exists. Neither propagation value **creates** a new transaction.

## Mirror guards

Both map to EJB-style “support current transaction, but fail if the state is wrong” semantics — they enforce preconditions rather than opening boundaries.

| | Active transaction present | No active transaction |
| --- | --- | --- |
| **`MANDATORY`** | Join it | Throw `IllegalTransactionStateException` |
| **`NEVER`** | Throw `IllegalTransactionStateException` | Run **non-transactionally** |

Spring’s `Propagation.MANDATORY` / `TransactionDefinition.PROPAGATION_MANDATORY`: support a current transaction; throw if none exists.

Spring’s `Propagation.NEVER` / `TransactionDefinition.PROPAGATION_NEVER`: do not support a current transaction; throw if one exists. Transaction synchronization is not available inside a `NEVER` scope.

```d2
direction: right
mandatory: "MANDATORY\nneeds TX" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
never: "NEVER\nforbids TX" {
  width: 180
  height: 70
  style.fill: "#ffebee"
}
guards: "Neither starts\na transaction" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}

mandatory -> guards
never -> guards
```

**Fig. 1.** Same family (guard propagations), opposite predicates on “is a transaction active?”.

```java
@Service
public class OutboxService {

    @Transactional(propagation = Propagation.MANDATORY)
    public void enqueue(Event event) {
        outboxRepository.save(event); // must be called inside caller's TX
    }
}

@Service
public class MetricsService {

    @Transactional(propagation = Propagation.NEVER)
    public void emit(Metric m) {
        http.post("/metrics", m); // must not run inside caller's TX
    }
}
```

**Listing 1.** Conceptual: `MANDATORY` for helpers that must stay atomic with the caller; `NEVER` for code that must not enlist in the caller’s resources.

## Not the pair people confuse with `REQUIRES_NEW`

Interview dumps sometimes pit **`MANDATORY`** against **`REQUIRES_NEW`**. That mixes different axes:

* **`MANDATORY` vs `NEVER`** — both **guard** transaction **presence** (throw if wrong).
* **`REQUIRED` vs `REQUIRES_NEW`** — both **manage** transaction **creation/joining** (start or join vs always new physical TX).

See [[How does MANDATORY transaction propagation work]], [[How does NEVER transaction propagation work]], and [[How does REQUIRES_NEW transaction propagation work]].

When you need to **step out** of an existing transaction without throwing, use **`NOT_SUPPORTED`** (suspend), not `NEVER` — [[How does NOT_SUPPORTED transaction propagation work]].

> [!warning] Guards apply only through the proxy
> Same-class `this.mandatory()` or `this.never()` bypasses the interceptor, so neither guard throws and propagation is not enforced. Cross-bean calls only — [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!warning] Neither fixes a missing facade transaction
> `MANDATORY` **detects** a missing outer boundary; it does **not** replace `@Transactional` on the entry service. `NEVER` **detects** accidental enlistment; it does not suspend the outer TX (that is `NOT_SUPPORTED`).

> [!tip] Interview answer
> **`MANDATORY` throws when no transaction exists; `NEVER` throws when one exists.** Both are guard propagations — neither creates a transaction. They are opposites on transaction presence, not counterparts to `REQUIRES_NEW`. Enforce them through a proxied cross-bean call, not `this`.
