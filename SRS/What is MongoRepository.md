<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS

# What is MongoRepository?

> [!abstract] Short answer
> **`MongoRepository<T, ID>`** is Spring Data MongoDB’s store-specific repository interface. It extends **`ListCrudRepository`**, **`ListPagingAndSortingRepository`**, and **`QueryByExampleExecutor`**, so you get List-returning CRUD, paging/sorting, Query by Example, plus derived/`@Query` finders — backed by a **`mongoTemplate`** bean by default.

## What you get

Declare an interface; Spring generates the implementation when `@EnableMongoRepositories` (or Boot auto-config) is active:

```java
public interface UserRepository extends MongoRepository<User, String> {

  List<User> findByStatusAndAgeGreaterThan(String status, int age);
  Optional<User> findByEmail(String email);
}
```

**Listing 1.** Mongo repository with derived finders; `String` id is the common mapping for MongoDB `_id` (`ObjectId` / `BigInteger` also supported).

Mongo-specific extras on the interface include **`insert` / `insert(Iterable)`** (assumes new documents; docs prefer `save` / `saveAll` for the portable path) and **`findAll(Example)`** variants from Query by Example.

```d2
direction: right
mr: "MongoRepository" {
  style.fill: "#e3f2fd"
}
crud: "ListCrudRepository" {
  style.fill: "#fff3e0"
}
page: "ListPagingAndSortingRepository" {
  style.fill: "#e8f5e9"
}
qbe: "QueryByExampleExecutor" {
  style.fill: "#f3e5f5"
}
tmpl: "MongoTemplate\n(mongoTemplate)" {
  style.fill: "#fce4ec"
}

mr -> crud
mr -> page
mr -> qbe
mr -> tmpl
```

**Fig. 1.** Composition of commons fragments plus wiring to `MongoTemplate`.

## Relation to `MongoTemplate`

Repositories cover most CRUD and named finders. Use **`MongoTemplate`** / **`MongoOperations`** for dynamic `Criteria`, aggregations, and driver callbacks — see [[What is MongoTemplate]] and [[What is the difference between MongoRepository and MongoTemplate]]. Domain types are typically marked **`@Document`**, not JPA `@Entity`.

> [!warning] Id type is not a JPA `Long` by default
> Official docs highlight **`String`**, **`ObjectId`**, and **`BigInteger`** as supported id types for the default mapping. Copying a JPA-style `Long` auto-increment model without thinking about `_id` mapping is a common mistake.

> [!warning] Inheritance wording (Spring Data 3+)
> Older dumps say `MongoRepository` “extends `CrudRepository` and `PagingAndSortingRepository`.” Current API extends the **`List*`** variants (and `QueryByExampleExecutor`). Behavior is the same idea; the exact parent types changed with the commons split.

> [!tip] Interview answer
> `MongoRepository` is the Mongo module’s main repository type: List CRUD, paging/sorting, Query by Example, and method-name or `@Query` finders. Spring implements it on top of `MongoTemplate`. I use it for standard access and drop to the template for dynamic queries and aggregations. Ids are often `String` mapped to `_id`.

See [[What are derived query methods in Spring Data MongoDB]], [[What is MongoTemplate]], and [[What is a CrudRepository]].
