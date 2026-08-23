<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS

# What is the difference between MongoRepository and MongoTemplate?

> [!abstract] Short answer
> **`MongoRepository`** is the **declarative** Spring Data interface: generated CRUD, paging, derived/`@Query` finders. **`MongoTemplate`** (`MongoOperations`) is the **programmatic** API: `Query`/`Criteria`, updates, aggregations, and driver callbacks. Both use the same mapping layer; repositories are typically backed by a **`mongoTemplate`** bean.

## Choose by shape of the work

| | `MongoRepository` | `MongoTemplate` |
| --- | --- | --- |
| Style | Interface + method names / `@Query` | Imperative calls in code |
| Best for | Stable CRUD and simple filters | Dynamic filters, bulk ops, aggregations |
| Query DSL | Derived names, JSON `@Query` | `Criteria`, `Query`, `Update`, fluent API |
| Setup | `@EnableMongoRepositories` | Inject `MongoOperations` |

```java
// Repository — predictable finder
List<Book> findByAuthor(String author);

// Template — runtime-built filter
mongo.find(
    Query.query(Criteria.where("pages").gt(min).and("genre").is(genre)),
    Book.class);
```

**Listing 1.** Same domain type; repository for fixed shapes, template when predicates are built at runtime (Spring Data MongoDB overview + Template API).

Official guidance: for most tasks use **either** repositories **or** `MongoTemplate` — both leverage mapping. Reach for the template for ad-hoc CRUD, counters, and low-level `MongoDatabase` / `MongoCollection` via `execute` callbacks.

```d2
direction: right
repo: "MongoRepository\nderived / @Query" {
  style.fill: "#e3f2fd"
}
tmpl: "MongoTemplate\nMongoOperations" {
  style.fill: "#e8f5e9"
}
map: "MappingMongoConverter" {
  style.fill: "#fff3e0"
}
db: "MongoDB" {
  style.fill: "#f3e5f5"
}

repo -> tmpl
tmpl -> map -> db
```

**Fig. 1.** Repositories sit on the template stack; both share object–document mapping.

## Mixing is normal

Use repositories for 80% CRUD and inject **`MongoOperations`** (or a custom repository fragment) for aggregations, `$or` / `$elemMatch`, optional-filter search forms, and geo — see [[How do you write custom queries with Query and MongoTemplate]] and [[How do you perform aggregation with Spring Data MongoDB]].

> [!warning] Not an either/or exclusivity rule
> You do not pick one forever. A service can call `BookRepository` and `MongoTemplate` in the same transaction boundary when configured. Duplicating every query as both a method and template code is the waste to avoid.

> [!warning] Repository names hit a ceiling
> Method-name queries and static `@Query` JSON cannot express every MQL shape. Forcing complex logic into a 40-character method name is a smell — move that path to the template or a custom impl.

> [!tip] Interview answer
> `MongoRepository` is the high-level Spring Data interface for CRUD and derived queries; `MongoTemplate` is the lower-level API for Criteria, updates, and aggregations. Repositories usually delegate to a `mongoTemplate` bean. I use both: repositories for simple access, template when the query is dynamic or advanced.

See [[What is MongoRepository]], [[What is MongoTemplate]], and [[How do you build a dynamic Mongo query with Criteria]].
