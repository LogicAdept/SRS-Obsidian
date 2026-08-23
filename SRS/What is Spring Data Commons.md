<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What is Spring Data Commons?

> [!abstract] Short answer
> **Spring Data Commons** is the shared foundation of the Spring Data project: store-agnostic repository abstractions (`Repository`, `CrudRepository`, paging/sorting, Query by Example, Querydsl fragments, …) that every module reuses. It does **not** talk to a database by itself — JPA, MongoDB, Redis, and siblings supply the store-specific implementations.

## What lives in commons

Commons applies core Spring ideas to data-access layers across relational and non-relational stores. The programming model you learn once includes:

- Marker **`Repository<T, ID>`** and **`CrudRepository`** / **`ListCrudRepository`**
- **`PagingAndSortingRepository`** / **`ListPagingAndSortingRepository`**
- Query method derivation rules, **`Page`/`Sort`/`Pageable`**
- Extensions such as **Query by Example** and **`QuerydslPredicateExecutor`**

```java
public interface OrderRepository extends CrudRepository<Order, Long> {
  List<Order> findByStatus(String status);
}
```

**Listing 1.** Commons-level contract; a store module (e.g. Spring Data JPA) generates the implementation.

```d2
direction: right
commons: "Spring Data Commons\nRepository, CRUD, Page…" {
  style.fill: "#e3f2fd"
}
jpa: "Spring Data JPA" {
  style.fill: "#fff3e0"
}
mongo: "Spring Data MongoDB" {
  style.fill: "#e8f5e9"
}
redis: "Spring Data Redis" {
  style.fill: "#f3e5f5"
}

commons -> jpa
commons -> mongo
commons -> redis
```

**Fig. 1.** One shared programming model; each store module keeps that database’s traits (`JpaRepository`, `MongoTemplate`, …).

## Umbrella vs one JAR

“Spring Data” is an **umbrella**: Commons plus modules (JPA, MongoDB, Redis, REST, Cassandra, Elasticsearch, …). Adding commons alone does not persist anything. Store modules extend commons interfaces (`JpaRepository` builds on the CRUD/paging story) and map them to `EntityManager`, Mongo drivers, Redis connections, and so on.

> [!warning] Commons is not a multi-database driver
> There is no single Commons JAR that speaks SQL, BSON, and Redis protocols. You depend on the **module** for each store. Multiple modules on the classpath need unambiguous repository binding (module-specific base interfaces).

> [!warning] `JpaRepository` is not in Commons
> Shared pieces (`CrudRepository`, query derivation) live in Commons. **`JpaRepository`**, flush helpers, and JPA `@Query` semantics live in **Spring Data JPA**. Same pattern for Mongo/Redis-specific types.

> [!tip] Interview answer
> Spring Data Commons is the shared repository abstraction — `Repository`, CRUD, paging, and query-method rules — used by every Spring Data store module. The umbrella project then adds JPA, MongoDB, Redis, and others that implement those contracts for a concrete database. Commons alone does not connect to a data store.

See [[What is the Spring Data umbrella project]], [[What is a CrudRepository]], and [[What are Spring Data Repository interfaces]].
