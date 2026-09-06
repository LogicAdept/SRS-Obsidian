<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Persistence/Hibernate #SRS

# What is the difference between JPA as a specification and Hibernate?

> [!abstract] Short answer
> **JPA** (Jakarta Persistence) is the **specification**: interfaces and mapping annotations (`EntityManager`, `EntityManagerFactory`, `@Entity`, JPQL). It is **not** a runnable ORM. **Hibernate ORM** is a **library** that **implements** that spec and also exposes a **native** API (`Session` extends `EntityManager`, `SessionFactory` extends `EntityManagerFactory`) plus extra mapping annotations. You compile against JPA types; Hibernate (or another **persistence provider**) is the engine on the classpath. What each is: [[What is the Java Persistence API JPA]], [[How would you explain Hibernate]].

## Spec versus one complete implementation

Jakarta Persistence 3.2 defines a standard object/relational mapping API for Java SE and Jakarta EE. The spec JAR has types. It does not flush SQL, manage a first-level cache, or talk to JDBC. A **persistence provider** implements the contract. Hibernate was the inspiration behind that API and includes a complete implementation of the current revision (package `jakarta.persistence` since Persistence 3.0). Other providers compete on the same JPA types.

Since Hibernate **5.2**, the native API **extends** JPA rather than wrapping it: every `SessionFactory` **is** an `EntityManagerFactory`. You can still `unwrap(Session.class)` / `unwrap(SessionFactory.class)` to drop down. Hibernate Javadoc: JPA mapping annotations are the foundation for Hibernate **and other JPA implementations**; `org.hibernate.annotations` extend that foundation and work with **either** API.

```d2
direction: down
jpa: "Jakarta Persistence spec\nEntityManager, @Entity, JPQL" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
hib: "Hibernate ORM\nSession extends EntityManager\nSessionFactory extends EMF" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
other: "other JPA providers" {
  width: 240
  height: 45
}
jpa -> hib
jpa -> other
```

**Fig. 1.** JPA is the contract. Hibernate implements it and adds a native superset. Other providers implement the same contract, not `Session`.

Hibernate’s own guide: write `Session` / `SessionFactory`, **or** stay on `EntityManager` / `EntityManagerFactory` wherever reasonable and fall back to native APIs only where needed. Using **only** JPA types is possible in principle; you then miss native `StatelessSession`, HQL extras, and Hibernate-only annotations.

Bootstrapping as a JPA provider uses `Persistence.createEntityManagerFactory`. You still need a provider class (Hibernate’s `persistence.xml` `provider`, or a container that injects the factory). Switching the provider only works if mappings, queries, and properties stayed inside portable JPA.

```java
EntityManagerFactory emf = Persistence.createEntityManagerFactory("pu");
EntityManager em = emf.createEntityManager();
em.find(Book.class, 1L); // portable JPA

Session session = em.unwrap(Session.class); // Hibernate engine — not in the spec
```

**Listing 1.** Conceptual. Same persistence unit. `unwrap` is the documented drop-down — and the point where you leave portability.

These bind you to Hibernate (or to one dialect): `Session` / `StatelessSession`, `org.hibernate.annotations.*`, vendor query hints, Hibernate XML mapping DTD, `unwrap`, and SQL/HQL that only one provider accepts. JPA-standard `orm.xml` plus `jakarta.persistence` annotations is the portable mapping core.

> [!warning] Session is not a second, unrelated API
> `Session` **is** an `EntityManager`. Adding `jakarta.persistence` to the classpath does not give you two persistence stacks. “We use JPA and Hibernate” usually means “we use Hibernate through JPA types.” Calling Hibernate-only methods on that subtype is what is non-portable.

> [!warning] Duplicate names are not the spec
> Hibernate-native types often shadow JPA names (`org.hibernate.annotations.CascadeType` vs `jakarta.persistence.CascadeType`, two `Query` types, two cache APIs). They may be used with `EntityManager`. They still are not in the spec. A provider swap will not honor them.

> [!tip] Interview answer
> JPA is the Jakarta Persistence specification: a standard API, not a product you run. Hibernate is a library that implements that specification and adds Session, SessionFactory, and extra annotations. Session extends EntityManager, so Hibernate-native is a superset, not a rival product. You cannot swap “JPA” for Hibernate; you can switch providers only if you stayed on portable JPA types, mappings, and properties.
