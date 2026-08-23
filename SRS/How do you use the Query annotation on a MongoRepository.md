<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Annotations #SRS

# How do you use the Query annotation on a MongoRepository?

> [!abstract] Short answer
> Put **`@Query`** on a repository method with a **MongoDB JSON** filter string. Method parameters bind as **`?0`, `?1`, …** into that JSON. The annotated query overrides name-derived query logic; use `fields`, `sort`, and SpEL (`?#{…}`) for projection and dynamic fragments.

## JSON query on the repository method

When derived method names or simple `Criteria` are awkward, declare the Mongo filter directly on `MongoRepository` / `ReactiveMongoRepository`.

```java
public interface UserRepository extends MongoRepository<User, String> {

  @Query("{ '_id' : ?0 }")
  Optional<User> findByCustomId(String id);

  @Query("{ 'status' : ?0, 'age' : { $gte : ?1 } }")
  List<User> findActiveUsersOlderThan(String status, int age);

  @Query(value = "{ 'firstname' : ?0 }",
         fields = "{ 'firstname' : 1, 'lastname' : 1 }")
  List<User> findNamesByFirstname(String firstname);
}
```

**Listing 1.** Index placeholders in BSON JSON; optional `fields` projection (Spring Data MongoDB repository query methods).

The **`value`** attribute is the filter document. It takes precedence over the method name for query derivation. Add **`sort = "{ age : -1 }"`** for default ordering (overridable with a method `Sort` parameter). **`hint`** and **`readPreference`** are also supported on the annotation.

```d2
direction: right
repo: "@Query on\nMongoRepository method" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
json: "MongoDB JSON\n{ status: ?0, … }" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
run: "Repository proxy\n→ find / count" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

repo -> json -> run
```

**Fig. 1.** Repository stays declarative; the string is Mongo query syntax, not JPQL.

For conditional JSON, SpEL placeholders such as `@Query("{ 'lastname': ?#{[0]} }")` embed method arguments or expressions. That is still repository-level — **aggregation pipelines** (`$group`, `$lookup`) belong on **`MongoTemplate.aggregate`**, not on `@Query`.

> [!warning] BSON placeholders, not JPQL names
> Mongo `@Query` uses **`?0`-style** binding in JSON, not JPA-style `:name` (unless combined with SpEL). Field names must match stored BSON keys (`@Field` aliases). Complex runtime filter matrices still fit **`Criteria` + `MongoTemplate`** or Specifications on the JPA side.

See [[What is MongoRepository]], [[How do you build a dynamic Mongo query with Criteria]], and [[How do you perform aggregation with Spring Data MongoDB]].

> [!tip] Interview answer
> I annotate a `MongoRepository` method with `@Query` and a JSON filter like `{ 'status': ?0, 'age': { $gte: ?1 } }`, binding args with `?0`, `?1`. Optional `fields` limits projection. It replaces query-by-name for that method. Aggregations stay on `MongoTemplate`, not `@Query`.
