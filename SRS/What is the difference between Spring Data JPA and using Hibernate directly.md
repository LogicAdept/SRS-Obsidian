<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Persistence/JPA #Java/Persistence/Hibernate #SRS

# What is the difference between Spring Data JPA and using Hibernate directly?

> [!abstract] Short answer
> **Spring Data JPA** is a **repository abstraction on top of JPA** (`EntityManager`). **Hibernate** is typically the **JPA provider** (or a native `Session` API) underneath. Spring Data does not replace Hibernate — in Boot it usually **uses** Hibernate through JPA; “Hibernate directly” means you call **`Session` / `EntityManager`** yourself instead of generated repositories.

## Layers

| Layer | What it is |
| --- | --- |
| Spring Data JPA | Interfaces (`JpaRepository`), derived/`@Query` methods, generated proxies (`SimpleJpaRepository`) |
| JPA | Standard API: `EntityManager`, `@Entity`, JPQL |
| Hibernate | Common JPA implementation; also offers native `Session` / Hibernate APIs |

`SimpleJpaRepository` Javadoc: a richer interface than a plain `EntityManager`, implemented **using** that `EntityManager`. So repository `save` / finders still end in JPA (and thus usually Hibernate) calls.

```d2
direction: down
sd: "Spring Data JPA\nJpaRepository proxy" {
  style.fill: "#e3f2fd"
}
jpa: "JPA EntityManager" {
  style.fill: "#fff3e0"
}
hib: "Hibernate\n(provider / Session)" {
  style.fill: "#e8f5e9"
}
db: "Database" {
  style.fill: "#f3e5f5"
}

sd -> jpa -> hib -> db
```

**Fig. 1.** Typical Boot stack: Spring Data → JPA → Hibernate → DB. Skipping Spring Data means talking to JPA/Hibernate yourself.

## Programming model difference

**With Spring Data JPA** you declare:

```java
public interface BookRepository extends JpaRepository<Book, Long> {
  List<Book> findByTitleContaining(String fragment);
}
```

**Listing 1.** No hand-written DAO; Spring Data generates the implementation that uses `EntityManager`.

**Using Hibernate (or JPA) directly** you inject `EntityManager` or `Session` and write persist/query code (JPQL/HQL/Criteria) yourself — more control, more boilerplate. Spring Framework’s ORM support wires factories and transactions either way; Spring Data is the optional repository layer on top.

You can combine them: keep repositories for CRUD/finders and drop to `EntityManager` in a **custom repository fragment** when Criteria or multi-step persistence logic needs the full API.

> [!warning] Not “Spring Data vs Hibernate as two ORMs”
> Choosing Spring Data JPA almost always still means Hibernate (or another provider) runs under JPA. The real choice is **repository abstraction vs hand-written persistence code**, not throwing Hibernate away.

> [!tip] Interview answer
> Spring Data JPA is repositories and query derivation over `EntityManager`. Hibernate is the usual engine behind that EntityManager. Direct Hibernate/JPA means I write Session or EntityManager calls myself; Spring Data generates the common CRUD and finder glue on top of the same stack.

See [[What is Spring Data JPA]], [[What are the pros and cons of EntityManager versus Spring Data JPA repositories]], and [[What technologies does Spring Data build upon]].
