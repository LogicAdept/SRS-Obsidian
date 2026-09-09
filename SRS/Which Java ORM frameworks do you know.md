<!--
reps: 0
priority: 0
-->
#Java/Persistence #ORM #Career/Experience #SRS

# Which Java ORM frameworks do you know

> [!abstract] Short answer
> **The mapping stack: Hibernate and EclipseLink implement JPA; Spring Data JPA adds repositories on top; MyBatis and jOOQ take the explicit-SQL side.** Know the split — spec (JPA) versus implementation (Hibernate, EclipseLink) versus wrapper (Spring Data) versus SQL-first mappers (jOOQ, MyBatis) — and be ready to name what your project used and why.

## The landscape by role

```d2
direction: right
spec: "JPA spec\nJakarta Persistence\nannotations + EntityManager" {
  width: 290
  height: 100
  style.fill: "#e3f2fd"
}
impl: "Implementations\nHibernate | EclipseLink" {
  width: 290
  height: 100
  style.fill: "#fff3e0"
}
wrap: "On top\nSpring Data JPA repositories" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
sql: "SQL-first mappers\njOOQ DSL | MyBatis XML" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
impl -> spec: "implements"
wrap -> impl: "uses"
```

**Fig. 1.** Four roles: the specification, its implementations, the repository wrapper, and the SQL-first alternatives.

What each is actually for. **Hibernate** is the dominant JPA implementation — full object mapping, dirty checking, lazy proxies, second-level cache; its native extensions (batch fetching, `@BatchSize`, StatelessSession) go beyond the spec. **EclipseLink** is the other JPA implementation (the reference implementation historically) — same API, different internals; choosing between them matters mostly for vendor-specific features. **Spring Data JPA** "provides repository support for the Jakarta Persistence API" — Spring Data's own description: you define `interface BookRepository extends JpaRepository<Book, Long>` and derived query methods (`findByAuthorName`), plus `@Query` for custom ones; no SQL boilerplate for the standard cases. **jOOQ** generates Java code from the actual schema and builds type-safe SQL — a DSL, not an entity mapper. **MyBatis** maps hand-written SQL statements to Java methods via XML or annotations — full SQL control, minimal magic. All of them still talk to the database through JDBC — see [[Which ways can Java applications talk to a database]].

> [!warning] Naming a framework is the easy 20% of the answer
> The traps in an "which ORMs do you know" question. First, category errors: calling jOOQ or MyBatis "JPA implementations" is wrong — they never implement the `EntityManager` contract; they are SQL mappers, which is exactly why teams pick them. Second, version blindness: "Hibernate" spans JPA 1.0-era Jakarta-precursor releases through Jakarta Persistence 3.1 (Jakarta EE 10, where `GenerationType.UUID` landed) — Spring Boot 3 generation uses Jakarta namespaces, Boot 2 uses `javax.persistence`; quoting the wrong namespace dates you. Third, the follow-up always comes: "what did N+1 look like in your project and what did you do?" — having only the list without the war story ([[When does the N plus 1 query problem occur and how do you fix it]]) reads as résumé familiarity, not experience. If the interviewer wants depth, describe one mechanism concretely — persistence context behavior from [[What is object relational mapping ORM]] is the safest pick.

> [!tip] Interview answer
> **Spec versus implementation first: Jakarta Persistence (JPA) is the standard; Hibernate and EclipseLink implement it. Spring Data JPA sits on top with repository interfaces and derived queries. On the SQL-first side, jOOQ generates a type-safe DSL from the schema and MyBatis maps hand-written SQL. Everything still runs over JDBC. In my project we used Spring Data JPA over Hibernate — and hit the usual N+1, fixed with JOIN FETCH and batch fetch size.**

