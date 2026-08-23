<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# When should you use `NOT_SUPPORTED` transaction propagation?

> [!abstract] Short answer
> Use **`Propagation.NOT_SUPPORTED`** when work must run **outside** the caller’s transaction — slow HTTP calls, in-memory processing, or metrics — so it does **not** extend the database transaction or inherit rollback scope. Spring **suspends** any active outer transaction for the call and **resumes** it afterward. Do **not** use it when the side effect must stay **atomic** with the database write.

## Step out without throwing

`NOT_SUPPORTED` always executes **non-transactionally**. If a transaction exists, it is **suspended** (not joined). That differs from **`NEVER`**, which **throws** when a transaction is present — [[What is the difference between MANDATORY and NEVER propagation]] and [[How does NOT_SUPPORTED transaction propagation work]].

Good fits:

* **Slow external I/O** (HTTP notification, email gateway) invoked from a `@Transactional` facade
* **In-memory** computation that should not hold JDBC/JPA synchronization
* Operations whose **side effects may commit independently** and must **not** roll back with the outer TX if the outer later fails

```java
@Service
public class OrderFacade {

    @Transactional
    public void placeOrder(Order order) {
        orders.save(order);
        notifications.sendReceipt(order); // NOT_SUPPORTED below
        inventory.reserve(order);
    }
}

@Service
public class NotificationClient {

    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void sendReceipt(Order order) {
        http.post("/notify", order.id()); // runs while outer TX suspended
    }
}
```

**Listing 1.** Conceptual cross-bean call: the notification runs without participating in the order transaction.

## What it does not do

Suspension **does not release** the outer connection back to the pool — the outer transaction’s resources stay bound while suspended. `NOT_SUPPORTED` mainly prevents the **slow call from running inside** the open unit of work (timeouts, lock hold time), not a free pool slot. See [[Why can REQUIRES_NEW exhaust the connection pool]] for the two-connection case.

JTA suspension may require a configured Jakarta `TransactionManager` — not every stack supports suspend equally.

If accidental enlistment should **fail loudly**, prefer **`NEVER`**. If the helper should **join** when a TX exists, use **`SUPPORTS`** — [[When should you use SUPPORTS transaction propagation]].

> [!warning] Not atomic with the database write
> Side effects during the suspended window are **outside** the outer rollback. Do not send irreversible external calls under `NOT_SUPPORTED` if they must commit or roll back **with** the same business transaction.

> [!warning] Self-invocation skips suspension
> `this.sendReceipt(order)` does not apply `NOT_SUPPORTED`. Cross-bean proxy call required — [[What is the difference between a self-invocation and a cross-bean Transactional call]].

> [!tip] Interview answer
> **Use `NOT_SUPPORTED` to run work non-transactionally while suspending an outer TX — typical for slow external calls so they do not stretch the database transaction.** The outer connection is still held while suspended. For atomic side effects with the DB write, stay on `REQUIRED`; to reject TX presence entirely, use `NEVER`.
