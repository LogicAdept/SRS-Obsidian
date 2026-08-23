<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS

# What is Spring Data JPA?

> [!abstract] Short answer
> **Spring Data JPA** is the Spring Data module that adds **repository support on top of Jakarta Persistence (JPA)**. You declare interfaces such as **`JpaRepository`**; Spring generates implementations that use the JPA **`EntityManager`** (typically Hibernate in Spring Boot) — cutting boilerplate CRUD and query glue without replacing JPA itself.

## Where it sits

Spring Data Commons defines the shared repository model. Spring Data JPA specializes it for relational JPA:

- Derived query methods → JPQL
- `@Query` (JPQL or native SQL)
- Specifications, Query by Example, auditing, locking annotations, …

```java
public interface UserRepository extends JpaRepository<User, Long> {
  List<User> findByLastName(String lastName);
}
```

**Listing 1.** Empty extension of `JpaRepository` plus a derived finder; implementation is generated at runtime (Spring Data JPA reference).

`JpaRepository` extends **`ListCrudRepository`**, **`ListPagingAndSortingRepository`**, and **`QueryByExampleExecutor`**, and adds JPA helpers (`flush`, `saveAndFlush`, batch deletes, `getReferenceById`, …).

```d2
direction: right
app: "Repository interface\nJpaRepository" {
  style.fill: "#e3f2fd"
}
sd: "Spring Data JPA\ngenerated impl" {
  style.fill: "#fff3e0"
}
jpa: "JPA API\nEntityManager" {
  style.fill: "#e8f5e9"
}
prov: "Provider\n(e.g. Hibernate)" {
  style.fill: "#f3e5f5"
}

app -> sd -> jpa -> prov
```

**Fig. 1.** Spring Data JPA is a repository layer over JPA — not a second ORM.

## What it is not

It is **not** a JPA implementation. Hibernate (or EclipseLink, …) remains the provider that maps entities and talks to the database. Spring Boot often auto-configures Hibernate, but the provider is **pluggable**. For “repositories vs raw `EntityManager`,” see [[What are the pros and cons of EntityManager versus Spring Data JPA repositories]] and [[What is the difference between Spring Data JPA and using Hibernate directly]].

> [!warning] Still JPA semantics underneath
> Persistence context, flush, lazy loading, and transactions behave as JPA defines them. Spring Data does not remove N+1 risks or OSIV pitfalls — it only generates repository code on top.

> [!warning] Not “no SQL forever”
> Derived names and `@Query` cover common cases. Complex reporting, bulk DML, and tuning still need explicit JPQL/native SQL, Specifications, or going through `EntityManager`.

> [!tip] Interview answer
> Spring Data JPA provides repository interfaces on top of JPA so I get CRUD, paging, and derived/`@Query` methods without writing DAO boilerplate. It uses the JPA `EntityManager`; Hibernate is the usual provider in Boot but is not Spring Data itself. I still reason about entities, flush, and transactions as JPA concepts.

See [[What is Spring Data Commons]], [[What are derived query methods in Spring Data JPA]], and [[What is a CrudRepository]].
