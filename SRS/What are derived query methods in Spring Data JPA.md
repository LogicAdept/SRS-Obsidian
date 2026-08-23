<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS

# What are derived query methods in Spring Data JPA?

> [!abstract] Short answer
> **Derived query methods** are repository interface methods whose **name encodes the query** — Spring Data parses the prefix (`findBy`, `countBy`, `deleteBy`, …) and property predicates, then generates **JPQL** (or uses a declared `@Query` when the name is not enough). No `@Query` annotation is required for straightforward filters.

## How the name becomes a query

Spring Data JPA follows the shared **Query Methods** rules. A method like `findByEmailAddressAndLastname` becomes JPQL along the lines of `select u from User u where u.emailAddress = ?1 and u.lastname = ?2`. The parser walks **property paths** on the domain type (including nested properties such as `address.city`).

```java
public interface UserRepository extends JpaRepository<User, Long> {

  List<User> findByLastName(String lastName);
  List<User> findByAgeGreaterThan(int age);
  User findByEmailAddress(String emailAddress);
  List<User> findByFirstnameAndLastname(String firstname, String lastname);
  List<User> findByStartDateBetween(LocalDate start, LocalDate end);
  List<User> findByActiveTrueOrderByLastnameDesc();
}
```

**Listing 1.** Common derived patterns: equality, comparisons, `Between`, boolean flags, `OrderBy` (Spring Data JPA query-methods reference).

Supported keywords include `And`, `Or`, `LessThan`, `GreaterThan`, `Like`, `In`, `IsNull`, `True`/`False`, `IgnoreCase`, and more. Return type can be a single entity, `List`, `Optional`, `Page`/`Slice` (with `Pageable`), or a count/delete result depending on the prefix.

```d2
direction: right
iface: "Repository method name\nfindByAgeGreaterThan" {
  style.fill: "#e3f2fd"
}
parser: "Spring Data\nquery parser" {
  style.fill: "#fff3e0"
}
jpql: "Generated JPQL\nselect … where age > ?1" {
  style.fill: "#e8f5e9"
}
run: "JPA provider\n(Hibernate)" {
  style.fill: "#f3e5f5"
}

iface -> parser -> jpql -> run
```

**Fig. 1.** Method name → generated JPQL → executed by the persistence provider.

## When to stop deriving

Derived names work well for simple CRUD filters. When the parser lacks a keyword, the name becomes unreadable, or you need joins/projections/native SQL, switch to **`@Query`**, **`@NamedQuery`**, or **Specifications** — see [[How do you handle dynamic queries in Spring Data JPA]] and [[How do you define a native query in Spring Data JPA]].

Prefixes beyond **`findBy`** include **`readBy`**, **`getBy`**, **`queryBy`**, **`countBy`**, and **`deleteBy`** (same predicate grammar, different operation).

> [!warning] Property paths must resolve
> Each segment in the method name must map to a property on the entity (or a supported association path). A typo or unknown property fails at **startup** during repository bootstrap, not at first call.

> [!warning] Long derived names do not scale
> Chaining many `And` / `GreaterThan` clauses produces fragile, unreadable method names and still cannot express every query. Prefer `@Query` or dynamic criteria once the name stops being obvious.

> [!tip] Interview answer
> Derived query methods let Spring Data build JPQL from the repository method name — `findByLastName`, `findByAgeGreaterThan`, `findByActiveTrueOrderByLastnameDesc`, and so on. Property names must match the entity model. Use them for simple filters; move to `@Query` or Specifications when the name gets ugly or the query is too rich.

See [[What is Spring Data JPA]], [[What are derived query methods in Spring Data MongoDB]], and [[How do you handle dynamic queries in Spring Data JPA]].
