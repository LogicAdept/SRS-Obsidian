<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Annotations #Java/Persistence/Hibernate/Query #SRS

# What are Hibernate named queries?

> [!abstract] Short answer
> A **named query** is a **static** HQL/JPQL or **native SQL** string registered **once** under a **name unique in the persistence unit**, then executed with **`createNamedQuery(name, resultClass)`**. You declare it with JPA **`@NamedQuery` / `@NamedNativeQuery`** (entity or mapped superclass) or Hibernate’s **typesafe** `org.hibernate.annotations.NamedQuery` / `NamedNativeQuery` (type or **package**). The session looks the query up by name — it does **not** parse a new string each call. `Session.getNamedQuery` is **deprecated**; use the typed `createNamedQuery`. Missing names throw **`UnknownNamedQueryException`** / **`IllegalArgumentException`**.

## What “named” means

Jakarta Persistence: **`@NamedQuery`** declares a JPQL string; **names are scoped to the persistence unit**; run it with **`EntityManager.createNamedQuery(String, Class)`**. Hibernate’s `QueryProducer` adds that the named query may be **HQL or native SQL**. Hibernate’s own `@NamedQuery` is the same idea in **HQL/JPQL**, with members instead of stringly-typed **`QueryHint`s**.

The annotation lives on a class, but the **name is global** to the unit — not “private to that entity.” Hibernate: the name **must be unique**. JPA **`EntityManagerFactory.addNamedQuery`**: a later definition **replaces** an earlier one of the same name (metadata or programmatic).

```d2
direction: right
ann: "@NamedQuery / @NamedNativeQuery\n(or addNamedQuery)" {
  width: 260
  height: 110
  style.fill: "#e3f2fd"
}
sf: "SessionFactory / EMF\nname → parsed query" {
  width: 240
  height: 110
  style.fill: "#fff3e0"
}
run: "createNamedQuery(name, Class)\nsetParameter → getResultList" {
  width: 260
  height: 110
  style.fill: "#e8f5e9"
}

ann -> sf -> run
```

**Fig. 1.** Define once on the mapping (or factory); execute by name on a session.

```java
@Entity
@NamedQuery(
    name = "Customer.byName",
    query = "SELECT c FROM Customer c WHERE c.name LIKE :custName")
class Customer { /* ... */ }

List<Customer> found = em.createNamedQuery("Customer.byName", Customer.class)
    .setParameter("custName", "Smith%")
    .getResultList();
```

**Listing 1.** Conceptual JPA named JPQL query: unique name, bind parameters at runtime.

## HQL/JPQL vs native SQL

| Kind | Annotation | Query text | Result mapping |
| --- | --- | --- | --- |
| Object query | `@NamedQuery` (JPA or `org.hibernate.annotations`) | JPQL / HQL | Entity or `resultClass`; typed `createNamedQuery` |
| Native SQL | `@NamedNativeQuery` | SQL dialect of the DB | **`resultClass`** **or** **`@SqlResultSetMapping`** (Hibernate: do **not** set both) |

Native named queries are called **the same way** as named HQL (`createNamedQuery`). Hibernate extra on native: **`querySpaces`** (tables the SQL touches) so flush can decide whether to synchronize the persistence context first. JPA native mapping can also use `entities` / `classes` / `columns` **instead of** a named `resultSetMapping` (Jakarta Persistence 3.2).

Hibernate **`createNamedMutationQuery(name)`** is for a named **insert/update/delete** (HQL or native). Passing a **select** there throws **`IllegalMutationQueryException`**; the reverse on a selection API throws **`IllegalSelectQueryException`**.

Hibernate `@NamedQuery` extras (defaults): **`cacheable = false`**, optional **`cacheRegion`**, **`timeout`**, **`fetchSize`**, **`readOnly`**, **`flush`**. Query-cache eligibility on the annotation is **not** enough by itself: the factory still needs **`hibernate.cache.use_query_cache`**.

```java
@NamedNativeQuery(
    name = "find_person_name",
    query = "SELECT name FROM person",
    resultClass = String.class)
// session.createNamedQuery("find_person_name", String.class).getResultList();
```

**Listing 2.** Conceptual named native query; same lookup API as named HQL.

Runtime registration: **`SessionFactory.addNamedQuery` / `EntityManagerFactory.addNamedQuery`**. Config on that `Query` (hints, max results, lock, result mapping) is **kept**; **parameter bindings are not**. Overrides at execution do **not** change the stored definition.

> [!warning] The name is persistence-unit global, and `getNamedQuery` is the old API
> Two entities both declaring `@NamedQuery(name = "findAll", …)` collide in one unit. Prefix with the entity (`Customer.findAll`). `Session.getNamedQuery(name)` still appears in older Hibernate examples; current `QueryProducer` marks it **deprecated** in favor of **`createNamedQuery(name, Class)`**. JPA’s typed `createNamedQuery(name, Class)` is specified for **JPQL** named queries (single select item assignable to `resultClass`); untyped `createNamedQuery(name)` covers **JPQL or native SQL**. Unknown name: Hibernate **`UnknownNamedQueryException`**, JPA **`IllegalArgumentException`**.

> [!tip] Interview answer
> Named queries are static HQL/JPQL or native SQL registered under a unique persistence-unit name, usually with @NamedQuery or @NamedNativeQuery. I run them with createNamedQuery, bind parameters, and get results — Hibernate does not re-parse a query string at each call site. Native named queries need resultClass or a SqlResultSetMapping. I treat names as global, I do not rely on the deprecated getNamedQuery, and I remember query-cache flags on the annotation still require the second-level query cache to be enabled.

See [[What is Hibernate Query Language HQL]], [[What kinds of queries can Hibernate run]], [[What is the difference between JPQL and Hibernate HQL]], and [[What advantages does Hibernate provide over plain JDBC]].
