<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS

# What are derived query methods in Spring Data MongoDB?

> [!abstract] Short answer
> **Derived query methods** on `MongoRepository` use the same Spring Data **method-name grammar** as JPA (`findBy`, `countBy`, `deleteBy`, …). The parser turns property predicates into a **MongoDB query document** (MQL/BSON), not JPQL — for example `findByLastname("al'thor")` → `{"lastname" : "al'thor"}`.

## How the name becomes a query

Spring Data MongoDB parses the method name into constraints joined with `And` / `Or`, mapped to Mongo operators (`$gt`, `$in`, `$near`, …). Nested paths follow domain properties (including embedded types).

```java
public interface BookRepository extends MongoRepository<Book, String> {

  List<Book> findByAuthor(String author);
  List<Book> findByPagesGreaterThan(int pages);
  List<Book> findByTitleAndAuthor(String title, String author);
  Page<Book> findByGenre(String genre, Pageable pageable);
}
```

**Listing 1.** Typical derived finders; `findByPagesGreaterThan` maps to `{"pages" : {"$gt" : pages}}` (Spring Data MongoDB query-methods reference).

`Pageable` / `Sort` on derived methods pass limit, skip, and sort to the query. Reactive repositories return `Flux` / `Mono` with the same naming rules.

```d2
direction: right
name: "findByAgeGreaterThan" {
  style.fill: "#e3f2fd"
}
parse: "Spring Data\nquery parser" {
  style.fill: "#fff3e0"
}
doc: "Mongo query doc\n{ age: { $gt: ? } }" {
  style.fill: "#e8f5e9"
}
run: "MongoDB driver" {
  style.fill: "#f3e5f5"
}

name -> parse -> doc -> run
```

**Fig. 1.** Same naming convention as JPA; execution target is a BSON query document.

## When to step up

Derived names cover most simple CRUD filters. When you need **`$or`**, **`$elemMatch`**, aggregation pipelines, or awkward dynamic predicates, use **`@Query`** with JSON, **`Criteria`** on **`MongoTemplate`**, or a custom fragment — see [[How do you write custom queries with Query and MongoTemplate]] and [[How do you build a dynamic Mongo query with Criteria]].

> [!warning] MQL, not JPQL
> Repository `@Query` on Mongo takes **JSON query documents**. JPQL from the JPA module does not apply here — see [[What are derived query methods in Spring Data JPA]] for the relational side.

> [!warning] Indexes still matter
> Derived queries do not create indexes. Multi-field filters on large collections without supporting indexes become collection scans — a common production pitfall, especially with `$regex` / `Containing` patterns.

> [!tip] Interview answer
> Mongo repositories derive queries from method names the same way JPA repositories do, but the output is a Mongo query document like `{"age":{"$gt":18}}`, not JPQL. Use derived methods for simple filters; switch to `@Query` JSON or `MongoTemplate`/`Criteria` when you need `$or`, aggregations, or runtime-composed predicates.

See [[What are derived query methods in Spring Data JPA]], [[What is the difference between MongoRepository and MongoTemplate]], and [[How do you write custom queries with Query and MongoTemplate]].
