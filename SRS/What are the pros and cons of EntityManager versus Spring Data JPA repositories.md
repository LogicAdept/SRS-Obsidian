<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Persistence/JPA #SRS

# What are the pros and cons of EntityManager versus Spring Data JPA repositories?

> [!abstract] Short answer
> **`EntityManager`** is the JPA API: full control over persist/merge/flush, Criteria, and JPQL. **Spring Data JPA repositories** generate CRUD and query methods on top of that `EntityManager`, cutting boilerplate. Prefer repositories for common access; drop to `EntityManager` (or a custom repository fragment) when you need control repositories do not express cleanly.

## Trade-offs

| | `EntityManager` | Spring Data repositories |
| --- | --- | --- |
| Pros | Exact JPA control; complex Criteria/JPQL; clear persistence context ops | Less CRUD code; derived/`@Query` methods; paging/QBE helpers |
| Cons | More boilerplate per entity; easy to reimplement the same DAOs | Less obvious for exotic queries; abstractions can hide flush/merge costs |
| Fit | Custom algorithms, bulk Criteria, multi-EM setups | Standard CRUD and named finders |

Repositories are not a second ORM: `CrudRepository.save` delegates to **`persist` or `merge`** on the underlying `EntityManager` (Spring Data JPA “Persisting Entities”).

```java
// Repository — generated
userRepository.findByEmail(email);

// EntityManager — explicit
em.createQuery("select u from User u where u.email = :email", User.class)
  .setParameter("email", email)
  .getResultList();
```

**Listing 1.** Same persistence unit; different call styles.

When a method outgrows derived queries, Spring Data’s supported escape hatch is a **custom repository fragment** that injects `EntityManager` / `JpaContext` — not abandoning repositories entirely.

```d2
direction: right
svc: "Service\n@Transactional" {
  style.fill: "#e3f2fd"
}
repo: "JpaRepository\nproxy" {
  style.fill: "#fff3e0"
}
em: "EntityManager" {
  style.fill: "#e8f5e9"
}
db: "Database" {
  style.fill: "#f3e5f5"
}

svc -> repo -> em -> db
svc -> em
```

**Fig. 1.** Typical stack: services orchestrate; repositories use `EntityManager`; custom code can use `EntityManager` directly.

## Transactions

CRUD methods inherit transaction settings from `SimpleJpaRepository` (reads often `readOnly`). Declared query methods do **not** get transactions by default unless you annotate them. Spring Data JPA docs still recommend declaring **unit-of-work** boundaries on a service/facade so multiple repository calls share one transaction.

> [!warning] “Repositories lack flexibility” is overstated
> You keep flexibility via `@Query`, Specifications, Querydsl, and **custom implementations** that use `EntityManager`. The real cost of repositories is accidental N+1 / wrong `save` semantics when you ignore JPA rules — not a hard ceiling on query power.

> [!warning] Direct `EntityManager` still needs a persistence context
> Injecting `EntityManager` outside an active transaction/persistence context fails or detaches work. Same transaction rules as repository calls — Spring does not waive JPA session requirements.

> [!tip] Interview answer
> I use Spring Data JPA repositories for CRUD and simple queries because they sit on `EntityManager` and remove boilerplate. For complex Criteria, bulk operations, or specialty APIs I inject `EntityManager` in a custom repository fragment. It is not either/or — repositories are a layer over JPA, and service-level `@Transactional` still defines the business boundary.

See [[What is Spring Data JPA]], [[How do you implement a custom repository method]], and [[What is the difference between Spring Data JPA and using Hibernate directly]].
