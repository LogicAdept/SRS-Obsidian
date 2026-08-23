<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS

# What are Spring Data JPA projections?

> [!abstract] Short answer
> **Projections** let a repository method return a **partial view** of an aggregate — only the properties you declare — instead of the full managed entity. Use an **interface** with getters (closed/open) or a **DTO/record** with a matching constructor; Spring Data JPA maps the query result into that shape.

## Interface-based projections

Declare accessors whose names match entity properties. The query engine creates a **proxy** that forwards to the underlying result:

```java
interface UserSummary {
  String getFirstname();
  String getLastname();
}

interface UserRepository extends JpaRepository<User, Long> {
  List<UserSummary> findByRole(String role);
}
```

**Listing 1.** Closed interface projection — Spring Data can optimize selection to those attributes (JPA projections reference).

- **Closed** — every accessor maps to a target property (optimizable).
- **Open** — uses `@Value` / SpEL on the full aggregate; fewer query optimizations.
- Nested projections wrap associations recursively (`getAddress()` → another projection interface).

Do **not** override base `CrudRepository` methods and expect a projection return type — base methods ignore that override unless turned into a real `@Query` method.

## Class-based (DTO) projections

A record or class outside the entity hierarchy holds the projected fields. For derived queries, JPA uses **constructor expressions**; constructor **parameter names** drive which properties load when the store optimizes field selection.

```java
record UserDto(String firstname, String lastname) {}

interface UserRepository extends JpaRepository<User, Long> {
  List<UserDto> findByRole(String role);

  @Query("SELECT u FROM User u WHERE u.lastname = :lastname")
  List<UserDto> findDtoByLastname(String lastname); // rewritten to SELECT new UserDto(…)
}
```

**Listing 2.** DTO/record projection; Spring Data JPA can rewrite entity/`@Query` selections into constructor expressions.

Multiple constructors need **`@PersistenceCreator`** on the one used for projection. **Dynamic projections** pass `Class<T>` as a method argument to choose the shape at call time.

```d2
direction: right
entity: "Full entity\nUser" {
  style.fill: "#e3f2fd"
}
iface: "Interface projection\nproxy getters" {
  style.fill: "#e8f5e9"
}
dto: "DTO / record\nconstructor" {
  style.fill: "#fff3e0"
}
cols: "Selected columns\n/ Tuple" {
  style.fill: "#f3e5f5"
}

entity -> iface
entity -> dto
iface -> cols
dto -> cols
```

**Fig. 1.** Both styles return a subset view; JPA builds interface proxies from `Tuple` queries and DTOs via constructors.

> [!warning] Nested paths can still join fully
> On derived queries, projections limit **top-level** properties. Nested properties that resolve to joins can still **materialize the whole nested association** — not a surgical column pick of the child.

> [!warning] DTO constructor must match
> Class-based projections need an all-args constructor (or `@PersistenceCreator`) whose parameters align with selected properties. Mismatched or multi-constructor DTOs without a hint fail at query time.

> [!tip] Interview answer
> Spring Data JPA projections return a partial view of an entity: interface getters for a closed projection proxy, or a DTO/record via constructor expression. That cuts what you load versus `findAll` of full entities. Nested joins may still fetch whole associations, and open `@Value` projections skip the closed-projection optimizations.

See [[What is Spring Data JPA]], [[What are derived query methods in Spring Data JPA]], and [[Should you return JPA entities from a Spring controller]].
