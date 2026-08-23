<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What are Spring Data Repository interfaces?

> [!abstract] Short answer
> Spring Data’s **repository interfaces** are typed contracts (`Repository<T, ID>` and extensions) that Spring turns into **proxies** against a store. You declare **what** you need — marker only, CRUD, paging, or store-specific APIs — and add **derived** or **`@Query`** methods; Spring Data Commons defines the shared hierarchy every module builds on.

## The Commons hierarchy

| Interface | Role |
| --- | --- |
| **`Repository<T, ID>`** | Marker: domain type + id type; no CRUD methods |
| **`CrudRepository`** | save / find / delete / count / exists |
| **`ListCrudRepository`** | Same as CRUD; multi-result methods return **`List`** instead of **`Iterable`** |
| **`PagingAndSortingRepository`** | `findAll(Sort)`, `findAll(Pageable)` |
| **`ListPagingAndSortingRepository`** | Paging/sorting with **`List`** where applicable |

Store modules add **`JpaRepository`**, **`MongoRepository`**, and so on — they extend the Commons pieces and expose store-specific extras (`flush`, geo queries, …).

```java
public interface UserRepository extends CrudRepository<User, Long> {
  List<User> findByLastName(String lastName);
  long countByLastName(String lastName);
}
```

**Listing 1.** Typical app repository: inherit CRUD, add derived finders/counts (Spring Data Commons core concepts).

```d2
direction: down
marker: "Repository<T,ID>" {
  style.fill: "#e3f2fd"
}
crud: "CrudRepository\nListCrudRepository" {
  style.fill: "#fff3e0"
}
page: "PagingAndSortingRepository\nListPagingAndSorting…" {
  style.fill: "#e8f5e9"
}
store: "JpaRepository /\nMongoRepository / …" {
  style.fill: "#f3e5f5"
}

marker -> crud
marker -> page
crud -> store
page -> store
```

**Fig. 1.** Marker at the root; CRUD and paging are separate fragments that store interfaces compose.

## Spring Data 3+ composition

Since **Spring Data 3.0**, paging/sorting repositories **no longer extend** CRUD. If you need both, **extend both** (or use a store interface that already combines them, such as many `JpaRepository` setups via `ListCrudRepository` + `ListPagingAndSortingRepository`).

You can stay on the marker alone and declare only the method signatures you want exposed — useful for read-only or minimal APIs. Intermediate base interfaces with type parameters need **`@NoRepositoryBean`**.

> [!warning] Not every store implements every fragment
> Extension interfaces are supported only if the **store module** implements them. Check the module docs before coding against `PagingAndSortingRepository` on an exotic store.

> [!warning] Multiple modules on the classpath
> Prefer store-specific bases (`JpaRepository` vs `MongoRepository`) or unambiguous domain mapping so Spring Data knows which module owns the repository.

> [!tip] Interview answer
> Spring Data repository interfaces start from the `Repository` marker, then `CrudRepository` / `ListCrudRepository` and separate paging interfaces. Store modules specialize them. Since 3.0, paging does not imply CRUD — compose what you need. I declare methods for derivation or `@Query`; Spring generates the proxy.

See [[What is the Spring Data Repository marker interface]], [[What is a CrudRepository]], [[What is the difference between CrudRepository and PagingAndSortingRepository]], and [[What is Spring Data Commons]].
