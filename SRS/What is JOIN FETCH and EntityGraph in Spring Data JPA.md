<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Persistence/JPA #SRS

# What is JOIN FETCH and EntityGraph in Spring Data JPA?

> [!abstract] Short answer
> **`JOIN FETCH`** (JPQL) loads an association **as a side effect of the query** so lazy proxies are already initialized. **`@EntityGraph`** is Spring Data’s way to apply a JPA **fetch/load graph** on a repository method (named `@NamedEntityGraph` or ad-hoc `attributePaths`) **without rewriting the JPQL** — including on derived `findBy…` methods.

## JOIN FETCH (query language)

Jakarta Persistence: a **FETCH JOIN** returns associated entities as a side effect even though they are not in the `SELECT` list:

```java
@Query("""
  select d from Department d
  left join fetch d.employees
  where d.deptNo = :deptNo
  """)
Department findWithEmployees(@Param("deptNo") int deptNo);
```

**Listing 1.** Explicit fetch join in a Spring Data `@Query` (JPQL shape from the Jakarta Persistence tutorial).

Use when you control the query text and need those associations in **one round-trip**. Collection fetch joins can **multiply parent rows**; providers often struggle with **multiple bag/collection fetch joins** in a single query — prefer one collection fetch, `DISTINCT` where appropriate, or graphs/batch fetching instead.

## @EntityGraph (repository annotation)

Spring Data JPA wires JPA 2.1 entity graphs onto repository methods:

```java
// Named graph defined on the entity with @NamedEntityGraph
@EntityGraph(value = "GroupInfo.detail", type = EntityGraphType.LOAD)
GroupInfo getByGroupName(String name);

// Ad-hoc paths — no @NamedEntityGraph required
@EntityGraph(attributePaths = { "members" })
GroupInfo getByGroupName(String name);
```

**Listing 2.** Named vs ad-hoc graphs from Spring Data JPA query-methods docs.

- **`type`**: `FETCH` (default) vs `LOAD` — matches JPA fetchgraph vs loadgraph semantics for attributes **not** listed in the graph.
- If **`attributePaths`** is set, the named `value` is ignored (dynamic graph).
- Works on **derived** methods and `@Query` methods alike — fetch plan stays out of the method name / JPQL string.

```d2
direction: right
q: "Repository method" {
  style.fill: "#e3f2fd"
}
jpql: "JOIN FETCH in @Query" {
  style.fill: "#fff3e0"
}
graph: "@EntityGraph\nnamed or attributePaths" {
  style.fill: "#e8f5e9"
}
em: "One query +\ninitialized associations" {
  style.fill: "#f3e5f5"
}

q -> jpql -> em
q -> graph -> em
```

**Fig. 1.** Two ways to eager-fetch associations for a repository call.

## Choosing

| Prefer | When |
| --- | --- |
| **`JOIN FETCH`** | Custom JPQL/Criteria where you want the join visible in the query |
| **`@EntityGraph`** | Derived finders, reuse of `@NamedEntityGraph`, keep query text clean |

Neither replaces a transaction: if you navigate **other** still-lazy associations after the query, you still need an open persistence context (or another fetch).

> [!warning] Fetch plan ≠ “load everything forever”
> Associations not covered by the fetch join / graph stay lazy (subject to fetch vs load graph rules). Touching them later can still N+1.

> [!tip] Interview answer
> `JOIN FETCH` embeds the fetch in JPQL. `@EntityGraph` applies a JPA fetch/load graph on the repository method — named or with `attributePaths` — so derived queries can avoid N+1 without stuffing JPQL. Watch cartesian products when fetch-joining collections.

See [[What is the N plus 1 problem in Spring Data JPA]], [[Which Spring Data JPA annotations have you used]], and [[What is Open Session In View in Spring]].
