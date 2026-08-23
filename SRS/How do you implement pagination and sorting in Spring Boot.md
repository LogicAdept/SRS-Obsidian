<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Data #SRS

# How do you implement pagination and sorting in Spring Boot?

> [!abstract] Short answer
> Use Spring Data’s **`Pageable`** / **`Sort`** on repository methods (or `PagingAndSortingRepository` / `JpaRepository`). Build pages with **`PageRequest.of(page, size, sort)`**, return **`Page`** (or cheaper **`Slice`**). In MVC, inject **`Pageable`** and let Spring Data Web bind `page`, `size`, and `sort` query params.

## Repository layer

```java
public interface UserRepository extends JpaRepository<User, Long> {
  Page<User> findByLastName(String lastName, Pageable pageable);
  Slice<User> findByActiveTrue(Pageable pageable);
  List<User> findByLastName(String lastName, Sort sort);
}
```

**Listing 1.** `Pageable`/`Sort` as method parameters (Spring Data query-methods docs).

- **`Page`** — content + total elements/pages (extra **count** query).
- **`Slice`** — content + whether a next slice exists (no full count).
- **`List` + `Pageable`** — range only; no `Page` metadata / no count.

```java
Page<User> page = users.findAll(PageRequest.of(1, 20, Sort.by("lastName")));
```

**Listing 2.** Second page (0-based index), size 20, sorted (Commons core concepts).

Since Spring Data **3.0**, `PagingAndSortingRepository` no longer extends CRUD — `JpaRepository` already composes list CRUD + paging. Prefer `JpaRepository` in Boot apps.

```d2
direction: right
http: "?page=&size=&sort=" {
  style.fill: "#e3f2fd"
}
ctrl: "Controller\nPageable arg" {
  style.fill: "#fff3e0"
}
repo: "Repository\nfind…(Pageable)" {
  style.fill: "#e8f5e9"
}
page: "Page / Slice" {
  style.fill: "#f3e5f5"
}

http -> ctrl -> repo -> page
```

**Fig. 1.** Query params → `Pageable` → repository → paged result.

## Web layer (Boot + Spring Data Web)

With Spring Data Web support, controllers can take `Pageable` directly:

| Param | Meaning |
| --- | --- |
| `page` | 0-based page (default 0) |
| `size` | page size (default 20) |
| `sort` | `property(,ASC\|DESC)` — repeat for multi-sort |

```java
@GetMapping("/users")
Page<User> list(Pageable pageable) {
  return userRepository.findAll(pageable);
}
```

**Listing 3.** Default binding via `PageableHandlerMethodArgumentResolver` (Spring Data web extensions). Customize with `@PageableDefault` or a `PageableHandlerMethodArgumentResolverCustomizer` bean.

## Cost notes

`Page` always pays for a count unless you switch to `Slice`, scrolling/`Window`, or return a limited `List`. Offset pagination (`PageRequest`) gets expensive on deep pages; Spring Data also documents **scrolling** for chunked iteration when offset is a poor fit.

> [!warning] Sort property must be real
> `Sort.by("email")` must map to an entity property (or explicit query). Invalid names fail at query time; unindexed sorts can full-scan large tables.

> [!tip] Interview answer
> I pass `Pageable` into Spring Data methods via `PageRequest.of(page, size, Sort.by(...))`, return `Page` when I need totals or `Slice` when I do not. In Boot MVC I inject `Pageable` and use `page`/`size`/`sort` query params. Since Data 3, paging is a separate fragment from CRUD — `JpaRepository` already includes both.

See [[What is a PagingAndSortingRepository]], [[What is the difference between CrudRepository and PagingAndSortingRepository]], and [[What are Spring Data Repository interfaces]].
