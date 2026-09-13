<!--
reps: 0
priority: 0
-->
#Persistence/Caching #Java/Persistence/Hibernate/Cache #SRS

# What are Hibernate first and second level cache tiers?

> [!abstract] Short answer
> Hibernate has **two cache tiers**. The **first-level cache is the persistence context**: the **managed entity instances** on one open **`Session` / `EntityManager`**. It is **always on**, scoped to that session, and gives **identity** (same id → same Java object) plus **dirty checking**. The **second-level cache** is **optional**, **shared by every session of a `SessionFactory`**, and stores **destructured state** (attribute tuples), plus optionally **query result ids**. It is **off** until you plug in a **`RegionFactory`** and mark types **`@Cacheable` / `@Cache`**. L2 is not “L1 but bigger”: different scope, different payload, and it **bypasses the database’s concurrency control**.

## First-level: the persistence context

`org.hibernate.Cache` names L1 explicitly: the collection of **managed instances** associated with an **open `Session`**. Architecture: the session **wraps a JDBC `Connection`** and keeps this cache for **navigation and lookup by identifier**. Load or `persist` puts the instance there until the session ends, you `detach`/`evict`, or you `clear()`.

Inside one context:

- **Identity** — two `find`s for the same id return the **same** object; no second SELECT while it stays managed.
- **Dirty checking** — mutate managed fields; **flush** writes `INSERT`/`UPDATE`/`DELETE`. SQL is often **not** synchronous with the Java call.
- **Hard references** — a long session that loads a huge graph **pins** it in RAM.

A **new** transaction / session starts with an **empty** L1. Nothing carries over automatically. That is not a bug in L1.

```java
sessionFactory.inTransaction(session -> {
  User a = session.find(User.class, 1L);
  User b = session.find(User.class, 1L);
  // a == b   L1 identity
  a.setEmail("new@example.com"); // dirty; UPDATE on flush
});
// next transaction: new Session, empty L1 — find hits DB (or L2 if enabled)
```

**Listing 1.** Conceptual: L1 identity and dirty checking live only inside that `Session`.

## Second-level: `SessionFactory` shared store

L2 sits **outside** any one persistence context. Hibernate **does not** ship a production cache backend; it integrates one through **`RegionFactory`** (`hibernate.cache.region.factory_class`, e.g. `jcache`, `infinispan`). Default factory is **`NoCachingRegionFactory`** — caching **disabled**. `hibernate.cache.use_second_level_cache` is then **true only when a real provider is set**.

Only entities and collection roles annotated **`@Cacheable` or `@Cache`** are eligible. JPA **`SharedCacheMode`** default is **`ENABLE_SELECTIVE`**: do not turn caching on “by accident” (`ALL` / `DISABLE_SELECTIVE` are discouraged). Payload is a **tuple of attribute values**, not a live object — another session **reconstitutes** a **new** managed instance into **its** L1. Direct **entity references** in L2 exist only as an opt-in for **immutable** types (`hibernate.cache.use_reference_entries`).

`RegionFactory` builds named **regions**:

| Region kind | Holds |
| --- | --- |
| Domain data | Entity / collection state |
| Query results | Cached query result sets (usually **ids** / value types) |
| Timestamps | Used to decide whether a cached query result is **stale** |

Default region name is the **entity class or collection role**; `@Cache(region=…)` overrides. Sharing one region across types means **one eviction** wipes **all** of them.

```d2
direction: right
s1: "Session A\nL1: live instances" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
s2: "Session B\nL1: live instances" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
l2: "SessionFactory L2\nRegionFactory regions\ntuples / query ids" {
  width: 260
  height: 120
  style.fill: "#fff3e0"
}
db: "Database" {
  width: 140
  height: 80
  style.fill: "#e8f5e9"
}

s1 -> l2
s2 -> l2
l2 -> db
s1 -> db
s2 -> db
```

**Fig. 1.** L1 is per session and always on; L2 is shared, optional, and not a Java-identity map.

### Query cache (not a third “level”)

`hibernate.cache.use_query_cache` defaults to **`false`**. After it is on, **each** query still needs `setCacheable(true)` (and optional `setCacheRegion`). The query cache stores **identifiers** (and scalars), **not** full entity state. If those entities are **not** in L2 when the result is reused, Hibernate **loads them from the database** — you paid for a cache hit that still hits SQL. Match query cacheability with entity `@Cache`.

### Concurrency on L2

`@Cache(usage=…)` picks **`CacheConcurrencyStrategy`**. L2 **shares state across transactions** and **bypasses** DB locking/MVCC, so it can **undermine ACID**. Put **read-mostly** data there.

| Strategy | Use when |
| --- | --- |
| **`READ_ONLY`** | Immutable / reference data; **update throws** |
| **`NONSTRICT_READ_WRITE`** | Rare concurrent updates; **no locks**; can still see stale during commit |
| **`READ_WRITE`** | Concurrent updates possible; **soft locks**; **versioned** entities; not serializable isolation |
| **`TRANSACTIONAL`** | Frequent writes; cache provider cooperates via **JTA/XA** |

Programmatic API: `SessionFactory.getCache()` (`org.hibernate.Cache`) — `containsEntity`, `evictEntityData`, `evictQueryRegion`. Eviction is a **hard** remove **outside** the current transaction. L2 **never** sees JDBC or other-process updates; expire or evict yourself.

```java
@Entity
@Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_ONLY, region = "countries")
class Country { @Id String code; String name; }
```

**Listing 2.** Conceptual: selective L2 for immutable reference data; still requires a configured `RegionFactory`.

> [!warning] L1 `clear()` is not L2 eviction, and L2 is not a cluster-safe JDBC cache
> `session.clear()` drops **this** persistence context only. Another transaction still has an empty L1 and will miss unless L2 is on **and** the type is cacheable. L2 will happily return **stale tuples** after a bulk SQL update, a second application, or a missed collection side (`auto_evict_collection_cache` defaults **off**). Treat L2 as **explicit**, selective, and **concurrency-policy-required** — not “turn on Ehcache and forget it.”

> [!tip] Interview answer
> First-level cache is the persistence context on the current Session: always on, same id same instance, dirty checking at flush, gone when the session ends. Second-level cache is optional, SessionFactory-wide, stores disassembled state through a RegionFactory, and only for types you mark cacheable. Query cache is an extra switch on L2 that stores ids, so the entities themselves still need to be in L2. I do not use L2 as a substitute for understanding isolation — it can fight ACID if the data is write-heavy.

See [[How does the Hibernate first-level cache work in Spring]], [[What is Hibernate second level cache and its main components]], [[What is the Hibernate query cache and when does it help]], [[What is Hibernate SessionFactory]], and [[What advantages does Hibernate provide over plain JDBC]].
