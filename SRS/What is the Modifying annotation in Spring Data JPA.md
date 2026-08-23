<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Annotations #SRS

# What is the Modifying annotation in Spring Data JPA?

> [!abstract] Short answer
> **`@Modifying`** marks a repository method whose **`@Query`** runs **DML** (`INSERT`, `UPDATE`, `DELETE`, or DDL) instead of a select. Without it, Spring Data treats the method as a read query and DML execution fails. Pair it with **`@Transactional`** when the method must write outside a read-only repository default.

## Role on `@Query` methods

Spring Data JPA executes most `@Query` methods as **selects**. For bulk DML written in JPQL or native SQL, add `@Modifying` so the framework calls **`executeUpdate()`** rather than a result-list fetch.

```java
public interface UserRepository extends JpaRepository<User, Long> {

  @Modifying
  @Transactional
  @Query("UPDATE User u SET u.active = false WHERE u.lastLoginDate < :date")
  int deactivateInactiveUsers(@Param("date") LocalDate date);
}
```

**Listing 1.** `@Modifying` + `@Query` for JPQL update; return type is commonly `int` (rows affected) or `void`.

The annotation applies **only** with `@Query`. **Derived** modifying methods (`deleteBy…`, `removeBy…`) and **custom repository implementations** already control the underlying API and do not need `@Modifying`.

```d2
direction: right
query: "@Query on repository method" {
  style.fill: "#e3f2fd"
}
select: "Default: selecting query\n(getResultList path)" {
  style.fill: "#fff3e0"
}
mod: "@Modifying present" {
  style.fill: "#e8f5e9"
}
dml: "Updating query\n(executeUpdate path)" {
  style.fill: "#f3e5f5"
}

query -> select
query -> mod -> dml
```

**Fig. 1.** `@Modifying` switches execution from read to update for the same `@Query` string.

## Transactions and persistence context

Modifying queries change database rows **without** automatically updating entities already loaded in the persistence context. Spring Data therefore does **not** auto-clear the context after DML (that would drop unflushed pending changes). Optional flags:

| Attribute | Default | Effect |
| --- | --- | --- |
| `flushAutomatically` | `false` | flush persistence context **before** the DML |
| `clearAutomatically` | `false` | clear persistence context **after** the DML |

Repository interfaces are often declared `@Transactional(readOnly = true)` for query-heavy APIs. A modifying method must run in a **write** transaction — typically by adding method-level `@Transactional` (overriding read-only for that method).

> [!warning] Missing `@Modifying` on DML
> An `@Query` with `UPDATE`/`DELETE` but no `@Modifying` is still executed as a select. Hibernate rejects DML on that path (`QueryExecutionRequestException`), surfaced as **`InvalidDataAccessApiUsageException`**.

> [!warning] Stale first-level cache after bulk DML
> Managed entities in memory can disagree with rows changed by a bulk `@Query`. Use `clearAutomatically = true`, `EntityManager.clear()`, or avoid reusing cached instances in the same transaction after the update.

> [!tip] Interview answer
> `@Modifying` tells Spring Data JPA that an `@Query` method runs insert/update/delete SQL, not a select. It is required only on `@Query` DML — not on derived deletes. Modifying methods need a write transaction, often via method-level `@Transactional`, and may return the affected row count as `int`.

See [[What is Spring Data JPA]], [[How do you implement soft deletes in Spring Data JPA]], and [[What are derived query methods in Spring Data JPA]].
