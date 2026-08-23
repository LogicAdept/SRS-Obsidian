<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What is a CrudRepository?

> [!abstract] Short answer
> **`CrudRepository<T, ID>`** is the Spring Data **commons** interface for basic **create/read/update/delete** on a domain type. You extend it (or a module-specific subinterface such as **`JpaRepository`** / **`MongoRepository`**) and Spring generates the implementation at runtime.

## Contract and placement

Defined in **`spring-data-commons`**, `CrudRepository` extends the marker **`Repository<T, ID>`** and exposes standard persistence operations:

| Method | Role |
| --- | --- |
| `save` / `saveAll` | Persist new or changed entities |
| `findById` | Load by primary key (`Optional`) |
| `existsById` | Presence check without loading |
| `findAll` / `findAllById` | Load many (`Iterable`) |
| `deleteById` / `delete` / `deleteAll*` | Remove by id, entity, or bulk |
| `count` | Row/document count |

```java
public interface StudentRepository extends CrudRepository<Student, Long> {
  // optional derived methods: List<Student> findByLastName(String lastName);
}
```

**Listing 1.** Empty extension is enough for generated CRUD (Spring Data Commons `CrudRepository`).

The interface is **store-agnostic**: the same shape backs JPA, MongoDB, Redis, JDBC, and other modules. Each module maps calls to its native API (`EntityManager`, `MongoTemplate`, …).

```d2
direction: right
repo: "CrudRepository<T,ID>\nspring-data-commons" {
  style.fill: "#e3f2fd"
}
jpa: "JpaRepository" {
  style.fill: "#fff3e0"
}
mongo: "MongoRepository" {
  style.fill: "#e8f5e9"
}
impl: "Generated proxy\nat runtime" {
  style.fill: "#f3e5f5"
}

repo -> jpa -> impl
repo -> mongo -> impl
```

**Fig. 1.** Shared CRUD contract; module repositories add paging, flushing, and store-specific behavior.

## Relation to richer interfaces

Module repositories **extend** (and therefore include) `CrudRepository` rather than replacing it:

- **`JpaRepository`** — JPA extras: flush, batch delete, `getReferenceById`, …
- **`MongoRepository`** — Mongo paging/sorting on top of CRUD

Spring Data 3+ also offers **`ListCrudRepository`** with **`List`** return types instead of bare **`Iterable`** for `findAll` / `saveAll`. Prefer **`JpaRepository`** / **`MongoRepository`** in applications unless you intentionally want the minimal surface.

> [!warning] `findAll()` returns `Iterable`
> On **`CrudRepository`**, `findAll()` is **`Iterable<T>`**, not `List`. For a `List`, use **`ListCrudRepository`**, **`JpaRepository`**, or collect in application code. Loading all rows/documents is risky on large tables.

> [!warning] Lifecycle and locking still apply
> Docs note that delete/update may load entities first to fire lifecycle events, and optimistic locking can fail on modifying calls. Bulk deletes are not always a single SQL statement — behavior is module-specific.

> [!tip] Interview answer
> `CrudRepository` is the shared Spring Data CRUD API in commons: save, findById, existsById, findAll, delete*, count. You declare an empty interface extending it and get an implementation at runtime. JPA and Mongo modules expose richer subinterfaces, but they all build on this contract.

See [[What is the difference between CrudRepository and PagingAndSortingRepository]], [[What is Spring Data JPA]], and [[What are Spring Data Repository interfaces]].
