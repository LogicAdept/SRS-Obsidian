<!--
reps: 0
priority: 0
-->
#Problems/Persistence #Java/Persistence/Hibernate/Fetching #SRS

# What is LazyInitializationException?

> [!abstract] Short answer
> **`LazyInitializationException`** is Hibernate’s **unchecked** `HibernateException` for **touching unfetched data outside an open stateful `Session`**. Typical targets: an **uninitialized proxy** (lazy to-one) or **persistent collection** (lazy to-many). Typical Spring case: `@Transactional` ended, then a getter, Jackson, or a view walks **`LAZY`**. It is **not** “any field after close”: already-loaded scalars and **already-initialized** associations remain readable on a detached instance. Fix by **initializing the graph while the session is open** (`JOIN FETCH`, entity graph, `Hibernate.initialize`) or by **not returning a lazy graph** (DTO) — not by mapping everything `EAGER`.

## What must be true for it to throw

Hibernate represents [[What is lazy fetch in JPA or Hibernate|lazy]] to-ones as a **proxy** (`LazyInitializer`). The proxy already stores the **id**; `getIdentifier()` does **not** fetch (unless JPA proxy-compliance is on). **Any other method** calls `initialize()`: load the entity **iff** `getSession()` is an **open** stateful session. Collections follow the same rule: `size()`, iteration, and most getters on an uninitialized `PersistentCollection` load through the session. `Hibernate.isInitialized(...)` is the check; a successful `getId()` is not.

If the session is **null**, **closed**, or **disconnected**, initialization fails. Messages from the initializer include **no session**, **owning session was closed**, and **owning session is disconnected**.

```d2
direction: down
touch: "Getter / size() / Jackson\non uninitialized proxy or collection" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
chk: "LazyInitializer: Session open?" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ok: "SELECT + hydrate" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
lie: "LazyInitializationException" {
  width: 220
  height: 60
  style.fill: "#ffebee"
}

touch -> chk
chk -> ok: yes
chk -> lie: no / closed / disconnected
```

**Fig. 1.** The exception is the failed lazy `SELECT`, not “JPA closed a transaction” by itself.

**Detached ≠ always this exception.** Closing the session **detaches** the instance ([[What is Hibernate entity lifecycle states]]). Fields already in the snapshot stay in memory. Only **still-lazy** navigations need the session.

## What to do (and what not to)

Initialize **while the session is open**. Hibernate’s fetching chapter treats **DTO projection** or **`JOIN FETCH`** as the usual way to get the needed graph in **one** SQL round-trip.

| Approach | What it does |
| --- | --- |
| **DTO / `select new …`** | Constructor expression. The class **need not** be an entity; if it is one, results are **`NEW`**, not managed — **no lazy proxies** on the DTO. |
| **`JOIN FETCH` / Criteria `fetch`** | Load the association **in the same query** (HQL/JPQL `join fetch`, or `Root.fetch`). Not limited to Spring `@Query`. |
| **Entity graph** | JPA fetch/load graph (`@NamedEntityGraph`, or Spring Data `@EntityGraph(attributePaths = …)`). |
| **`@BatchSize(size = n)`** | When a lazy select finally runs, load up to **n** unfetched proxies/collections per `IN` list. Hibernate’s own example uses `size = 100`; **n is not a default**. Still extra SQL. |
| **`Hibernate.initialize` / `PersistenceUnitUtil.load`** | Explicit init **before** close. Collection **wrapper** only — nested lazy fields can still throw later. `Hibernate.unproxy` **throws `LazyInitializationException`** if the proxy is uninitialized and has **no** open session. |

Prefer **`LAZY` mappings** and fetch **in the query**. Global **`EAGER`** (especially on collections) does not remove the design problem: a JPQL query that **omits** an eager association still gets **secondary selects** ([[What is the N plus one problem in Hibernate]]). JPA `LAZY` is a **hint**; the provider may still fetch early — LIE is about **what remained unfetched** when the session died.

```java
Book book = session.find(Book.class, id);
Hibernate.initialize(book.getReviews()); // still inside the Session
session.close();
book.getTitle();                 // OK — already loaded
book.getReviews().size();        // OK — collection initialized
book.getPublisher().getName();   // throws if publisher was still a proxy
```

**Listing 1.** Conceptual: close is safe only for state you already fetched.

```java
List<Order> orders = em.createQuery(
    "select o from Order o left join fetch o.lines where o.customer.id = :cid",
    Order.class)
    .setParameter("cid", customerId)
    .getResultList();
```

**Listing 2.** Conceptual `JOIN FETCH`: `lines` is initialized before the session closes, so later `getLines()` does not throw.

**Open Session / EntityManager in View** is a **documented** way to **avoid** LIE: keep a `Session` / `EntityManager` bound for the **whole HTTP request** so the view or Jackson can still lazy-load **after** the service `@Transactional` method returns ([[What is Open Session In View in Spring]]). Spring Boot **registers `OpenEntityManagerInViewInterceptor` by default** (`spring.jpa.open-in-view=true`). Spring’s `OpenSessionInViewFilter` is the Hibernate-`Session` form. That **hides** missing fetch plans: turn OSIV off and the same getter walk throws. While the context stays open, walking a list of parents plus lazy children is classic **N+1**.

Do **not** “fix” it with **`hibernate.enable_lazy_load_no_trans`**: Hibernate marks it **`@Unsafe`**. It opens a **temporary** persistence context on access, **disabled by default**, and can **break isolation** or **alias** data.

> [!warning] Identifier access does not prove the graph is loaded
> `order.getCustomer().getId()` on an uninitialized **to-one proxy** usually **does not** initialize and **does not** throw. `getCustomer().getName()` (or Jackson reading a non-id property) does — and that is the call that fails after the session is gone. `Hibernate.isInitialized(...)` is the check; a successful `getId()` is not. Returning an entity from a transactional service and walking `LAZY` in a controller is the usual production stack. `initialize(collection)` does **not** initialize each element’s lazy associations. `getClass()` / logging a proxy can **force** a fetch — or throw if the session is already gone. `ENABLE_LAZY_LOAD_NO_TRANS` hides the miss with **another** session and **worse** isolation.

> [!tip] Interview answer
> LazyInitializationException means Hibernate tried to load a lazy proxy or collection after the Session was closed or the instance was detached — in Spring, usually after `@Transactional` ended and OSIV was off. Already-loaded fields are fine; only unfetched associations need the persistence context. I initialize the graph in the transaction with JOIN FETCH, an entity graph, or Hibernate.initialize, or I return a DTO. OSIV stops the exception by keeping the context open for the request; that often just moves the cost into N+1 during JSON rendering. I do not enable lazy load no trans and I do not make every association EAGER to silence it.

See [[What is lazy fetch in JPA or Hibernate]], [[What is Hibernate entity lifecycle states]], [[What is JOIN FETCH and EntityGraph in Spring Data JPA]], [[What is Open Session In View in Spring]], [[What is the N plus one problem in Hibernate]], and [[What is the N plus 1 problem in Spring Data JPA]].
