<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What is a PagingAndSortingRepository?

> [!abstract] Short answer
> **`PagingAndSortingRepository<T, ID>`** is a Spring Data **commons** fragment that adds **`findAll(Sort)`** and **`findAll(Pageable)`** for sorted and paged reads. Since Spring Data **3.0** it extends **`Repository` only** — not `CrudRepository` — so you combine it with a CRUD interface when you need both.

## Methods

```java
interface PagingAndSortingRepository<T, ID> extends Repository<T, ID> {

  Iterable<T> findAll(Sort sort);

  Page<T> findAll(Pageable pageable);
}
```

**Listing 1.** Official commons contract (Spring Data Commons core concepts).

Typical usage with `PageRequest` (zero-based page index) and `Sort`:

```java
Page<User> page = repository.findAll(
    PageRequest.of(0, 20, Sort.by("lastname").ascending()));

int totalPages = page.getTotalPages();
Pageable next = page.nextPageable();
```

**Listing 2.** First page of 20, sorted; `Page` exposes totals and navigation.

`ListPagingAndSortingRepository` is the variant that returns **`List`** where this interface returns **`Iterable`** for the sorted overload.

```d2
direction: right
marker: "Repository<T,ID>" {
  style.fill: "#e3f2fd"
}
page: "PagingAndSortingRepository\nfindAll(Sort/Pageable)" {
  style.fill: "#fff3e0"
}
crud: "CrudRepository /\nListCrudRepository" {
  style.fill: "#e8f5e9"
}
jpa: "JpaRepository /\nMongoRepository" {
  style.fill: "#f3e5f5"
}

marker -> page
marker -> crud
page -> jpa
crud -> jpa
```

**Fig. 1.** Paging/sorting and CRUD are separate fragments; store repositories compose both.

## Relation to CRUD and module repositories

Before Spring Data 3.0, `PagingAndSortingRepository` **extended** `CrudRepository`. That inheritance was **removed** so you can mix paging with `CrudRepository` or `ListCrudRepository` (or neither). If you extend only `PagingAndSortingRepository`, you do **not** get `save` / `findById`.

In practice, **`JpaRepository`** and **`MongoRepository`** already expose paging/sorting (and CRUD), so applications rarely extend `PagingAndSortingRepository` alone.

> [!warning] Page index is zero-based
> `PageRequest.of(0, 20)` is the **first** page. `PageRequest.of(1, 20)` is the **second** — the commons docs use that form when showing “page 1 of size 20.” Off-by-one bugs are common in API design and interviews.

> [!warning] Extending only paging loses CRUD (Spring Data 3+)
> `interface X extends PagingAndSortingRepository<…>` no longer inherits `save` / `delete`. Extend **both** paging and a CRUD fragment, or use `JpaRepository` / `MongoRepository`.

> [!tip] Interview answer
> `PagingAndSortingRepository` adds sorted and paged `findAll` on top of the repository marker. Since Spring Data 3 it does not extend `CrudRepository`, so you compose both if you need CRUD plus paging. `PageRequest` pages are zero-based, and `JpaRepository`/`MongoRepository` already include this surface.

See [[What is a CrudRepository]], [[What is the difference between CrudRepository and PagingAndSortingRepository]], and [[What are Spring Data Repository interfaces]].
