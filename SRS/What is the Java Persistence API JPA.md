<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS

# What is the Java Persistence API JPA?

> [!abstract] Short answer
> **JPA** is the **Java Persistence API**, now **Jakarta Persistence**: the **standard** for mapping Java domain objects to a relational database and managing their lifecycle. You write **entities** and mapping metadata; a **persistence provider** (Hibernate, EclipseLink, …) implements `EntityManager` / `EntityManagerFactory`. The spec is the contract; it is **not** a runnable ORM. Spec vs product: [[What is the difference between JPA as a specification and Hibernate]], [[How would you explain Hibernate]].

## Spec, provider, persistence context

Jakarta Persistence 3.2 (Jakarta EE 11) is that API on Jakarta EE and Java SE. **Java Persistence API** is the historical JCP name (`javax.persistence`). Persistence **3.0** moved the project to Eclipse and renamed the package to **`jakarta.persistence`**. Mix the two packages and bootstrap fails.

A **persistence unit** (`persistence.xml` or `PersistenceConfiguration`) compiles into an `EntityManagerFactory`. An `EntityManager` is the API over a **persistence context**: at most one managed instance per entity type + primary key. You `persist`, `find`, `merge`, `remove`, and query (JPQL, Criteria, native SQL). Container-managed managers are injected with `@PersistenceContext`; application-managed ones come from the factory. The API JAR has **interfaces** — without a provider there is no SQL and no working factory.

An **entity** is a lightweight persistent domain object: `@Entity`, non-`final` top-level or static nested class, public or protected no-arg constructor, no `final` persistent members. Enums, records, and interfaces cannot be entities. Every entity needs `@Id` or `@EmbeddedId`: [[What is the JPA Id annotation]]. Abstract entities are legal: [[Can a JPA entity class be abstract]]. Associations use relationship annotations and optional `cascade`: [[How would you explain CascadeType.ALL]].

```d2
direction: down
app: "application" {
  width: 150
  height: 40
}
em: "EntityManager\npersistence context" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
prov: "persistence provider\n(Hibernate, …)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
db: "relational database" {
  width: 180
  height: 40
}
app -> em
em -> prov
prov -> db
```

**Fig. 1.** You program to `EntityManager`. The provider talks JDBC/SQL. Switching providers is portable only if you stay on the spec.

```java
@Entity
public class Book {
    @Id
    private Long id;

    private String title;

    @Version
    private int revision;

    protected Book() {}
}
```

**Listing 1.** Portable entity: identity, basic state, optional `@Version` for optimistic locking. The provider, not application code, updates `revision` after the instance is persistent.

## Optimistic locking is a JPA feature, not “Hibernate magic”

If the entity has a version, the provider **must** verify it when writing: read version with the row, compare at flush or commit (or on `merge` of a detached instance). If the database revision changed, it throws `OptimisticLockException` and **marks the transaction for rollback**. Portable version types are `int` / `Integer`, `short` / `Short`, `long` / `Long`, or `LocalDateTime` / `Instant` / `java.sql.Timestamp`. At most one version, on the hierarchy root or a mapped superclass. The application must not assign the version after persist.

Without `@Version`, automatic optimistic locking is **not** portable. Providers may offer extra schemes; those are not the spec.

> [!warning] The API JAR is not an ORM
> Adding `jakarta.persistence-api` gives you interfaces. “We use JPA” almost always means a provider through JPA types. Hibernate *implements* JPA and adds native `Session` APIs. Mapping annotations that are not in `jakarta.persistence` are not JPA.

> [!warning] A version check can fail late
> `OptimisticLockException` may be thrown on an API call, on **flush**, or at **commit**. Catching it without rolling back is wrong: the spec requires the current transaction to be marked rollback-only. Do not bump `@Version` yourself.

> [!tip] Interview answer
> JPA, the Java Persistence API, is the standard for mapping Java objects to relational tables and managing their lifecycle. Today that spec is Jakarta Persistence in the jakarta.persistence package. EntityManager is the API; Hibernate or another provider implements it. JPA is not a second product next to Hibernate, and the persistence-api JAR does not run SQL by itself.
