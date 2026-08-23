<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS

# What is MongoTemplate?

> [!abstract] Short answer
> **`MongoTemplate`** is the central Spring Data MongoDB helper for CRUD, queries, updates, and aggregations. It implements **`MongoOperations`**, maps domain objects to BSON documents, and exposes fluent **`Query`** / **`Criteria`** / **`Update`** APIs — the lower-level counterpart to `MongoRepository`.

## Role and API shape

Once configured, the template is **thread-safe** and reusable. Method names mirror the MongoDB driver `Collection` API (`find`, `findOne`, `insert`, `save`, `remove`, `update` / `updateMulti`, `findAndModify`, …), but you pass **domain types** instead of raw `Document` when mapping is available.

```java
@Autowired
MongoOperations mongo; // prefer the interface over the concrete class

List<Book> books = mongo.find(
    Query.query(Criteria.where("pages").gt(300)),
    Book.class);

mongo.save(new Book("Dune", 412));
```

**Listing 1.** Inject `MongoOperations` and run a criteria query (Spring Data MongoDB Template API).

A fluent style is also available: `mongo.query(Book.class).matching(…).all()`. `execute` callbacks expose `MongoCollection` / `MongoDatabase` when you need driver-level control. Driver exceptions are translated into Spring’s **`DataAccessException`** hierarchy.

```d2
direction: right
repo: "MongoRepository\nderived / @Query" {
  style.fill: "#e3f2fd"
}
tmpl: "MongoTemplate\nMongoOperations" {
  style.fill: "#e8f5e9"
}
conv: "MongoConverter\nPOJO ↔ Document" {
  style.fill: "#fff3e0"
}
db: "MongoDB" {
  style.fill: "#f3e5f5"
}

repo -> tmpl
tmpl -> conv -> db
```

**Fig. 1.** Repositories typically delegate to a `mongoTemplate` bean; the template owns mapping and ad-hoc operations.

## When to use it vs repositories

Prefer **`MongoRepository`** for simple CRUD and derived/`@Query` finders. Reach for **`MongoTemplate`** for dynamic `Criteria`, bulk updates, aggregations, geo queries, and anything awkward as a method name — see [[How do you write custom queries with Query and MongoTemplate]] and [[What is the difference between MongoRepository and MongoTemplate]].

> [!warning] Inject `MongoOperations`, not only the class
> Official docs prefer referencing the template through **`MongoOperations`**. That keeps code against the contract and matches how Spring wires repository support (default bean name **`mongoTemplate`**).

> [!warning] Not a drop-in for JPA `EntityManager` semantics
> There is no JPA-style persistence context with automatic dirty checking. You explicitly `save` / `update` / `remove`. Multi-document transactions need **`MongoTransactionManager`** — see [[How do you use multi-document transactions in Spring Data MongoDB]].

> [!tip] Interview answer
> `MongoTemplate` is Spring Data MongoDB’s central API: CRUD and queries with POJO mapping, implementing `MongoOperations`. Repositories cover common finders; I use the template for Criteria-based dynamic queries, updates, and aggregations. Prefer injecting `MongoOperations`, and remember it is thread-safe once configured.

See [[What is the difference between MongoRepository and MongoTemplate]], [[How do you build a dynamic Mongo query with Criteria]], and [[How does Spring Data MongoDB differ from Spring Data JPA]].
