<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What is the difference between `NESTED` and `REQUIRED` propagation?

> [!abstract] Short answer
> **With an outer transaction active, both join the same physical transaction — but `NESTED` adds a JDBC savepoint for partial rollback, while `REQUIRED` does not.** Inner failure under `REQUIRED` marks the shared transaction rollback-only and blocks outer commit; inner failure under `NESTED` can roll back **only to the savepoint** so the outer method may continue. **With no outer transaction, both behave like `REQUIRED` and start one.**

## Same physical TX, different failure semantics

When a caller transaction already exists:

| | `REQUIRED` | `NESTED` |
| --- | --- | --- |
| Physical transaction | **Same** as outer | **Same** as outer |
| Savepoint | **No** | **Yes** (JDBC savepoint when supported) |
| Inner failure | Usually marks whole TX **rollback-only** | Can roll back **to savepoint**; outer may continue |
| Outer rollback | Undoes inner work | Undoes inner work |

Spring’s `NESTED` contract: nested **if** a current transaction exists; **behave like `REQUIRED` otherwise** — see [[What happens if NESTED is used when no current transaction exists]].

```d2
direction: down
outer: "Outer TX open" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
req: "Inner REQUIRED\nno savepoint" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}
nest: "Inner NESTED\nsavepoint" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
reqFail: "Inner throws →\nwhole TX rollback-only" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
nestFail: "Inner throws →\nrollback to savepoint\nouter may catch & continue" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}

outer -> req -> reqFail
outer -> nest -> nestFail
```

**Fig. 1.** The savepoint is what separates `NESTED` from joining `REQUIRED`.

```java
@Service
public class OrderService {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        try {
            audit.tryRecord(order); // NESTED in AuditService
        } catch (AuditException ex) {
            // NESTED: audit rolled back to savepoint; order row still in outer TX
        }
        // REQUIRED inner failure would mark rollback-only → outer commit fails
    }
}
```

**Listing 1.** Conceptual: `NESTED` is the savepoint pattern for “optional sub-work” inside one commit boundary.

## When there is no outer transaction

The savepoint difference **never appears**: both `REQUIRED` and `NESTED` **start a new physical transaction** on a thread with no active transaction. Interview answers that say “`NESTED` always uses a savepoint” miss this case.

Platform requirements for savepoints when an outer TX exists: [[Does NESTED propagation require JDBC savepoints]] and [[How does NESTED transaction propagation work]].

Rollback-only behavior for nested `REQUIRED`: [[What is UnexpectedRollbackException in Spring REQUIRED propagation]].

> [!warning] Catching an inner `REQUIRED` exception does not save the commit
> Under `REQUIRED`, an inner runtime failure typically leaves the **shared** transaction rollback-only even if the outer method catches the exception. `NESTED` is the propagation meant for “undo inner work locally, keep going” — not `REQUIRED` with a try/catch.

> [!warning] Neither gives an independent inner commit
> Both share one physical transaction until the outer commits. For inner work that must **commit before** the outer finishes, use `REQUIRES_NEW` — [[What is the difference between NESTED and REQUIRES_NEW propagation]].

> [!tip] Interview answer
> **With an outer TX, `REQUIRED` and `NESTED` share one physical transaction; `NESTED` adds a savepoint for partial rollback.** Inner failure under `REQUIRED` usually poisons the whole commit; under `NESTED` the outer can continue after rolling back to the savepoint. With no outer TX, both start a new transaction and look the same.
