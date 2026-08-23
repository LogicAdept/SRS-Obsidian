<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS

# What are Spring Data JPA Specification queries?

> [!abstract] Short answer
> A **`Specification`** is a reusable **Criteria API predicate** over an entity (DDD-style). Extend the repository with **`JpaSpecificationExecutor`**, then `findAll(spec)`, compose with `and`/`or`, or use the fluent `findBy(spec, q -> …)` API for paging, sorting, and projections — without a new derived method for every filter combination.

## Setup

```java
public interface CustomerRepository
    extends CrudRepository<Customer, Long>, JpaSpecificationExecutor<Customer> {
}
```

**Listing 1.** Mix CRUD with specification execution (Spring Data JPA specifications docs).

Build predicates with JPA Criteria (`Root` / `From`, `CriteriaBuilder`). Classic `Specification.toPredicate(Root, CriteriaQuery, CriteriaBuilder)`; Spring Data JPA 4.0 also adds lighter **`PredicateSpecification`** (`toPredicate(From, CriteriaBuilder)`) for easier composition, plus **`UpdateSpecification`** / **`DeleteSpecification`** for Criteria updates/deletes.

```java
static PredicateSpecification<Customer> isLongTermCustomer() {
  return (from, builder) -> {
    LocalDate date = LocalDate.now().minusYears(2);
    return builder.lessThan(from.get(Customer_.createdAt), date);
  };
}

List<Customer> customers = customerRepository.findAll(
    isLongTermCustomer().or(hasSalesOfMoreThan(amount)));
```

**Listing 2.** Spec factory methods composed with `or` (docs example shape; `Customer_` is the JPA static metamodel).

```d2
direction: right
repo: "JpaSpecificationExecutor" {
  style.fill: "#e3f2fd"
}
spec: "Specification /\nPredicateSpecification" {
  style.fill: "#fff3e0"
}
crit: "JPA Criteria API\nPredicate" {
  style.fill: "#e8f5e9"
}
db: "Database" {
  style.fill: "#f3e5f5"
}

repo -> spec -> crit -> db
```

**Fig. 1.** Repository executes composed Criteria predicates built as specifications.

## When to use

Prefer specifications for **dynamic** filters (optional request params, admin search) where method-name explosion or huge `@Query` strings hurt. Derived queries and `@Query` stay better for fixed, named use cases. Specs combine with **`Pageable`**, sorting, and projections via the fluent API:

```java
Page<CustomerProjection> page = repository.findBy(spec,
    q -> q.as(CustomerProjection.class)
          .page(PageRequest.of(0, 20, Sort.by("lastname"))));
```

**Listing 3.** Fluent `findBy` with projection + page (Spring Data JPA 4.x docs).

> [!warning] Still Criteria complexity
> Specifications do not remove JPA Criteria ceremony or metamodel setup. Wrong joins/null handling still produce bad SQL — specs are composition, not magic safety.

> [!tip] Interview answer
> Specifications wrap Criteria predicates so I can reuse and compose filters (`and`/`or`) on a `JpaSpecificationExecutor` repository. Ideal for dynamic queries; I still use derived methods or `@Query` for simple fixed finders.

See [[How do you handle dynamic queries in Spring Data JPA]], [[What is Query by Example in Spring Data]], [[What are derived query methods in Spring Data JPA]], and [[What is Spring Data JPA]].
