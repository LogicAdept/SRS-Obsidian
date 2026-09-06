<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #Java/Persistence/JPA #SRS

# What is the difference between optimistic and pessimistic locking in Hibernate?

> [!abstract] Short answer
> **Optimistic locking** assumes conflicts are **rare**: transactions **do not** hold row locks while you work. Hibernate (JPA) stores a **`@Version`** number or timestamp, **checks it on `UPDATE`/`DELETE` at flush/commit**, and throws **`OptimisticLockException`** (transaction marked **rollback**) if another unit of work won. **Pessimistic locking** assumes conflicts are **likely**: Hibernate asks the **database** for a **long-term row lock** **immediately** (`SELECT … FOR UPDATE` / `FOR SHARE`) via `LockModeType.PESSIMISTIC_WRITE` / `PESSIMISTIC_READ`. Hibernate **never locks objects in memory**. JPA **assumes optimistic concurrency** by default (typically **read-committed** isolation); you **opt in** to explicit lock modes.

## Two stories about conflict

| | **Optimistic** | **Pessimistic** |
| --- | --- | --- |
| **Assumption** | Concurrent work usually **does not** collide | Concurrent work **will** collide |
| **When the lock bites** | **Flush/commit** (version compare) | **On read/lock request** |
| **Mechanism** | `WHERE id=? AND version=?`; then increment | DB lock (`FOR UPDATE` / `FOR SHARE`) |
| **Failure** | `OptimisticLockException` | `PessimisticLockException` (tx rollback) or `LockTimeoutException` (statement only) |
| **Needs `@Version`?** | **Yes** for portable automatic checks | **No** for `PESSIMISTIC_READ`/`WRITE` |
| **Scales for** | Read-often, write-sometimes; **long conversations** across several DB txs | Short, hot rows (inventory, seats) |

JPA `@Version`: one field on the **root** entity, mapped to the **primary table**; types include `int`/`long` wrappers, `Instant`, `LocalDateTime`, `Timestamp`. The **application must not** assign it — use `OPTIMISTIC_FORCE_INCREMENT` / `PESSIMISTIC_FORCE_INCREMENT` to bump without a business change. Spec: enable optimistic locking on anything **merged from detached** or **concurrently accessed**, or **you** own consistency. Hibernate: a **null** version on a detached instance is treated as **transient**.

```d2
direction: down
opt: "Optimistic: read version v\nwork without row lock" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
chk: "Flush: UPDATE … WHERE version=v" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
pes: "Pessimistic: SELECT … FOR UPDATE\nnow; hold until commit" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}

opt -> chk
```

**Fig. 1.** Optimistic checks at write; pessimistic serializes at read.

**Lock modes** (`EntityManager.lock` / `find` / `Query.setLockMode`, Hibernate `Session.lock` + `LockMode`):

- **`OPTIMISTIC`**: version checked **near end of tx** (versioned types only).
- **`OPTIMISTIC_FORCE_INCREMENT`**: check **and increment** even if the entity did not change.
- **`PESSIMISTIC_READ`**: shared lock (`FOR SHARE` where supported; else **`FOR UPDATE`**).
- **`PESSIMISTIC_WRITE`**: `SELECT … FOR UPDATE`. Hibernate extras: **`UPGRADE_NOWAIT`**, **`UPGRADE_SKIPLOCKED`**.
- **`PESSIMISTIC_FORCE_INCREMENT`**: pessimistic write **plus immediate `UPDATE` of version**.

Hibernate `LockMode.READ` is **not** JPA `LockModeType.READ` (`OPTIMISTIC`). Weaker lock requests are **no-ops** if a **stronger** lock is already held.

```java
@Version
private long version;

em.lock(order, LockModeType.OPTIMISTIC);           // check at commit
em.find(Seat.class, id, LockModeType.PESSIMISTIC_WRITE); // FOR UPDATE now
```

**Listing 1.** Conceptual: version for optimistic; explicit lock mode for pessimistic.

Pessimistic is **in addition to** [[What are transaction isolation levels in Hibernate|isolation]], not a replacement. Bulk HQL `UPDATE` **bypasses** optimistic version unless **`update versioned`**.

> [!warning] Lost updates without @Version look like “Hibernate works”
> Unversioned entities get **last-commit-wins** on flush. Do **not** set `@Version` in application code. `OptimisticLockException` **rolls back** — retry the **use case**, not just `flush`. `PESSIMISTIC_WRITE` can **deadlock**; timeout 0 is **NOWAIT**. `refresh` can still see a non-repeatable read unless isolation is at least repeatable read.

> [!tip] Interview answer
> Optimistic locking uses a @Version column and fails at flush if another transaction changed the row; pessimistic locking takes a database FOR UPDATE (or FOR SHARE) immediately. JPA is built around optimistic concurrency at read-committed; I add @Version on concurrent entities and merge paths. I use PESSIMISTIC_WRITE only for short, contested rows. Hibernate LockMode and JPA LockModeType line up except that Hibernate READ is not JPA OPTIMISTIC.

See [[What are transaction isolation levels in Hibernate]], [[What is Hibernate dirty checking]], [[What is Hibernate entity lifecycle states]], and [[What is the difference between JPA as a specification and Hibernate]].
