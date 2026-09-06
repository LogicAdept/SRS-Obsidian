<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Persistence/Hibernate/Session #SRS

# What is Hibernate SessionFactory?

> [!abstract] Short answer
> A **`SessionFactory`** is **one Hibernate instance**: the compiled **runtime metamodel** (entities, associations, table mappings), **configuration**, and **services** (JDBC, cache, statistics). It is **thread-safe**. Typically the process has **one**. You **`openSession()`** (or **`createEntityManager()`**) **per client request**, then **close** that session. A **`Session` is never shared across threads**. Every `SessionFactory` **is** a JPA **`EntityManagerFactory`**; `unwrap(SessionFactory.class)` recovers the Hibernate type when JPA bootstrapped. Simplest native build: **`new Configuration()…buildSessionFactory()`**.

## Factory vs session

The metamodel is **fixed at build**. Later property tweaks on `Configuration` **do not** change an already-built factory. Clients do not see pool internals. Exceptions that look “stateful”: this factory’s **isolated [[What is Hibernate second level cache and its main components|second-level cache]]** (`getCache()`), and **`Statistics`** for its sessions.

| Object | Role |
| --- | --- |
| **`SessionFactory`** | Long-lived, **thread-safe**, one per persistence unit / app. Owns or **uses** the JDBC pool / JTA. |
| **`Session` / `EntityManager`** | Short-lived **persistence context** ([[How does the Hibernate first-level cache work in Spring|L1]]). **Not** thread-safe. New one per request/transaction. |
| **`StatelessSession`** | Also from the factory; **no** persistence context. |

**Obtain a session:** `openSession()` (JDBC connection **lazy** from `ConnectionProvider`) — same idea as `createEntityManager()`. Convenience: **`inTransaction(session -> …)`** / **`fromTransaction`** open, begin, commit/rollback, close. **`inSession`** does **not** start a transaction (no auto-flush unless you flush or begin one). **`getCurrentSession()`** uses **`CurrentSessionContext`** (`hibernate.current_session_context_class`); with JTA and no explicit context, **`JTASessionContext`** scopes to the JTA transaction. **`withOptions()`** customizes one session (tenant, `CacheMode`, interceptor).

**`close()`** destroys the factory: caches, pools. **Close all sessions first** — impact on leftover sessions is **undefined**. No-op if already closed.

```d2
direction: right
cfg: "Configuration / MetadataSources\nbuildSessionFactory()" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
sf: "SessionFactory\nthread-safe metamodel" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
s1: "Session\nrequest A" {
  width: 140
  height: 70
  style.fill: "#e8f5e9"
}
s2: "Session\nrequest B" {
  width: 140
  height: 70
  style.fill: "#e8f5e9"
}

cfg -> sf
sf -> s1
sf -> s2
```

**Fig. 1.** One factory; many short sessions. Do not share a `Session`.

## How you build it

`Configuration` aggregates properties (`hibernate.properties`, system properties, `setProperty`) and mappings (`addAnnotatedClass`, `orm.xml` / deprecated `.hbm.xml`), then **`buildSessionFactory()`**. It delegates to **`StandardServiceRegistryBuilder` → `MetadataSources` / `MetadataBuilder` → `SessionFactoryBuilder`**. Hibernate 7 also documents **`HibernatePersistenceConfiguration`** (JPA `PersistenceConfiguration`). In a container, Persistence XML / Spring Boot still yields this same factory (as EMF).

```java
SessionFactory factory = new Configuration()
    .addAnnotatedClass(Book.class)
    .setProperty(AvailableSettings.DATASOURCE, "java:comp/env/jdbc/test")
    .buildSessionFactory();

factory.inTransaction(session -> session.persist(new Book("…")));
```

**Listing 1.** Conceptual: native bootstrap, then one transactional session per unit of work.

JPA `addNamedQuery` / `addNamedEntityGraph` sit on the factory; they are meant **at create time**, not after sessions are live.

> [!warning] One SessionFactory, never one Session per thread-pool worker
> Building a factory parses the metamodel — **expensive**. Creating one per HTTP request is a classic outage. Sharing **one `Session`** across threads corrupts the persistence context. After any `HibernateException` on a session, **rollback and discard** that session. `close()` on the factory with sessions still open is **indeterminate**. Do not treat L2 or `Statistics` as proof the factory is “mutable” in the mapping sense — the **entity model does not change**.

> [!tip] Interview answer
> SessionFactory is the thread-safe Hibernate instance: compiled mappings plus services, usually one per application, and it is also JPA’s EntityManagerFactory. I open a new Session per request or use inTransaction, and I never share that Session. I build it once with Configuration or the boot API, then close it at shutdown after sessions are gone. getCurrentSession is only for a configured CurrentSessionContext, not a substitute for a singleton Session.

See [[What is Hibernate as an ORM framework]], [[What is the difference between JPA as a specification and Hibernate]], [[How does the Hibernate first-level cache work in Spring]], [[What are Hibernate first and second level cache tiers]], [[What is Hibernate second level cache and its main components]], [[What is Hibernate entity lifecycle states]], and [[What advantages does Hibernate provide over plain JDBC]].
