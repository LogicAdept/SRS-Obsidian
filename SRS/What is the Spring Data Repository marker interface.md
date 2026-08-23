<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What is the Spring Data Repository marker interface?

> [!abstract] Short answer
> **`Repository<T, ID>`** is the **central marker** in Spring Data Commons: it captures the **domain type** and **id type** and lets Spring discover repository interfaces for bean creation. It declares **no CRUD methods** by itself — you add derived/`@Query` methods, or extend **`CrudRepository`** / store interfaces for a full API.

## Role

```java
public interface Repository<T, ID> {
  // marker — no methods
}
```

**Listing 1.** Empty marker (Spring Data Commons `Repository` Javadoc).

Domain repositories **must** extend `Repository` (or a subtype / `@RepositoryDefinition`). Classpath scanning finds those interfaces and builds proxies. You can **selectively** expose CRUD by declaring methods with the same signatures as `CrudRepository` (`findById`, `save`, …) without inheriting the whole CRUD surface.

```java
@NoRepositoryBean
interface MyBaseRepository<T, ID> extends Repository<T, ID> {
  Optional<T> findById(ID id);
  <S extends T> S save(S entity);
}

interface UserRepository extends MyBaseRepository<User, Long> {
  User findByEmailAddress(EmailAddress email);
}
```

**Listing 2.** Fine-tuned base + derived finder (Spring Data Commons: Defining Repository Interfaces).

```d2
direction: right
marker: "Repository<T,ID>\nmarker" {
  style.fill: "#e3f2fd"
}
crud: "CrudRepository" {
  style.fill: "#fff3e0"
}
page: "PagingAndSortingRepository" {
  style.fill: "#e8f5e9"
}
jpa: "JpaRepository /\nMongoRepository" {
  style.fill: "#f3e5f5"
}

marker -> crud
marker -> page
crud -> jpa
page -> jpa
```

**Fig. 1.** Marker at the root; CRUD and paging are separate fragments (Spring Data 3+); store modules compose them.

## Relation to richer interfaces

- **`CrudRepository`** — save/find/delete/count
- **`PagingAndSortingRepository`** — `findAll(Sort)` / `findAll(Pageable)` (does **not** extend CRUD since 3.0)
- **`JpaRepository`**, **`MongoRepository`**, … — store-specific extras

With multiple Spring Data modules on the classpath, prefer module-specific bases or domain annotations (`@Entity` vs `@Document`) so binding is unambiguous.

> [!warning] Empty marker ≠ no queries
> Extending only `Repository` still allows **derived query methods** and `@Query`. You simply omit the bulk CRUD API you do not want to expose (useful for read-only or security-sensitive APIs).

> [!warning] `@NoRepositoryBean` on intermediate bases
> Shared base interfaces that still have type variables must be annotated **`@NoRepositoryBean`**, or Spring Data may try (and fail) to instantiate them.

> [!tip] Interview answer
> `Repository<T,ID>` is Spring Data’s marker interface that ties a domain type to an id type for scanning and proxies. It has no methods. `CrudRepository` and store interfaces build on it. I can extend the marker alone and declare only the methods I need, matching CRUD signatures when I want those operations routed to the store implementation.

See [[What is a CrudRepository]], [[What is the difference between CrudRepository and PagingAndSortingRepository]], and [[What is Spring Data Commons]].
