<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# How does `REQUIRED` transaction propagation work?

> [!abstract] Short answer
> **`Propagation.REQUIRED` joins an existing transaction on the thread, or starts one if none exists.** It is the default for `@Transactional`. Nested `REQUIRED` methods create separate *logical* scopes but share one *physical* transaction, so a rollback-only mark from an inner scope can doom the outer commit.

## Join or start

`REQUIRED` means “there must be a physical transaction for this work”:

* no active transaction → Spring starts one for this scope;
* an outer transaction already exists → this method **participates** in it (same connection / resource transaction for typical local TX managers).

```java
@Service
public class OrderService {

    @Transactional // propagation defaults to REQUIRED
    public void placeOrder(Order order) {
        orderRepository.save(order);
        inventoryService.reserve(order); // also REQUIRED → same physical TX
    }
}
```

**Listing 1.** Default `@Transactional` is `REQUIRED`; a cross-bean call into another `REQUIRED` method joins the same physical transaction.

```d2
direction: down
call: "REQUIRED method enters" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
hasTx: "Thread already has a TX?" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
join: "Join / participate\nin outer physical TX" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
start: "Begin a new\nphysical TX" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
logical: "New logical scope\n(same physical TX if joined)" {
  width: 300
  height: 80
  style.fill: "#f3e5f5"
}

call -> hasTx
hasTx -> join: yes
hasTx -> start: no
join -> logical
start -> logical
```

**Fig. 1.** `REQUIRED` always ends in a physical transaction; joining keeps one resource transaction for the whole call stack.

## Logical scopes, one physical transaction

Each `@Transactional(REQUIRED)` method gets its own **logical** transaction scope (it can set rollback-only for that scope). Under standard `REQUIRED` behavior those scopes map to the **same physical** transaction. An inner rollback-only marker therefore blocks a successful outer commit.

By default a participating method’s local isolation, timeout, and `readOnly` flags are **silently ignored** in favor of the outer scope. Set `validateExistingTransaction` to `true` on the transaction manager if mismatches should fail instead.

Contrast with [[How does REQUIRES_NEW transaction propagation work]] (independent physical transaction) and [[How does NESTED transaction propagation work]] (same physical TX with savepoints).

## Rollback-only and `UnexpectedRollbackException`

If an inner `REQUIRED` scope marks the shared transaction rollback-only (typical default: an uncaught `RuntimeException` or `Error` leaves the interceptor), catching that exception in the outer method does **not** clear the mark. When the outer scope later tries to commit, Spring throws `UnexpectedRollbackException` so the caller cannot believe a commit happened.

```java
@Transactional
public void outer() {
    try {
        otherBean.innerThatThrows(); // REQUIRED; marks TX rollback-only
    } catch (RuntimeException ignored) {
        // business continues…
    }
    // commit attempt → UnexpectedRollbackException
}
```

**Listing 2.** Conceptual: swallowing the inner failure does not rehabilitate a rollback-only physical transaction under `REQUIRED`.

> [!warning] Catching does not undo rollback-only
> Under `REQUIRED`, an inner failure that marks rollback-only still dooms the shared physical transaction. Handling the exception in the outer method does not make commit succeed; expect `UnexpectedRollbackException` at commit time.

> [!warning] Self-invocation skips the proxy
> In default **proxy** mode, `this.otherRequiredMethod()` never hits the transaction interceptor, so the inner `@Transactional(REQUIRED)` is not applied. That is a self-invocation issue, not a `REQUIRED` special case — see [[What happens when one Spring Transactional method calls another]]. AspectJ mode can advise self-calls.

> [!tip] Interview answer
> **`REQUIRED` is the default: join the current transaction or start one.** Nested `REQUIRED` methods share one physical transaction with separate logical scopes, so an inner rollback-only mark can force the whole unit of work to roll back and surface as `UnexpectedRollbackException` on the outer commit. Self-calls on `this` skip the proxy, so the inner annotation never runs unless you go through another bean or AspectJ.
