<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #SRS

# How would you explain Hibernate?

> [!abstract] Short answer
> **Hibernate ORM** is a Java **object/relational mapper**: it maps domain classes to relational tables, runs queries, and flushes in-memory changes inside transactions. It is a complete **Jakarta Persistence** implementation (`EntityManager` / `EntityManagerFactory`) and also a **native** API (`Session` extends `EntityManager`, `SessionFactory` extends `EntityManagerFactory`). It does **not** hide SQL.

## ORM plus a JPA provider

Hibernate sits between the application and JDBC. `SessionFactory` is a thread-safe, expensive mapping of the domain model (one per database); it creates `Session`s and holds shared services, including the **second-level cache**. A `Session` is a short-lived, **not thread-safe** unit of work: it wraps a JDBC connection and a **persistence context** (the first-level cache). JPA names the same pair `EntityManagerFactory` / `EntityManager`. Spec vs product: [[What is the Java Persistence API JPA]], [[What is the difference between JPA as a specification and Hibernate]].

You persist POJO entities with JPA annotations most of the time, and Hibernate-only annotations when you need extra mapping power. HQL/JPQL is an object-oriented dialect of SQL; native SQL is still in scope.

```d2
direction: down
app: "application" {
  width: 160
  height: 40
}
sf: "SessionFactory\n(thread-safe, L2 cache)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
sess: "Session / EntityManager\npersistence context (L1)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
db: "relational database" {
  width: 180
  height: 40
}
app -> sess
sf -> sess
sess -> db
```

**Fig. 1.** `SessionFactory` is shared. Each `Session` has its own first-level cache and talks to the database.

## Entity states on a Session

With respect to one open `Session`, an instance is **transient** (never persistent, not associated), **persistent** / managed (associated; dirty-checked and flushed), or **detached** (was persistent, session closed, `detach`/`clear`, or deserialized). `remove` marks a persistent instance for deletion; after flush it is gone and the object is treated as transient again. JPA also names that in-between state **removed**.

Inside one session, persistent identity (type + id) matches Java identity: `find` twice with the same id returns the **same instance**. Distinct sessions use distinct instances for the same row.

```java
try (Session session = sessionFactory.openSession()) {
    session.beginTransaction();
    Book first = session.find(Book.class, 1L);
    Book again = session.find(Book.class, 1L);
    // first == again  — at most one persistent instance per id in this Session
    session.persist(new Book()); // transient → persistent
    session.getTransaction().commit();
} // Session closed → remaining instances are detached
```

**Listing 1.** Conceptual. Unit of work on a `Session`. Identity is session-scoped, not JVM-global.

`StatelessSession` is the other programming model: **no** first-level cache (Hibernate 7 still gives it the rest of the engine, including second-level cache).

## Two cache levels (query results sit in the second)

The **first-level cache** is the persistence context. It is on for every `Session` / `EntityManager`. It is not a product you plug in.

The **second-level cache** is `SessionFactory`-scoped, stores destructured entity/collection state, and is **off** until you set a `RegionFactory` (`hibernate.cache.region.factory_class`). Only types marked `@Cacheable` / `@Cache` go in. Built-in integrations are **JCache** (Ehcache, Caffeine, …) and **Infinispan**. It is unaware of updates done outside Hibernate.

The **query cache** is not a third engine: it stores query result sets in second-level regions (`hibernate.cache.use_query_cache`, default **false**, plus `setCacheable(true)` per query). Cached entity results are ids; if the entity is not in the entity cache, Hibernate still loads it from the database.

> [!warning] A Session is a short-lived identity map, not a shared cache
> The persistence context holds **hard references**; a long-lived `Session` can exhaust memory. It is **never thread-safe**. `StatelessSession` has no first-level cache, so the “one id, one object” guarantee does not apply there.

> [!warning] Second-level and query caches trade consistency for speed
> L2 can undermine ACID reasoning and serve stale data after JDBC or another process writes. Query caching is off by default because most queries do not benefit; caching a query whose entities are not themselves cacheable still hits the database for state.

> [!tip] Interview answer
> Hibernate is a Java ORM and a Jakarta Persistence provider: SessionFactory maps the model and Session is a unit of work with a persistence context. That first-level cache is automatic and guarantees one object per id inside the session; the second-level cache is optional, shared, and provider-backed. Query caching stores result ids in that shared cache and is disabled until you turn it on globally and per query.
