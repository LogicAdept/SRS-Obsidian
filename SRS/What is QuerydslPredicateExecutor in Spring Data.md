<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What is QuerydslPredicateExecutor in Spring Data?

> [!abstract] Short answer
> **`QuerydslPredicateExecutor<T>`** is a Spring Data repository **fragment** that runs **Querydsl `Predicate`** instances: type-safe dynamic filters via generated **Q-types**. Mix it onto your repository; it is **not** part of `CrudRepository` by default.

## Mixing it in

Several Spring Data modules integrate Querydsl through this interface. Extend it next to your store repository:

```java
interface UserRepository
    extends JpaRepository<User, Long>, QuerydslPredicateExecutor<User> {
}
```

**Listing 1.** Explicit mix-in (Spring Data Commons: Spring Data Extensions).

Then build predicates from generated metamodel classes (e.g. `QUser`) and call executor methods:

```java
QUser user = QUser.user;
Predicate predicate = user.firstname.equalsIgnoreCase("dave")
    .and(user.lastname.startsWithIgnoreCase("mathews"));

Iterable<User> users = userRepository.findAll(predicate);
Optional<User> one = userRepository.findOne(predicate);
long n = userRepository.count(predicate);
```

**Listing 2.** Type-safe AND of Querydsl predicates → `findAll` / `findOne` / `count`.

Also available: `exists`, sorted/paged `findAll`, Querydsl `OrderSpecifier`s, and fluent `findBy(predicate, queryFunction)` for projection/limit. Web apps can bind request params to a `Predicate` with **`@QuerydslPredicate`** (optional `QuerydslBinderCustomizer`).

```d2
direction: right
qtype: "Generated QUser\n(APT / codegen)" {
  style.fill: "#e3f2fd"
}
pred: "com.querydsl…Predicate" {
  style.fill: "#fff3e0"
}
exec: "QuerydslPredicateExecutor" {
  style.fill: "#e8f5e9"
}
store: "JPA / Mongo / …" {
  style.fill: "#f3e5f5"
}

qtype -> pred -> exec -> store
```

**Fig. 1.** Q-types produce predicates; the executor runs them against the store module.

## Compared to other dynamic options

| Approach | Strength |
| --- | --- |
| Querydsl + this executor | Compile-time property safety |
| [[What is Query by Example in Spring Data]] | Probe object, no codegen |
| JPA `Specification` | Criteria API, JPA-only |
| `@Query` / derived methods | Fixed or simple shapes |

> [!warning] Q-types must be on the classpath
> Without Querydsl annotation processing (or equivalent codegen), `QUser` does not exist and the approach does not compile. This is infrastructure, not a free `CrudRepository` feature.

> [!warning] Extra interface, extra setup
> Extending only `JpaRepository` / `MongoRepository` does **not** expose `findAll(Predicate)`. You must mix in `QuerydslPredicateExecutor` and enable Querydsl for the module.

> [!tip] Interview answer
> `QuerydslPredicateExecutor` lets a Spring Data repository execute Querydsl `Predicate`s built from generated Q-classes — type-safe dynamic queries with `findAll`, `findOne`, `count`, and paging. You add it as a second interface on the repository and need the Querydsl metamodel generated. It sits alongside QBE and Specifications as another dynamic-filter option.

See [[What is Query by Example in Spring Data]], [[What are Spring Data JPA Specification queries]], and [[How do you handle dynamic queries in Spring Data JPA]].
