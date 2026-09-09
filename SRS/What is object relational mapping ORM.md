<!--
reps: 0
priority: 0
-->
#Java/Persistence #SRS

# What is object relational mapping ORM

> [!abstract] Short answer
> **Object-relational mapping is the technique of mapping classes to tables, fields to columns, and object references to foreign keys, so application code works with objects while the database keeps storing rows.** In Java the standard for it is Jakarta Persistence (JPA): a specification of annotations, the entity model, and an `EntityManager` API, implemented by tools like Hibernate and EclipseLink.

## The mapping problem it solves

A relational database has tables; Java has graphs of objects with references, inheritance, and collections. Writing SQL and row-mapping code by hand for every entity is repetitive and error-prone. An ORM framework maps the two worlds declaratively — entities describe the mapping, the framework generates the SQL, tracks changes, and manages the identity of loaded objects.

```d2
direction: right
obj: "Java objects\nAuthor(1..*) Book" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
orm: "ORM layer\nentities + EntityManager\nunit of work" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
sql: "SQL over JDBC\nINSERT / SELECT / UPDATE" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
db: "Relational DB\nauthors / books tables" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
obj <-> orm <-> sql <-> db
```

**Fig. 1.** The ORM sits between the object model and JDBC: entities on one side, generated SQL on the other — everything still crosses a JDBC driver underneath.

The standard pieces (Jakarta Persistence 3.1 is the current EE 10 release): `@Entity` marks mapped classes; `@Id` designates identity; `@OneToMany`/`@ManyToOne` map relationships; `EntityManager` persists, finds, and flushes; JPQL queries entities instead of tables; and `GenerationType.UUID` joined the standard identity strategies in 3.1. What the framework adds beyond mapping: dirty checking (changed entities flush as UPDATEs), a first-level cache per persistence context, lazy loading through proxies, and transactional write-behind.

```java
@Entity
class Book {
    @Id @GeneratedValue
    Long id;
    String title;

    @ManyToOne(fetch = FetchType.LAZY)
    Author author;
}

Book b = em.find(Book.class, 11L);      // SELECT ... FROM book WHERE id = ?
b.setTitle("Effective Java, 3rd ed.");  // detected as dirty -> UPDATE at flush
```

**Listing 1.** Conceptual JPA shape: annotated entity, `find` by primary key, and a plain setter that the framework turns into an UPDATE at commit time.

> [!warning] The object-relational impedance mismatch does not disappear — ORM just manages it
> Three truths interviewers probe. First, lazy loading leaks into correctness: accessing an unloaded association outside an open persistence context throws `LazyInitializationException`, and carelessly eager mappings load half the database. Second, generated SQL is a black box unless you look — the classic N+1 explosion of one query per relationship row comes from natural-looking object navigation ([[When does the N plus 1 query problem occur and how do you fix it]]). Third, identity vs equality: JPA guarantees one instance per row *inside* a persistence context; comparing detached entities still needs `equals`/`hashCode` discipline. ORM is not "no SQL": reports, bulk updates, and vendor features still want real SQL (JPQL native queries). The alternative stack — mapping SQL explicitly with tools like jOOQ/MyBatis — trades this automation for direct query control; see [[Which ways can Java applications talk to a database]] and [[Which Java ORM frameworks do you know]].

> [!tip] Interview answer
> **ORM maps classes to tables and object references to foreign keys so code works with objects while SQL is generated for you. In Java, JPA — Jakarta Persistence — is the spec: entities, annotations, EntityManager, JPQL; Hibernate and EclipseLink implement it, Spring Data JPA wraps it with repositories. The trade-offs: lazy loading, N+1 queries and dirty tracking need real understanding — the mapping problem is managed, not eliminated.**

