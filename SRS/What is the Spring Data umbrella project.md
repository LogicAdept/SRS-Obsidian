<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What is the Spring Data umbrella project?

> [!abstract] Short answer
> **Spring Data** is an **umbrella** of Spring projects that apply a **shared repository / mapping programming model** across many stores. **Spring Data Commons** holds the store-agnostic core; sibling modules (**JPA**, **MongoDB**, **Redis**, **JDBC/R2DBC**, **Cassandra**, **Elasticsearch**, **REST**, …) implement that model for each technology.

## Umbrella, not one JAR

“Spring Data” is not a single persistence engine. It is a family:

- **Commons** — `Repository`, CRUD/paging fragments, query derivation rules, `Page`/`Sort`, shared extensions
- **Store modules** — wire those abstractions to a concrete database or API
- **Cross-cutting modules** — e.g. **Spring Data REST** exposing repositories over HTTP

You depend on the module(s) you need (`spring-boot-starter-data-jpa`, `…-data-mongodb`, `…-data-redis`, …). Boot auto-configures the matching stack.

```d2
direction: down
umbrella: "Spring Data (umbrella)" {
  style.fill: "#e3f2fd"
}
commons: "Commons\nshared repositories" {
  style.fill: "#fff3e0"
}
stores: "JPA · MongoDB · Redis\nJDBC/R2DBC · Cassandra · …" {
  style.fill: "#e8f5e9"
}
rest: "Spring Data REST\n(optional)" {
  style.fill: "#f3e5f5"
}

umbrella -> commons
umbrella -> stores
umbrella -> rest
commons -> stores
```

**Fig. 1.** One brand, many modules: Commons shared model plus store-specific implementations.

## What you get in practice

Declare a typed repository interface; the store module generates an implementation. Method naming and paging feel familiar when you move between JPA and MongoDB, while mapping annotations and low-level templates stay store-specific (`@Entity` / `EntityManager` vs `@Document` / `MongoTemplate`).

```java
// Relational
public interface UserRepository extends JpaRepository<User, Long> { }

// Document
public interface ProductRepository extends MongoRepository<Product, String> { }
```

**Listing 1.** Same repository idea; different modules and domain markers (conceptual).

> [!warning] Modules are not interchangeable
> Sharing the repository *shape* does not make Mongo a drop-in for JPA. Transactions, schemas, and query languages still follow the store. Pick the module that matches the database you actually run.

> [!tip] Interview answer
> Spring Data is an umbrella: Commons defines the shared repository model, and modules like JPA, MongoDB, and Redis implement it for each store. I add the starter for the technology I use; I do not expect one Spring Data JAR to talk to every database by itself.

See [[What is Spring Data Commons]], [[What are Spring Data Repository interfaces]], [[Why do you need Spring Data]], and [[What is Spring Data JPA]].
