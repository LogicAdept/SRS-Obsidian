<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Persistence/JPA #SRS

# What is the difference between JpaRepository CrudRepository?

> [!abstract] Short answer
> **`CrudRepository`** is the **store-agnostic** CRUD API (`save`, `findById`, `findAll` → `Iterable`, `delete`, …). **`JpaRepository`** is the **JPA-specific** Spring Data interface: it extends **`ListCrudRepository`** and **`ListPagingAndSortingRepository`** (so you get **`List`** plus paging/sort) and **`QueryByExampleExecutor`**, and it adds **flush / save-and-flush** and **batch deletes**. CRUD itself: [[What is a CrudRepository]]. Pagination sibling: [[What is the difference between CrudRepository and PagingAndSortingRepository]].

## Generic CRUD versus the JPA module API

Spring Data’s marker is `Repository<T, ID>`. `CrudRepository` adds create/read/update/delete. `ListCrudRepository` (Spring Data **3.0**) is the same CRUD with **`List`** instead of **`Iterable`** where that matters. Persistence-technology interfaces such as `JpaRepository` sit on top of that generic stack and expose store features. Repository family: [[What are Spring Data Repository interfaces]].

**Current `JpaRepository` (Spring Data JPA 4.x):** `extends ListCrudRepository, ListPagingAndSortingRepository, QueryByExampleExecutor`. That is **not** the old chain `JpaRepository extends PagingAndSortingRepository extends CrudRepository`. Since **3.0**, `PagingAndSortingRepository` **no longer extends** `CrudRepository` — you extend **both** if you want CRUD and paging without `JpaRepository`. What paging is: [[What is a PagingAndSortingRepository]].

```d2
direction: down
repo: "Repository<T,ID>\nmarker" {
  width: 180
  height: 40
}
crud: "CrudRepository\nIterable CRUD" {
  width: 200
  height: 40
}
listcrud: "ListCrudRepository\nList CRUD" {
  width: 200
  height: 40
}
pas: "PagingAndSortingRepository" {
  width: 240
  height: 40
}
listpas: "ListPagingAndSortingRepository" {
  width: 260
  height: 40
}
jpa: "JpaRepository\n+ flush, batch delete, getReferenceById" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
repo -> crud
repo -> pas
crud -> listcrud
pas -> listpas
listcrud -> jpa
listpas -> jpa
```

**Fig. 1.** `JpaRepository` is JPA-only. `CrudRepository` is the portable CRUD slice. Paging is a **sibling** of CRUD, not a parent, since Spring Data 3.0.

JPA-only methods on `JpaRepository`: `flush()`, `saveAndFlush`, `saveAllAndFlush`, `deleteAllInBatch` / `deleteAllByIdInBatch`, `getReferenceById` (replaces deprecated `getOne` / `getById`). `getReferenceById` is the Spring Data wrapper for a JPA reference — same late-failure idea as `EntityManager.getReference`: [[What is the difference between get() load() Hibernate]].

```java
interface BookCrud extends CrudRepository<Book, Long> { }           // any Spring Data store
interface BookJpa extends JpaRepository<Book, Long> { }             // JPA: List, page, flush, batch
```

**Listing 1.** Conceptual. Prefer `CrudRepository` / `ListCrudRepository` unless you need JPA flush, batch delete, Example queries, or `getReferenceById`.

> [!warning] Batch delete is not EntityManager.remove
> `deleteAllInBatch` issues **one query**. It **does not** honor JPA **cascade**, **does not** emit lifecycle events, and can leave the **persistence context** out of sync with the database. Flush first if the context has pending state. Ordinary `delete` on `CrudRepository` is the lifecycle-aware path.

> [!warning] Interview sheets still draw the 2.x inheritance line
> `JpaRepository extends PagingAndSortingRepository extends CrudRepository` was the old picture. Today `JpaRepository` extends the **List** CRUD and paging interfaces. `List` return types come from **`ListCrudRepository`**, not from “being JpaRepository” alone.

> [!tip] Interview answer
> CrudRepository is generic Spring Data CRUD and works across stores. JpaRepository is the JPA module API: List CRUD, paging and sort, Query by Example, plus flush and batch deletes. Since Spring Data 3, paging does not extend CRUD, so JpaRepository is how you get both plus JPA extras. Do not use batch delete if you need cascades or entity callbacks.
