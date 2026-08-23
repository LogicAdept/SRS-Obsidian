<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What is the difference between CrudRepository and PagingAndSortingRepository?

> [!abstract] Short answer
> **`CrudRepository`** exposes **save / find / delete / count**. **`PagingAndSortingRepository`** exposes only **`findAll(Sort)`** and **`findAll(Pageable)`**. Since Spring Data **3.0** they are **sibling fragments** under `Repository` — paging no longer extends CRUD — so you compose both (or use `JpaRepository` / `MongoRepository`) when you need the full surface.

## Side-by-side

| | `CrudRepository` | `PagingAndSortingRepository` |
| --- | --- | --- |
| Purpose | Create, read, update, delete | Sorted / paged `findAll` |
| Key methods | `save`, `findById`, `findAll()`, `delete*`, `count` | `findAll(Sort)`, `findAll(Pageable)` |
| Extends (3.0+) | `Repository` | `Repository` (not CRUD) |
| List variant | `ListCrudRepository` | `ListPagingAndSortingRepository` |

```java
// CRUD only
interface OrderRepository extends CrudRepository<Order, Long> {}

// Paging only — no save/findById unless you also extend CRUD
interface OrderPages extends PagingAndSortingRepository<Order, Long> {}

// Both (Spring Data 3+ style)
interface OrderRepository
    extends PagingAndSortingRepository<Order, Long>, ListCrudRepository<Order, Long> {}
```

**Listing 1.** Choose fragments explicitly; store repositories usually bundle them for you.

```d2
direction: right
marker: "Repository" {
  style.fill: "#e3f2fd"
}
crud: "CrudRepository\nsave / find / delete" {
  style.fill: "#fff3e0"
}
page: "PagingAndSortingRepository\nfindAll(Sort/Pageable)" {
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

**Fig. 1.** Separate commons fragments; module repositories compose both.

## Practical choice

- Need only CRUD → `CrudRepository` / `ListCrudRepository`.
- Need page metadata (`Page`) or sorted full scans → add paging fragment or use **`JpaRepository`** / **`MongoRepository`**.
- Pagination is not limited to `findAll(Pageable)`: derived methods can take **`Pageable`** / **`Sort`** parameters too.

> [!warning] Pre–Spring Data 3 dumps are outdated
> Older material says **`PagingAndSortingRepository` extends `CrudRepository`**. That inheritance was **removed** in 3.0. Extending only the paging interface no longer gives you `save` / `delete`.

> [!warning] `findAll()` vs paged `findAll`
> Unpaged `CrudRepository.findAll()` loads the whole table/collection. Prefer `Pageable` (or streaming/scrolling APIs) for large datasets even if you “only” use CRUD elsewhere.

> [!tip] Interview answer
> `CrudRepository` is the CRUD API; `PagingAndSortingRepository` adds sorted and paged `findAll`. Since Spring Data 3 they do not inherit from each other — you extend both or use a store repository like `JpaRepository` that already includes List CRUD plus paging. Page indexes on `PageRequest` are zero-based.

See [[What is a CrudRepository]], [[What is a PagingAndSortingRepository]], and [[What are Spring Data Repository interfaces]].
