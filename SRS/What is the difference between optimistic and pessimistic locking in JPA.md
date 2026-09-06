<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS

# What is the difference between optimistic and pessimistic locking in JPA?

> [!abstract] Short answer
> **Optimistic** locking lets transactions proceed and **checks a version** (or timestamp) at **update/delete**. If another transaction changed the row, the provider throws **`OptimisticLockException`** and **marks the transaction for rollback**. **Pessimistic** locking **takes a database lock immediately** and holds it until the transaction ends, so others cannot modify or delete that instance. JPA assumes optimistic concurrency as the default model. Hibernate-flavored twin: [[What is the difference between optimistic and pessimistic locking in Hibernate]]. What JPA is: [[What is the Java Persistence API JPA]].

## Version check later versus row lock now

Jakarta Persistence: each revision of versioned data has a version number or timestamp. On read-then-write, the provider **reads** the version with the entity and **verifies** it when flushing the update or delete. A mismatch is an optimistic lock failure. Portable apps put **`@Version`** on a field; the provider then does this **automatically**. Merge of a stale detached instance also fails (check may wait until flush or commit).

Pessimistic locks exist because optimistic collisions often **fail late**. Once a transaction holds a pessimistic lock, **no other transaction** (JPA or otherwise) may successfully **modify or delete** that instance until this transaction ends. The provider locks the **row(s)** for the entity’s non-collection state (including secondary tables / joined inheritance). Owned FKs on that row are locked; **referenced entities, element collections, and join-table relationships are not**, unless you set lock scope `EXTENDED` (join-table rows only; phantoms still possible). Spring Data entry point: [[How do you apply pessimistic locking in a Spring Data JPA repository]].

`LockModeType`: `OPTIMISTIC` / `OPTIMISTIC_FORCE_INCREMENT` (old names `READ` / `WRITE`); `PESSIMISTIC_READ` (shared-style repeatable read without blocking other readers), `PESSIMISTIC_WRITE` (exclusive; use when concurrent updaters would otherwise deadlock or fail), `PESSIMISTIC_FORCE_INCREMENT`. Pass them to `EntityManager.lock` / `find` / `refresh` or `Query.setLockMode`.

```d2
direction: down
opt: "optimistic\nread now, verify version at flush" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
pes: "pessimistic\nlock row now, hold until commit" {
  width: 280
  height: 50
  style.fill: "#ffe0b2"
}
opt -> pes: "late failure vs wait"
```

**Fig. 1.** Optimistic collisions show up at flush/commit. Pessimistic collisions wait (or time out) when taking the lock.

```java
@Entity
class Account {
    @Id Long id;
    @Version long version;   // portable automatic optimistic locking
    long balance;
}

Account a = em.find(Account.class, id, LockModeType.PESSIMISTIC_WRITE);
a.setBalance(a.getBalance() - 10);
```

**Listing 1.** Conceptual. `@Version` is the optimistic default. `PESSIMISTIC_WRITE` on `find`/`lock` is the explicit exclusive row lock.

Pessimistic lock not obtained: **`PessimisticLockException`** if the failure rolls back the **transaction**; **`LockTimeoutException`** if only the **statement** rolls back (`jakarta.persistence.lock.timeout`, `0` = no-wait — a **hint**, not portable). The spec does **not** define `SELECT FOR UPDATE` wording; do not depend on the SQL.

> [!warning] No @Version means you own lost-update prevention
> The provider must optimistically lock **versioned** entities. Unversioned entities skip that check; mixed graphs are only consistent for the versioned parts. Version-less “optimistic locking” is **not portable**.

> [!warning] Pessimistic does not lock the whole graph
> Default scope is the entity row (and its FK columns), not collections or inverse sides. Pessimistic locks can **deadlock**: [[What is deadlock]]. A provider may lock **more** rows than you selected.

> [!tip] Interview answer
> Optimistic locking uses a version column: you read freely and fail at flush if someone else updated the row, with OptimisticLockException and rollback. Pessimistic locking takes a database lock immediately and holds it until the transaction ends. JPA expects optimistic locking as the usual model; use pessimistic when a late collision is too expensive. Always map @Version on concurrently edited entities.
