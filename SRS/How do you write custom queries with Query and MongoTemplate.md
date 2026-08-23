<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Annotations #SRS

# How do you write custom queries with Query and MongoTemplate?

> [!abstract] Short answer
> Use **`@Query`** on a `MongoRepository` method with a **MongoDB JSON (MQL)** string and `?0`/`?1` placeholders when the query shape is fixed. Use **`MongoTemplate`** with **`Query`** + **`Criteria`** (or `BasicQuery`) when you need dynamic filters, updates, or other template operations that repositories do not express cleanly.

## Repository `@Query` (fixed MQL)

`org.springframework.data.mongodb.repository.Query` replaces derived method-name queries with an explicit JSON query document. Placeholders bind method arguments; optional `fields` projects returned properties.

```java
public interface UserRepository extends MongoRepository<User, String> {

  @Query("{ 'status': ?0, 'age': { $gte: ?1 } }")
  List<User> findByStatusAndAgeAtLeast(String status, int age);

  @Query(value = "{ 'firstname': ?0 }", fields = "{ 'firstname': 1, 'lastname': 1 }")
  List<User> findProjectedByFirstname(String firstname);
}
```

**Listing 1.** JSON-based repository queries (Spring Data MongoDB reference: JSON-based Query Methods).

This is **not** JPQL. SpEL (`?#{…}`) is also supported for conditional fragments when binding alone is not enough.

## `MongoTemplate` + `Query` / `Criteria` (dynamic)

`MongoTemplate` (`MongoOperations`) runs ad-hoc finds with a fluent `Criteria` API that mirrors Mongo operators (`is`, `gte`, `lt`, …). Wrap criteria in `Query` and call `find` / `findOne` / `count`.

```java
import static org.springframework.data.mongodb.core.query.Criteria.where;
import static org.springframework.data.mongodb.core.query.Query.query;

List<User> users = mongoTemplate.find(
    query(where("status").is("active").and("age").gte(18)),
    User.class);
```

**Listing 2.** Template query with `Criteria` / `Query` (Spring Data MongoDB: Querying Documents).

For optional runtime filters, build `Criteria` pieces only when present and AND them — see [[How do you build a dynamic Mongo query with Criteria]]. `BasicQuery` accepts a plain JSON string when you already have MQL text. The same template API covers updates (`updateFirst` / `updateMulti`) and aggregations beyond simple finds.

```d2
direction: right
fixed: "Fixed shape\n@Query JSON + ?0" {
  style.fill: "#e3f2fd"
}
repo: "MongoRepository\nmethod" {
  style.fill: "#fff3e0"
}
dyn: "Runtime filters\nCriteria + Query" {
  style.fill: "#e8f5e9"
}
tmpl: "MongoTemplate.find\n/ update / count" {
  style.fill: "#f3e5f5"
}

fixed -> repo
dyn -> tmpl
```

**Fig. 1.** Prefer repository `@Query` for stable MQL; prefer `MongoTemplate` when the predicate or operation is built at runtime.

> [!warning] Wrong query language
> Mongo `@Query` strings are **MongoDB query documents**, not JPQL/`@Query` from Spring Data JPA. Copying JPQL into a Mongo repository method fails at parse/runtime.

> [!warning] `@Query` does not replace the template
> A repository `@Query` cannot express “add this clause only if the caller sent a value.” Push those cases to `MongoTemplate` (or a custom fragment) instead of exploding derived method overloads.

> [!tip] Interview answer
> For a fixed Mongo filter I put MQL JSON on `@Query` with positional placeholders. For dynamic filters I build `Criteria`, wrap them in `Query`, and run `mongoTemplate.find`. Repository `@Query` is Mongo JSON, not JPQL — and optional predicates belong on the template side.

See [[What is the difference between MongoRepository and MongoTemplate]], [[How do you use the Query annotation on a MongoRepository]], and [[How do you build a dynamic Mongo query with Criteria]].
