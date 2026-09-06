<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS

# What is the JPA Criteria API?

> [!abstract] Short answer
> The **Jakarta Persistence Criteria API** builds queries as **Java objects** (`CriteriaQuery`, `Predicate`, `Root`, …) instead of a **JPQL string**. Semantics match the query language: same abstract schema (entities and relationships), materialized as **metamodel** objects. You get `CriteriaBuilder` from `EntityManager` / `EntityManagerFactory`, then `em.createQuery(criteriaQuery)`. String JPQL: [[What is the difference between JPQL and Hibernate HQL]]. What JPA is: [[What is the Java Persistence API JPA]].

## Object graph with JPQL semantics

Criteria queries are an object-based query **graph**. Nodes are semantic elements (`from`, `join`, `where`, `select`). Java variables that point at entity/embeddable nodes play the same role as JPQL **identification variables**.

`CriteriaBuilder` constructs `CriteriaQuery`, `CriteriaUpdate`, and `CriteriaDelete`. A `CriteriaQuery` is **typed** by its result class (`createQuery(Book.class)`, `createTupleQuery()`, or untyped `createQuery()`). `from` adds a **root** (like a JPQL range variable). Extra roots are a **cartesian product**. Joins, fetch joins, paths, restrictions, parameters, subqueries, and the select list mirror JPQL.

Two equivalent construction styles:

- **Strongly typed** — static metamodel (`Book_.title`) or runtime `jakarta.persistence.metamodel` types.
- **String names** — `book.get("title")`. Same expressiveness; **no** compile-time attribute checking.

Execute with `EntityManager.createQuery(CriteriaQuery)` → `TypedQuery` / `Query`, then `getResultList` / `getSingleResult` like any other select. `CriteriaBuilder` and `Metamodel` from an `EntityManager` are valid only while that manager is **open**.

```d2
direction: down
jpql: "JPQL string\n\"select b from Book b\"" {
  width: 260
  height: 45
}
crit: "Criteria API\nCriteriaQuery + Root + Predicate" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
meta: "metamodel\nBook_ / EntityType" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
meta -> crit
crit -> jpql: "same semantics"
```

**Fig. 1.** Criteria is JPQL as a typesafe (or string) object graph, not a second query language.

```java
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery<Book> q = cb.createQuery(Book.class);
Root<Book> book = q.from(Book.class);
q.select(book).where(cb.equal(book.get(Book_.title), "Dune"));
List<Book> result = em.createQuery(q).getResultList();
```

**Listing 1.** Conceptual. `Book_` is the generated static metamodel (`Book` → `Book_`). `book.get("title")` is the string alternative.

Hibernate’s Javadoc: the JPA Criteria API can express **any standard JPQL** query. Hibernate adds `HibernateCriteriaBuilder` for extras beyond JPQL — those calls are **not** portable. Programmatic HQL: [[What is Hibernate Query Language HQL]].

> [!warning] String paths are not “Criteria safety”
> `root.get("titel")` compiles and fails at runtime. The type-safe story is **`Book_.title`** (or the metamodel API). Generating the canonical `*_` classes is the usual setup.

> [!warning] Two from() calls are a cartesian product
> Each extra query root multiplies rows. That is a join you did not write. Prefer `join` for associations. Fetch joins exist on the Criteria API the same way they do in JPQL.

> [!tip] Interview answer
> The JPA Criteria API builds the same queries as JPQL, but as Java objects instead of strings, so you can compose them dynamically and, with the static metamodel, check attributes at compile time. You obtain a CriteriaBuilder, build a CriteriaQuery, and pass it to EntityManager.createQuery. String attribute names work but throw away that type safety.
