<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Annotations #SRS

# How do you apply pessimistic locking in a Spring Data JPA repository?

> [!abstract] Short answer
> Annotate a repository query method (or a redeclared CRUD method) with `@Lock(LockModeType.PESSIMISTIC_WRITE)`. Spring Data JPA passes the lock mode to the JPA provider, which typically issues a database exclusive lock such as `SELECT … FOR UPDATE`. Call it inside a transaction so the lock lasts until commit or rollback.

## Repository `@Lock`

Spring Data JPA’s `@Lock` sets the JPA `LockModeType` on the generated query. It works on derived query methods, `@Query` methods, and CRUD methods you redeclare in the repository interface.

```java
public interface BankAccountRepository extends JpaRepository<BankAccount, Long> {

  @Lock(LockModeType.PESSIMISTIC_WRITE)
  @Query("SELECT b FROM BankAccount b WHERE b.id = :id")
  Optional<BankAccount> findByIdForUpdate(@Param("id") Long id);

  // Or redeclare a CRUD method:
  @Lock(LockModeType.PESSIMISTIC_READ)
  @Override
  Optional<BankAccount> findById(Long id);
}
```

**Listing 1.** Lock metadata on a custom `@Query` or a redeclared `findById` (Spring Data JPA locking reference).

`PESSIMISTIC_WRITE` requests an exclusive database lock to serialize concurrent updates. Jakarta Persistence defines it for read-then-modify flows where update conflicts are likely. The provider maps it to vendor SQL (commonly `FOR UPDATE`). The lock is tied to the **persistence context transaction** — without an active transaction, behavior is undefined or the lock may not be held through your business logic.

```d2
direction: right
svc: "@Transactional service\nread-modify-write" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
repo: "@Lock(PESSIMISTIC_WRITE)\nrepository method" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
jpa: "JPA provider\nSELECT … FOR UPDATE" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
commit: "commit / rollback\nlock released" {
  width: 240
  height: 80
  style.fill: "#f3e5f5"
}

svc -> repo -> jpa -> commit
```

**Fig. 1.** Pessimistic lock is acquired when the annotated repository method runs inside a transaction and released at transaction end.

## Versus optimistic locking

Pessimistic locking blocks other transactions up front. **Optimistic locking** uses a `@Version` column: no row lock on read, but commit fails with `OptimisticLockException` if the version changed. Prefer pessimistic locks for hot contended rows; prefer `@Version` when conflicts are rare. You can combine both on a versioned entity — the provider may still perform version checks. Optional `@QueryHint(name = "jakarta.persistence.lock.timeout", value = "…")` avoids waiting indefinitely when the row is already locked.

> [!warning] Lock without transaction
> Calling a `@Lock` method outside a transaction may not hold the database lock through your update. Pair repository locks with [[What is the Transactional annotation in Spring Data]] on the service layer. Also distinguish `PESSIMISTIC_READ` (shared) from `PESSIMISTIC_WRITE` (exclusive) — wrong mode still allows some concurrent writers depending on the database.

See [[What is Spring Data JPA]] and [[What is the difference between optimistic and pessimistic locking in Hibernate]].

> [!tip] Interview answer
> I put `@Lock(LockModeType.PESSIMISTIC_WRITE)` on the repository finder that loads the row I am about to change, usually with an explicit `@Query`, inside a transactional service. That maps to a DB row lock like `FOR UPDATE`. Optimistic locking with `@Version` is the alternative when I do not want to lock up front.
