<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Persistence/Hibernate/Cache #SRS

# How does the Hibernate first-level cache work in Spring?

> [!abstract] Short answer
> Hibernate’s **first-level cache is the persistence context**: the set of **managed entity instances** on an open **`Session` / `EntityManager`**. In a typical Spring app that is **one context per `@Transactional` unit of work**. Same id → same Java instance; changes are **dirty-checked** and flushed. It is **not** shared across transactions — that is the optional **second-level** cache.

## What “L1” actually is

Hibernate’s `Cache` Javadoc: the first-level cache **is** the persistence context — managed entities tied to an open `Session`. Once loaded or persisted, the instance lives there until the session ends, the entity is detached/evicted, or you `clear()`.

```d2
direction: right
tx: "@Transactional\nservice method" {
  style.fill: "#e3f2fd"
}
em: "EntityManager / Session\n(= L1 / persistence context)" {
  style.fill: "#fff3e0"
}
map: "id → managed instance\ndirty checking" {
  style.fill: "#e8f5e9"
}
db: "Database\n(on flush / commit)" {
  style.fill: "#f3e5f5"
}

tx -> em -> map
map -> db
```

**Fig. 1.** Spring transaction scope owns the persistence context that acts as L1.

## Behavior that interviews care about

- **Identity guarantee** inside one context: two `find`/`getReference` calls for the same id return the **same** managed instance (no second SELECT for that id while it stays managed).
- **Dirty checking**: mutate managed fields; on flush Hibernate synchronizes SQL. No explicit “update” API required for managed entities.
- **Scope**: ends with the transaction (or OSIV-extended request if Open EntityManager in View keeps the EM open). A **new** transaction → **new** empty L1; nothing carries over automatically.
- **Memory**: the context holds hard references — long transactions that load huge graphs keep everything in RAM until clear/detach/end.

```java
@Transactional
void demo(EntityManager em) {
  User a = em.find(User.class, 1L);
  User b = em.find(User.class, 1L);
  // a == b  (same managed instance in this persistence context)
  a.setEmail("new@example.com"); // dirty; UPDATE on flush
}
```

**Listing 1.** Conceptual identity + dirty checking inside one Spring transaction.

## L1 vs L2

| | First-level | Second-level |
| --- | --- | --- |
| Scope | One `Session` / EM | Shared across sessions (`SessionFactory`) |
| Default | Always on | Off unless configured (`RegionFactory`, etc.) |
| Stores | Live managed objects | Destructured state / query results |

`clear()` empties L1 for that session; it is not “flush.” `saveAndFlush` forces SQL sync but entities remain managed in L1.

> [!warning] Do not expect L1 across transactions
> Caching “I already loaded User 1 in the previous request” is **not** L1. That needs application caching or a configured **second-level** cache.

> [!tip] Interview answer
> Hibernate L1 is the persistence context on the current Session/EntityManager — in Spring, usually the `@Transactional` boundary. Same id, same instance, dirty checking at flush. It does not span transactions; L2 is the optional shared cache.

See [[What is the difference between save and persist in JPA with Spring Data]], [[What is the difference between save and saveAndFlush in Spring Data JPA]], and [[What is Open Session In View in Spring]].
