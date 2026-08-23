<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# Why do you need Spring Data?

> [!abstract] Short answer
> **Hand-written data-access layers repeat the same CRUD and query glue** (`EntityManager`, JDBC templates, store-specific APIs) for every entity, while **applications now use many persistence technologies** (relational, document, key-value, search). **Spring Data** provides a **shared repository model** and **generates implementations** from interfaces — cutting boilerplate without pretending every store is identical.

## The problem: boilerplate and store sprawl

Before Spring Data, a typical JPA service layer duplicated **`findById` / `save` / `delete`** wrappers around **`EntityManager`** (or **`JdbcTemplate`** SQL) per aggregate. That code is tedious, easy to get subtly wrong, and unrelated to business rules.

At the same time, production systems rarely stop at one database: relational OLTP, Redis caches, MongoDB documents, Elasticsearch indexes, and others each ship their own client APIs. Re-implementing the same repository-shaped access pattern for every store wastes effort.

Spring Data Commons states the repository abstraction goal explicitly: **significantly reduce the amount of boilerplate code required to implement data access layers for various persistence stores**.

```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByLastName(String lastName);
}
// Spring Data generates the implementation at runtime — no manual EntityManager glue
```

**Listing 1.** Declare the interface; CRUD + query derivation replace repetitive persistence code.

## What Spring Data adds

| Layer | Role |
|---|---|
| **Spring Data Commons** | Core **`Repository`**, **`CrudRepository`**, query derivation, paging/sorting model |
| **Store modules** | **JPA**, **MongoDB**, **Redis**, **JDBC**, **Elasticsearch**, … — each maps the shared API to that technology |
| **Generated implementations** | e.g. **`SimpleJpaRepository`** for JPA — wired from your interface definition |

You program to **interfaces**, not to a single universal driver. **`JpaRepository`** extends the commons model with JPA-specific behavior; Mongo or Redis modules keep their store traits (annotations like **`@Entity`** vs **`@Document`**, reactive variants, etc.).

```d2
direction: right
app: "Service layer" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
repo: "YourRepository\n(interface)" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
gen: "Generated impl\n(SimpleJpaRepository, …)" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
store: "JPA / Mongo / Redis / …" {
  width: 180
  height: 50
  style.fill: "#fce4ec"
}

app -> repo -> gen -> store
```

**Fig. 1.** Commons defines the programming model; each module binds it to a persistence technology.

## What Spring Data does not replace

The **abstraction is shared**; **each module still reflects its store** (transactions, query language, indexing, consistency). Spring Data is **not** a ORM — **Spring Data JPA** sits **on top of JPA/Hibernate**, it does not replace them.

When **query derivation** and **`@Query`** are insufficient, you still write **custom repository fragments**, **`EntityManager`** access, or native SQL — Spring Data removes repetitive CRUD, not every data-access decision. See [[What is Spring Data Commons]] and [[What is Spring Data JPA]].

> [!warning] Not a silver bullet for complex domains
> Derived query method names explode for deep filters; multi-store apps must **scope modules correctly** (`@EnableJpaRepositories` vs `@EnableMongoRepositories`). Spring Data **reduces glue**, it does not eliminate the need to understand your database. Compare [[What are the pros and cons of EntityManager versus Spring Data JPA repositories]] when choosing raw JPA vs repositories.

> [!tip] Interview answer
> Spring Data exists to cut repetitive data-access boilerplate and give one repository-shaped programming model across many stores. You declare interfaces; Spring generates CRUD and derived queries. Commons is shared; JPA/Mongo/Redis modules add store-specific behavior. You still write custom code when derivation and @Query are not enough.
