<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #Java/Spring/Data/JPA #SRS

# What is the difference between save and saveAll in Spring Data?

> [!abstract] Short answer
> **`save(entity)`** persists **one** entity and returns that saved instance. **`saveAll(entities)`** persists an **`Iterable`** of entities and returns the saved collection (same size). Same per-entity save semantics; `saveAll` is the multi-arg API, not a magic bulk SQL shortcut by itself.

## Commons contract

Both live on **`CrudRepository`** (and **`ListCrudRepository`** / store interfaces):

| | `save` | `saveAll` |
| --- | --- | --- |
| Input | one non-null entity | non-null `Iterable`, no null elements |
| Output | the saved entity | saved entities, same size as input |
| Use returned value | yes — instance may change | yes — use the returned iterable |

Javadoc: use the **returned** instance for further work; save may replace the object (e.g. JPA `merge`). Both can throw `IllegalArgumentException` on null input and `OptimisticLockingFailureException` when versioning fails.

```java
User one = users.save(new User("a@example.com"));
List<User> many = users.saveAll(List.of(
    new User("b@example.com"),
    new User("c@example.com")));
```

**Listing 1.** One vs many through the repository API (`ListCrudRepository` returns `List` from `saveAll`).

```d2
direction: right
save: "save(e)" {
  style.fill: "#e3f2fd"
}
all: "saveAll(es)" {
  style.fill: "#fff3e0"
}
loop: "for each: same\nsave path" {
  style.fill: "#e8f5e9"
}
store: "Store / EM" {
  style.fill: "#f3e5f5"
}

save -> store
all -> loop -> store
```

**Fig. 1.** `saveAll` is typically a loop of `save`, not a separate persistence mode.

## JPA behavior

In Spring Data JPA, `SimpleJpaRepository.save` chooses **`persist`** (new) or **`merge`** (existing). **`saveAll`** iterates and calls **`save`** for each element — confirmed in the repository implementation. That means:

- Same new/existing detection per entity
- **Not** automatically one JDBC batch insert; Hibernate batching still needs provider settings (`jdbc.batch_size`, ordered inserts/updates, …)
- `JpaRepository` also offers **`saveAllAndFlush`** = `saveAll` then `flush()`

Prefer `saveAll` when you already have a collection (clearer intent, one transactional boundary in the default `@Transactional` methods). Prefer `save` for a single aggregate.

> [!warning] `saveAll` ≠ guaranteed bulk SQL
> Calling `saveAll` does not by itself emit a single multi-row insert. Under JPA it walks entities one by one; tune the provider for JDBC batching if throughput matters.

> [!warning] Use the returned instances
> Especially after `merge`, continuing with the **input** reference can leave you holding a detached/stale object. Prefer what `save` / `saveAll` return.

> [!tip] Interview answer
> `save` is one entity; `saveAll` is an iterable of the same operation. On JPA, `saveAll` loops `save` (persist or merge each). It is the convenient multi-save API — not automatically a bulk SQL statement unless the provider batches.

See [[What is a CrudRepository]], [[What is the difference between save and saveAndFlush in Spring Data JPA]], and [[What is the difference between save and persist in JPA with Spring Data]].
