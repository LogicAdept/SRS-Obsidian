<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# How would you explain `Propagation`?

> [!abstract] Short answer
> **`Propagation` tells Spring what to do when a `@Transactional` method is entered and a transaction may already exist.** The seven values (EJB CMT–style names) choose join, create, suspend, nest, or refuse. Default is **`REQUIRED`**. They apply only when the call goes through the Spring proxy (or AspectJ weaving).

## Seven behaviors, one decision point

`org.springframework.transaction.annotation.Propagation` maps to `TransactionDefinition` constants. Interview answer: name the default, then contrast the “new physical TX”, “savepoint”, and “must / must-not have a TX” options.

| Constant | If a TX exists | If none exists |
| --- | --- | --- |
| **`REQUIRED`** (default) | Join it | Create one |
| **`SUPPORTS`** | Join it | Run non-transactionally |
| **`MANDATORY`** | Join it | Throw |
| **`REQUIRES_NEW`** | Suspend, start new | Start new |
| **`NOT_SUPPORTED`** | Suspend, run without TX | Run without TX |
| **`NEVER`** | Throw | Run without TX |
| **`NESTED`** | Nested TX / JDBC savepoint | Like `REQUIRED` |

```d2
direction: down
enter: "Enter @Transactional\nmethod (via proxy)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ask: "Current TX?" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
join: "REQUIRED / SUPPORTS /\nMANDATORY join" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
new: "REQUIRES_NEW\nindependent TX" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
nest: "NESTED\nsavepoint" {
  width: 200
  height: 60
  style.fill: "#fce4ec"
}
forbid: "NEVER / NOT_SUPPORTED\navoid or suspend" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

enter -> ask
ask -> join
ask -> new
ask -> nest
ask -> forbid
```

**Fig. 1.** Propagation is the policy at the interceptor boundary — not a property of the database alone.

```java
@Transactional                          // REQUIRED by default
public void placeOrder(Order order) { … }

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void audit(Order order) { … }

@Transactional(propagation = Propagation.MANDATORY)
public void enqueueOutbox(Event e) { … }
```

**Listing 1.** Conceptual attribute usage from the `Propagation` / `@Transactional` APIs.

Depth cards: [[How does REQUIRED transaction propagation work]], [[How does REQUIRES_NEW transaction propagation work]], [[How does NESTED transaction propagation work]], [[What is the difference between REQUIRED and REQUIRES_NEW propagation]].

> [!warning] Names ≠ automatic suspension everywhere
> `REQUIRES_NEW` / `NOT_SUPPORTED` need a manager that can **suspend** (JTA often needs an explicit `TransactionManager`). `NESTED` needs savepoint support (typically `DataSourceTransactionManager`).

> [!warning] Self-invocation ignores propagation
> `this.helper()` never re-enters the interceptor, so a callee’s `REQUIRES_NEW` or `MANDATORY` does nothing — [[What happens when one Spring Transactional method calls another]].

> [!tip] Interview answer
> **Propagation answers: join, create, suspend, nest, or fail when a transactional method is entered.** Default `REQUIRED` joins or starts one TX. Reach for `REQUIRES_NEW` when work must commit alone, `NESTED` for savepoints, `MANDATORY`/`NEVER` to enforce presence or absence of a transaction.
