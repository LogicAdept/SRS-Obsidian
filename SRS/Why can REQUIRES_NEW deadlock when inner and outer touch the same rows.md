<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# Why can REQUIRES_NEW deadlock when inner and outer touch the same rows?

> [!abstract] Short answer
> **`REQUIRES_NEW` suspends the outer transaction but does not release its database locks or connection.** The inner transaction opens on a **second connection** and may try to lock the **same rows** the suspended outer still holds. The outer cannot resume until the inner finishes, and the inner cannot proceed until the outer releases locks — a **self-deadlock** on one thread (or a classic wait-for-lock hang).

## Suspended outer still owns the locks

Spring's propagation guide states that with **`PROPAGATION_REQUIRES_NEW`**:

1. The inner scope always gets an **independent physical transaction**.
2. **Resources attached to the outer transaction remain bound** while the inner acquires **its own** (another connection).
3. Inner locks are released when the **inner** transaction completes — but **outer locks stay held** until the outer resumes and commits or rolls back.

So if the outer method already updated (or locked) row R, and the inner method also needs an exclusive lock on R:

| Step | Who holds what |
|---|---|
| Outer `UPDATE` on row R | Outer connection holds lock |
| Spring suspends outer, starts `REQUIRES_NEW` | Outer still holds lock; inner uses new connection |
| Inner `UPDATE` / `SELECT … FOR UPDATE` on R | Blocks waiting for outer's lock |
| Outer waiting for inner to return | Never resumes → **deadlock / hang** |

```java
@Service
public class OrderService {

    @Transactional // REQUIRED — locks order row
    public void cancel(OrderId id) {
        Order order = orders.findForUpdate(id);
        order.markCancelling();
        audit.recordCancel(id); // REQUIRES_NEW that also updates same order → hang
    }
}
```

**Listing 1.** Conceptual bug — do not nest `REQUIRES_NEW` work that needs the same row locks the parent already took.

```d2
direction: right
outer: "Outer TX (suspended)\nholds lock on row R" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
inner: "Inner REQUIRES_NEW\nwants lock on row R" {
  width: 220
  height: 70
  style.fill: "#fce4ec"
}
wait: "Each waits for the other\n(self-deadlock)" {
  width: 200
  height: 60
  style.fill: "#ffcdd2"
}

outer -> wait
inner -> wait
```

**Fig. 1.** Same-thread lock wait: outer cannot finish until inner returns; inner cannot lock until outer finishes.

## Related failure: connection-pool deadlock

Spring documents a **second** deadlock mode: many threads each hold a suspended outer connection and wait for a **second** connection for `REQUIRES_NEW`. When the pool is empty, they wait forever — see [[Why can REQUIRES_NEW exhaust the connection pool]]. That is pool contention across threads; the cue here is **row-lock contention** between outer and inner on the **same data**.

## Safer alternatives

- **Do not** use `REQUIRES_NEW` to update tables/rows the parent transaction already locked.
- Prefer **`NESTED`** (savepoint on the **same** connection) when you need partial rollback without a second TX — [[How does NESTED transaction propagation work]].
- Move independent work (true audit/outbox) to rows/tables the outer TX does not lock, or run it **after** the outer commits (event, async listener).

> [!warning] Independent commit does not mean independent locks
> Interviewers often praise `REQUIRES_NEW` for “audit that survives outer rollback.” That is true **only** when the inner work does **not** need locks the suspended outer still holds. Same-row updates turn independence into a hang. See [[How does REQUIRES_NEW transaction propagation work]] and [[What is the difference between NESTED and REQUIRES_NEW propagation]].

> [!tip] Interview answer
> REQUIRES_NEW suspends the outer transaction but keeps its connection and locks. An inner transaction on a new connection that locks the same rows waits forever, because the outer cannot resume until the inner returns. Avoid REQUIRES_NEW for the same tables the parent already locked; use NESTED or post-commit work instead.
