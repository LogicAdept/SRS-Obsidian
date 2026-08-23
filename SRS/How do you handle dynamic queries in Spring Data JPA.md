<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS

# How do you handle dynamic queries in Spring Data JPA?

> [!abstract] Short answer
> When filter combinations are chosen at runtime, build predicates programmatically: **`Specification` + `JpaSpecificationExecutor`**, **Querydsl** via `QuerydslPredicateExecutor`, or the JPA Criteria API in a custom repository. Static `@Query` JPQL and derived method names are fixed at compile time.

## Choose the mechanism

| Approach | Dynamic at runtime? | Typical use |
|----------|---------------------|-------------|
| `@Query` JPQL | No (unless you branch to different methods) | Stable query text |
| Derived `findBy…` | No | Simple, fixed predicates |
| `Specification` | Yes | Optional filters, composable AND/OR |
| Querydsl `Predicate` | Yes | Type-safe criteria with generated `Q` types |
| Custom `EntityManager` | Yes | Full control in `{Repo}Impl` fragment |

Extend the repository with **`JpaSpecificationExecutor<T>`** before `findAll(Specification)` / `findBy(spec, …)` work.

```java
public interface UserRepository
    extends JpaRepository<User, Long>, JpaSpecificationExecutor<User> {}

public class UserSpecifications {

  static Specification<User> nameEquals(String name) {
    return (root, query, cb) ->
        name == null ? cb.conjunction()
                     : cb.equal(root.get("name"), name);
  }

  static Specification<User> activeOnly() {
    return (root, query, cb) -> cb.isTrue(root.get("active"));
  }
}

List<User> users = repository.findAll(
    Specification.where(UserSpecifications.nameEquals(filter.name()))
        .and(UserSpecifications.activeOnly()));
```

**Listing 1.** Composable specifications with optional clauses (Spring Data JPA Specifications reference).

Querydsl follows the same idea with generated **`QUser`** types:

```java
public interface UserRepository
    extends JpaRepository<User, Long>, QuerydslPredicateExecutor<User> {}

QUser user = QUser.user;
Predicate predicate = user.name.eq("John").and(user.active.isTrue());
List<User> users = repository.findAll(predicate);
```

**Listing 2.** Type-safe dynamic predicates through Querydsl (requires annotation processing / `Q` class generation).

```d2
direction: down
dto: "Search DTO\n(nullable fields)" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
build: "Specification / Querydsl\nPredicate" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
repo: "JpaSpecificationExecutor\nfindAll / findBy" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
jpa: "JPA Criteria API\n→ SQL" {
  width: 200
  height: 70
  style.fill: "#f3e5f5"
}

dto -> build -> repo -> jpa
```

**Fig. 1.** Runtime filters become Criteria predicates executed through the repository executor.

Spring Data JPA 4.x also exposes a **fluent** `findBy(spec, q -> q.sortBy(…).page(…))` API for projections and paging on specifications.

> [!warning] `@Query` is not a runtime builder
> A single `@Query` string does not add optional `WHERE` branches unless you maintain multiple methods or move logic into Specifications/Querydsl. Derived names like `findByNameAndStatus` explode combinatorially when filters are optional.

See [[What are Spring Data JPA Specification queries]], [[What is QuerydslPredicateExecutor in Spring Data]], and [[How do you define a native query in Spring Data JPA]].

> [!tip] Interview answer
> For dynamic JPA search I extend `JpaSpecificationExecutor`, build a `Specification` per optional filter, combine them with `Specification.where(…).and(…)`, and call `findAll`. Querydsl with `QuerydslPredicateExecutor` is the type-safe alternative. Plain `@Query` and derived finders are for fixed predicates, not runtime filter matrices.
