<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS

# What is the difference between findById and getOne in Spring Data JPA?

> [!abstract] Short answer
> **`findById`** loads the entity now and returns **`Optional`** (empty if missing). **`getOne`** (deprecated) — now **`getReferenceById`** — returns a **lazy reference** (often a proxy) without guaranteeing a DB hit; a missing id typically fails with **`EntityNotFoundException` on first property access**, not at the call site.

## Eager optional load vs reference

| | `findById(id)` | `getOne` / `getReferenceById(id)` |
| --- | --- | --- |
| API | `CrudRepository` | `JpaRepository` |
| Return | `Optional<T>` | `T` (reference) |
| Load | Fetch (or return empty) | Provider-dependent proxy / reference |
| Missing id | `Optional.empty()` | Often deferred `EntityNotFoundException` |

```java
Optional<User> loaded = userRepository.findById(1L);

User ref = userRepository.getReferenceById(1L); // preferred over getOne / getById
// touching ref.getName() may hit the DB or throw if id does not exist
```

**Listing 1.** Real load vs reference (Spring Data JPA `JpaRepository` / `CrudRepository`).

`getOne` and `getById` are **deprecated**; docs point to **`getReferenceById`**. All three share the same reference semantics: providers usually always return an instance and throw on first access for invalid ids; some may reject earlier.

```d2
direction: right
find: "findById" {
  style.fill: "#e3f2fd"
}
opt: "Optional\nentity or empty" {
  style.fill: "#e8f5e9"
}
ref: "getReferenceById\n(getOne deprecated)" {
  style.fill: "#fff3e0"
}
proxy: "Lazy reference\naccess may throw" {
  style.fill: "#f3e5f5"
}

find -> opt
ref -> proxy
```

**Fig. 1.** Choose `findById` when you need a loaded entity or a clear miss; use a reference when you only need an association target by id.

## When to use which

Use **`findById`** for “load or handle missing.” Use **`getReferenceById`** when assigning a foreign-key association and you already know the id exists (or accept deferred failure) — avoids an unnecessary select before `persist`/`merge` of the parent.

> [!warning] Touching a bad reference is late
> `getOne(999)` may return without error. The exception appears when you **access** the proxy (or when the provider validates). That surprises code that assumed “got a `User`, so it exists.”

> [!warning] Open Session In View / detached proxies
> A reference obtained in a transaction can fail later if the persistence context is closed before initialization. Prefer `findById` when you will read fields outside a controlled session.

> [!tip] Interview answer
> `findById` returns `Optional` after loading the row (or empty). `getOne` — replaced by `getReferenceById` — returns a lazy reference that may throw `EntityNotFoundException` only when first used. I use `findById` for real reads and references mainly to set associations by id without an extra fetch.

See [[What is Spring Data JPA]], [[How does the Hibernate first-level cache work in Spring]], and [[What is the difference between save and persist in JPA with Spring Data]].
