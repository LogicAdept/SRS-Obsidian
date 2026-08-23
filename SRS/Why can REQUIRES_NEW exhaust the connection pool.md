<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# Why can REQUIRES_NEW exhaust the connection pool?

> [!abstract] Short answer
> **`REQUIRES_NEW` suspends the outer transaction but leaves its JDBC connection bound** while the inner scope **opens a second physical transaction on another connection**. Under load, **one thread can hold two pool connections** (suspended outer + active inner). If every thread does that simultaneously, the pool has **no free connections left** for new inner work — threads **block waiting on themselves** and the app looks deadlocked.

## Two connections per thread

Spring's transaction-propagation reference states that with **`PROPAGATION_REQUIRES_NEW`**, outer resources **remain bound** to the suspended outer transaction while the inner transaction **acquires its own resources** — typically a **new database connection**.

That independence is the feature: inner commits or rolls back **without** joining the outer physical transaction. The cost is **connection consumption doubles** for the duration of the inner call.

```d2
direction: right
pool: "Connection pool\n(size N)" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
t1: "Thread 1\nconn A (suspended outer)\nconn B (REQUIRES_NEW)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
t2: "Thread 2\nconn C + conn D" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
wait: "Thread N+1\nblocks — no conn left" {
  width: 200
  height: 60
  style.fill: "#ffcdd2"
}

pool -> t1
pool -> t2
pool -> wait
```

**Fig. 1.** Each active outer+inner pair ties up two connections until the inner method returns.

## Official pool-sizing warning

The same Spring documentation warns explicitly:

- This pattern **may lead to exhaustion of the connection pool** and **potentially to a deadlock** if several threads have an active outer transaction and wait to acquire a new connection for their inner transaction, while the pool **cannot hand out any such inner connection anymore**.
- **Do not use `REQUIRES_NEW`** unless the connection pool is **appropriately sized — exceeding the number of concurrent threads by at least 1**.

Rule of thumb: if up to **T** request threads can nest **`REQUIRES_NEW`** inside an outer **`@Transactional`**, plan for **`T × 2`** peak connections (plus headroom), not **`T`**.

```java
@Service
public class OrderService {

    @Transactional // REQUIRED — holds connection #1 (suspended during audit)
    public void placeOrder(Order order) {
        orders.save(order);
        auditService.record(order); // REQUIRES_NEW — needs connection #2
    }
}
```

**Listing 1.** Conceptual cross-bean nesting — two connections for one thread while `record` runs.

## When `NESTED` avoids the extra connection

**`PROPAGATION_NESTED`** uses **one physical transaction** with **JDBC savepoints** for partial rollback — it does **not** suspend the outer transaction and grab a second connection for the inner scope. Choose **`NESTED`** when inner failure should roll back only to a savepoint but you **do not** need an independent commit before the outer finishes. See [[How does NESTED transaction propagation work]] and [[Does NESTED propagation require JDBC savepoints]].

> [!warning] Hot-path audit logging is the classic trap
> A **`REQUIRES_NEW`** audit helper on every **`@Transactional`** service method doubles connection demand at peak. Mis-sized pools produce **indefinite waits** on `DataSource.getConnection()`, not always obvious SQL errors. Prefer **`NESTED`**, async outbox, or batching when independent commit is not required. Related: [[Why can REQUIRES_NEW deadlock when inner and outer touch the same rows]] and [[How does REQUIRES_NEW transaction propagation work]].

> [!tip] Interview answer
> REQUIRES_NEW suspends the outer transaction but keeps its connection; the inner transaction needs another. Many threads doing that at once can exhaust the pool and deadlock waiting for a second connection. Spring recommends sizing the pool above concurrent threads by at least one before using REQUIRES_NEW; NESTED reuses one connection via savepoints instead.
