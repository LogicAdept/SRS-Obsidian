<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# When should you use `NEVER` transaction propagation?

> [!abstract] Short answer
> Use **`Propagation.NEVER`** when the method **must not run inside a transaction** and accidentally doing so is a **bug** you want to detect — for example cache eviction, metrics emission, or read-only reporting that must not enlist in a caller’s JDBC/JPA unit of work. If a transaction is already active, Spring throws **`IllegalTransactionStateException`** instead of joining or suspending.

## Fail fast when a transaction must not exist

`NEVER` is a **guard** propagation: execute non-transactionally when no TX is active; **throw if one exists**. It does **not** start a transaction.

Reach for it when:

* running **inside a TX would be wrong** (side effects that must not roll back with the caller, or code that must not see uncommitted caller state tied to enlistment)
* you want **tests or reviews to catch** accidental transactional wrapping — louder than `NOT_SUPPORTED`, which silently suspends

```java
@Service
public class CacheMaintenanceService {

    @Transactional(propagation = Propagation.NEVER)
    public void evictRegion(String region) {
        cacheManager.getCache(region).clear();
    }
}

@Service
public class OrderFacade {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        cache.evictRegion("products"); // → IllegalTransactionStateException
    }
}
```

**Listing 1.** Conceptual: `NEVER` turns “called inside a TX” into an immediate failure. Mechanism: [[How does NEVER transaction propagation work]].

## `NEVER` vs `NOT_SUPPORTED`

| Situation | `NOT_SUPPORTED` | `NEVER` |
| --- | --- | --- |
| Active outer TX | **Suspend** and run | **Throw** |
| Intent | Step outside TX quietly | **Reject** TX presence as an error |

Use **`NOT_SUPPORTED`** for long external I/O where suspension is acceptable — [[How does NOT_SUPPORTED transaction propagation work]]. Use **`NEVER`** when presence of a transaction indicates a **misconfiguration**.

Mirror guard: **`MANDATORY`** throws when **no** TX exists — [[What is the difference between MANDATORY and NEVER propagation]].

> [!warning] Uncommon in everyday services
> Production code rarely defaults to `NEVER`; interviews still expect you to name the **throw-if-transaction-exists** behavior and contrast it with `NOT_SUPPORTED`.

> [!warning] Proxy-only enforcement
> `this.neverHelper()` from the same class bypasses the guard. Cross-bean calls only — [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **Use `NEVER` when the method must never run inside a transaction and you want an exception if one is active.** It is a deliberate guard, not a default. For “run outside the caller’s TX without throwing,” use `NOT_SUPPORTED`, not `NEVER`.
