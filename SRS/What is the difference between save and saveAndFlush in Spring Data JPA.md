<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS

# What is the difference between save and saveAndFlush in Spring Data JPA?

> [!abstract] Short answer
> **`save`** registers the entity in the persistence context (`persist` for new, `merge` for existing) and may defer SQL until a later **flush**. **`saveAndFlush`** does the same registration, then calls **`EntityManager.flush()`** immediately so pending changes are synchronized to the database inside the current transaction.

## What each method does

`SimpleJpaRepository` implements both on top of the JPA `EntityManager`:

```java
@Transactional
public S save(S entity) {
  if (entityInformation.isNew(entity)) {
    entityManager.persist(entity);
    return entity;
  } else {
    return entityManager.merge(entity);
  }
}

@Transactional
public S saveAndFlush(S entity) {
  S result = save(entity);
  flush(); // entityManager.flush()
  return result;
}
```

**Listing 1.** `saveAndFlush` is literally `save` followed by an immediate flush (Spring Data JPA 4.x `SimpleJpaRepository`).

Both methods return the managed entity. Neither commits the transaction.

```d2
direction: right
save: "repository.save(entity)" {
  style.fill: "#e3f2fd"
}
ctx: "Persistence context\n(managed state)" {
  style.fill: "#fff3e0"
}
flushLater: "SQL may wait\nuntil auto/manual flush" {
  style.fill: "#fce4ec"
}
saveFlush: "repository.saveAndFlush(entity)" {
  style.fill: "#e8f5e9"
}
now: "entityManager.flush()\nimmediate SQL sync" {
  style.fill: "#f3e5f5"
}

save -> ctx -> flushLater
saveFlush -> ctx -> now
```

**Fig. 1.** `save` queues work in the persistence context; `saveAndFlush` forces synchronization to the database before the method returns.

## When flush happens without saveAndFlush

JPA **`flush()`** synchronizes the persistence context to the database. With Hibernate’s default **`FlushModeType.AUTO`**, the provider may flush before some queries or at transaction commit even after a plain `save()`. So `save()` does **not** guarantee “SQL only at commit,” but it also does **not** force an extra flush on every call.

Prefer **`save()`** for normal writes so the provider can batch and defer work. Reach for **`saveAndFlush()`** when the **same open transaction** must see database-visible state before commit — for example, running a native query or stored procedure that reads rows you just wrote, or triggering immediate DB constraint checks.

> [!warning] Flush is not commit
> A flush sends SQL to the database, but the transaction stays open. Other transactions still cannot see uncommitted changes (under default isolation). If the transaction **rolls back** later, flushed work is rolled back too. **`saveAndFlush` does not commit.**

> [!warning] “Has an id” ≠ new entity
> `save()` chooses `persist` vs `merge` via **`entityInformation.isNew(entity)`**, not a simple null-id check. Assigned identifiers, `@Version`, and `Persistable.isNew()` can make an entity with an id still “new.” Wrong assumptions here cause surprise `merge` calls.

## Typical usage

```java
@Transactional
public Order placeOrder(Order order) {
  Order saved = orderRepository.save(order); // default path
  return saved;
}

@Transactional
public void deactivateAndAudit(User user) {
  userRepository.saveAndFlush(user);
  jdbcTemplate.update(
      "INSERT INTO audit_log(user_id, action) VALUES (?, ?)",
      user.getId(), "DEACTIVATED");
}
```

**Listing 2.** Use `saveAndFlush` when later steps in the **same transaction** need the row present in the database.

> [!tip] Interview answer
> `save` puts the entity under JPA management and may delay SQL until flush time. `saveAndFlush` saves and immediately flushes the persistence context. Neither commits — flush pushes SQL inside the transaction, and a rollback still undoes it. Default to `save`; use `saveAndFlush` when you need DB-visible state before commit, such as for a native query in the same transaction.

See [[What is Spring Data JPA]], [[How does the Hibernate first-level cache work in Spring]], and [[What is the difference between save and persist in JPA with Spring Data]].
