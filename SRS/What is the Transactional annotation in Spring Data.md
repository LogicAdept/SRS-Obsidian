<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Spring/Transactions #Java/Annotations #SRS

# What is the `Transactional` annotation in Spring Data?

> [!abstract] Short answer
> Spring Data JPA uses the **same Spring `@Transactional`** as the rest of the framework — not a separate Data annotation. **`SimpleJpaRepository`** applies it to inherited **`CrudRepository`** methods ( **`readOnly = true`** for queries). **Custom query methods** need **`@Transactional` on the repository interface** unless a **service** already owns the boundary. Override per method by redeclaring it on the interface.

## Built-in repository transactions

Spring Data JPA reference (*Transactionality*): methods inherited from **`CrudRepository`** through **`SimpleJpaRepository`** run inside a transaction — **`readOnly = true`** for read operations, plain **`@Transactional`** (defaults) for writes.

Fragment-backed repository methods inherit transactional metadata from the fragment implementation.

That gives each repository call a TX boundary even when the service is not annotated — but **multi-step business work** should still be grouped on a **service facade** so all repositories share one unit of work ([[Where is the Transactional annotation used in Spring]]).

```java
public interface OrderRepository extends JpaRepository<Order, Long> {
    // save/delete/findById — transactional via SimpleJpaRepository
}

@Transactional(readOnly = true)
public interface UserRepository extends JpaRepository<User, Long> {

    List<User> findByLastname(String lastname);

    @Modifying
    @Transactional // overrides readOnly = false for this write
    @Query("delete from User u where u.active = false")
    void deleteInactiveUsers();
}
```

**Listing 1.** Pattern from Spring Data JPA reference — class-level read-only for queries, explicit TX on modifying queries.

## When you add or override `@Transactional`

| Case | Spring Data behavior |
| --- | --- |
| Inherited CRUD from `SimpleJpaRepository` | Transactional by default |
| Declared query / derived methods | **No** TX unless you annotate the interface or call from a `@Transactional` service |
| Tune timeout / propagation on a CRUD method | **Redeclare** the method on your interface with `@Transactional` |
| `@Modifying` JPQL | Needs a write transaction — override `readOnly` on that method |

Attributes are the standard Spring ones — [[What is the Spring Transactional annotation and its parameters]]. Propagation on a repository method participates in an outer service TX under **`REQUIRED`** — [[What is transaction propagation in Spring Data]].

```d2
direction: right
svc: "@Transactional\nservice (facade)" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
repo: "Repository method\njoins or starts TX" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
em: "EntityManager /\nJDBC in same TX" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}

svc -> repo -> em
```

**Fig. 1.** Prefer one service-level boundary; repository TX defaults are per-call fallbacks.

> [!warning] `readOnly = true` is a hint, not a security gate
> Spring Data docs: some databases still allow writes in a read-only transaction. The flag optimizes JDBC/JPA (for example Hibernate `FlushMode.NEVER` on read-only) — it does not block a mistaken `@Modifying` query unless you configure the method correctly.

> [!warning] Repository `@Transactional` ≠ replace service boundaries
> Two `save` calls on different repositories without a service TX can commit separately. Use a **`@Transactional` service** for atomic multi-repository updates.

> [!warning] Interface-only annotations and AspectJ
> Spring Framework recommends **`@Transactional` on concrete service classes**. Interface annotations on repositories work with default proxies; service-layer concrete classes remain the safer interview answer.

> [!tip] Interview answer
> **Spring Data reuses Spring’s `@Transactional`. CRUD from `SimpleJpaRepository` is already transactional; custom queries need it on the repo interface or a transactional service.** Mark read repositories `readOnly = true`; give `@Modifying` writes their own non-read-only TX. Business units of work belong on the service, not scattered per repository call.
