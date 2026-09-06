<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #Persistence/ORM #SRS

# What is Hibernate as an ORM framework?

> [!abstract] Short answer
> **Hibernate ORM** is an **Object/Relational Mapping** engine for **Java (and other JVM languages)**. ORM maps an **object domain model** to a **relational schema** (classes ↔ tables, Java types ↔ SQL types) and back. The application talks to a **`Session` / `EntityManager`**; Hibernate generates JDBC SQL, hydrates **entities**, and keeps a **persistence context**. A **`SessionFactory`** (also a JPA **`EntityManagerFactory`**) is one Hibernate **instance**: the compiled metamodel plus services. Hibernate is a **Jakarta Persistence provider**, not a replacement for SQL or JDBC.

## The mismatch it sits in

Working with objects and tables together is expensive because the representations **do not match**. Hibernate’s preface calls that the **paradigm mismatch**. Hibernate **sits between** the Java data-access layer and the RDBMS: you **load, store, and query domain objects**; it talks **JDBC** underneath (`Session` **wraps** a `java.sql.Connection`).

It also supplies **query languages** (HQL/JPQL, Criteria, native SQL). The stated design goal is to drop **hand-crafted ResultSet mapping** for **common** persistence work — **not** to hide SQL. Native queries and `Session.doWork` stay first-class. It is **most useful** with an **object model in the middle tier**; a design that is **only stored procedures** in the database is a documented poor fit.

```d2
direction: right
app: "Java domain model\n@Entity / Session API" {
  width: 220
  height: 110
  style.fill: "#e3f2fd"
}
orm: "Hibernate\nmappings, Session, SQL" {
  width: 240
  height: 110
  style.fill: "#fff3e0"
}
jdbc: "JDBC Connection" {
  width: 180
  height: 90
  style.fill: "#e8f5e9"
}
db: "RDBMS" {
  width: 140
  height: 80
  style.fill: "#f3e5f5"
}

app -> orm -> jdbc -> db
```

**Fig. 1.** Hibernate is the ORM layer: object graph in, JDBC SQL out.

## Runtime shape

| Piece | Role |
| --- | --- |
| **`SessionFactory`** | Thread-safe, **immutable metamodel** (entities, associations, table mappings) + services. Typically **one per database**. Factory for sessions. **Is** a JPA `EntityManagerFactory` (`unwrap` if you started from JPA). Optional **second-level cache**. |
| **`Session`** | Short-lived **unit of work**, **not** shared across threads. Persistence context (L1): identity, dirty checking, lazy proxies. Factory for `Transaction`. |
| **Mappings** | Annotations (`@Entity`, associations) or XML: how types persist. |

`persist` makes Hibernate responsible for **`INSERT`**. An HQL `from Event` makes it **generate `SELECT`** and **instantiate/populate** `Event` objects from the result set.

```java
sessionFactory.inTransaction(session -> {
  session.persist(new Event("kickoff", now()));
  List<Event> all = session.createSelectionQuery("from Event", Event.class)
      .getResultList();
});
```

**Listing 1.** Conceptual: the application manipulates entities; Hibernate emits JDBC and rebuilds objects.

Every `Session` is a JPA `EntityManager`. You can stay on standard JPA types or call Hibernate APIs (`Session`, HQL extensions, `@org.hibernate.annotations…`).

> [!warning] ORM is not “I never look at SQL”
> Hibernate still runs **your** JDBC bill: fetch plans, N+1, isolation, and dialects are database problems. A `Session` **must not** be shared between threads; leaking one across requests pins the **whole persistence context** in memory. `SessionFactory` is the long-lived object — create it **once**, close sessions **per request**.

> [!tip] Interview answer
> Hibernate is an ORM: it maps Java entities to tables and talks JDBC so I persist and query objects instead of walking ResultSets by hand. SessionFactory is the compiled mapping, one per app; Session is the unit of work and first-level cache. It implements Jakarta Persistence, but it does not replace SQL — I still read the statements it generates and drop to native SQL when I need to.

See [[What advantages does Hibernate provide over plain JDBC]], [[What is Hibernate SessionFactory]], [[What is the difference between JPA as a specification and Hibernate]], and [[What association types exist in Hibernate]].
