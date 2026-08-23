<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# What is Query by Example in Spring Data?

> [!abstract] Short answer
> **Query by Example (QBE)** builds a store query from a partially filled domain object (**probe**) plus an optional **`ExampleMatcher`**, wrapped as an **`Example`**. You do not write field names in a query string. Repositories that extend **`QueryByExampleExecutor`** (including `JpaRepository` and `MongoRepository`) run `findAll` / `findOne` / `count` / `exists` against that example.

## Probe, matcher, example

| Part | Role |
| --- | --- |
| Probe | Domain instance with the values you care about |
| `ExampleMatcher` | How to match strings, nulls, ignore paths, case |
| `Example` | Immutable pair of probe + matcher |

By default, **`null` properties are ignored**. **Primitive** fields (`int`, `boolean`, …) are **always included** unless you `withIgnorePaths(…)`.

```java
Employee probe = new Employee();
probe.setDepartment("Engineering");
probe.setActive(true);

ExampleMatcher matcher = ExampleMatcher.matching()
    .withIgnorePaths("id")
    .withStringMatcher(ExampleMatcher.StringMatcher.CONTAINING)
    .withIgnoreCase();

Example<Employee> example = Example.of(probe, matcher);
List<Employee> employees = employeeRepository.findAll(example);
```

**Listing 1.** Probe + matcher → `Example.of` → `QueryByExampleExecutor.findAll` (Spring Data Commons QBE).

`ExampleMatcher.matchingAny()` ORs probe predicates instead of requiring all set fields to match. Per-path options use `withMatcher("firstname", endsWith())`. Fluent `findBy(example, q -> q.page(…))` adds sort, projection, and paging.

```d2
direction: right
probe: "Probe object\nset fields" {
  style.fill: "#e3f2fd"
}
match: "ExampleMatcher\nignore / string / null" {
  style.fill: "#fff3e0"
}
ex: "Example.of(…)" {
  style.fill: "#e8f5e9"
}
repo: "QueryByExampleExecutor\nfindAll / findOne" {
  style.fill: "#f3e5f5"
}

probe -> ex
match -> ex -> repo
```

**Fig. 1.** QBE pipeline from probe configuration to repository execution.

## Fit and limits

Good for dynamic filters without JPQL/MQL strings and for refactoring domain property names safely. **Not** for nested OR/AND groups like `firstname = ?0 or (firstname = ?1 and lastname = ?2)`. String matching is **store-specific**; other types use exact matching.

> [!warning] Ignore identifier paths
> An unset or default `id` (and similar) can skew the match. Prefer `withIgnorePaths("id")` unless you intentionally filter by id. Primitives on the probe always participate unless ignored.

> [!warning] Mongo typed examples add `_class`
> On MongoDB, default typed Example matching restricts by type key (often `_class`). Use an **`UntypedExampleMatcher`** when that restriction is unwanted — see `MongoRepository.findAll(Example)` docs.

> [!tip] Interview answer
> Query by Example takes a probe domain object and an `ExampleMatcher`, builds an `Example`, and runs it through `QueryByExampleExecutor`. Null fields are skipped by default; primitives are not. It avoids writing query strings for simple dynamic filters but cannot express complex nested boolean trees — then use Specifications, `@Query`, or `Criteria`.

See [[What is QuerydslPredicateExecutor in Spring Data]], [[What are Spring Data JPA Specification queries]], and [[What is MongoRepository]].
