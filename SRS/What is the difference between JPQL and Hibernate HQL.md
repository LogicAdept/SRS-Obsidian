<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Persistence/Hibernate #SRS

# What is the difference between JPQL and Hibernate HQL?

> [!abstract] Short answer
> **JPQL** is the **Jakarta Persistence** string query language: portable queries over **entities** (select / update / delete), independent of the physical schema. **HQL** is Hibernate’s query language. **JPQL was inspired by early HQL and is a subset of modern HQL.** Hibernate treats “HQL” as the full language plus that standard subset. Spec vs Hibernate: [[What is the difference between JPA as a specification and Hibernate]]. Native SQL is a third option: [[How would you explain @Query JPQL vs native SQL]].

## Portable subset versus Hibernate’s superset

Jakarta Persistence query language operates on the **abstract persistence schema** (entities, state, relationships) and compiles to SQL. Statement types in the spec: **select, update, delete**. No `insert`.

Hibernate Query Language is an **object-oriented** language based on SQL. Hibernate’s user guide: JPQL is a **subset** of modern HQL; the Javadoc query packages treat JPQL the same way. Hibernate’s intro: HQL is a **superset of JPQL** that covers most modern SQL dialect features. What HQL is as a topic: [[What is Hibernate Query Language HQL]].

HQL-only (not JPQL) includes **`insert … values` / `insert … select`**, **`with` CTEs**, **`limit` / `offset` / `fetch`**, from-first queries like `from Person`, and other dialect-facing functions. Identification variables are **case-sensitive** in HQL; JPQL defines them as **case-insensitive**. Hibernate’s `hibernate.jpa.compliance.query=true` **rejects** HQL features outside the JPQL subset (Hibernate does not recommend turning it on).

```d2
direction: down
jpql: "JPQL\nselect / update / delete\nportable JPA" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
hql: "HQL\nJPQL + insert, CTE, limit, …" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
jpql -> hql: "subset"
```

**Fig. 1.** Every legal JPQL query is HQL. The reverse is false.

```java
// Portable JPQL (and HQL)
em.createQuery("select p from Person p where p.name = :name", Person.class);

// HQL: implicit select, not something to rely on for provider portability
session.createQuery("from Person", Person.class);

// HQL only — JPQL has no insert statement
session.createMutationQuery("insert into Person (id, name) values (1, 'Ada')");
```

**Listing 1.** Conceptual. `EntityManager.createQuery` accepts JPQL; Hibernate will also accept HQL unless query compliance is on.

Bulk `update` / `delete` (both languages) **do not** update the persistence context or in-memory entities. The application must keep memory and the database in sync. That is not a JPQL-vs-HQL difference; it is a bulk-DML trap in both.

> [!warning] createQuery is not a JPQL linter
> On Hibernate, `EntityManager.createQuery` compiles **HQL**. A string that runs in tests can still be **illegal JPQL**. If you must stay portable, stay inside the spec grammar (or enable query compliance and expect breakage).

> [!warning] insert in HQL is not persist
> HQL `insert` writes SQL immediately and is **not** in JPQL. Prefer `persist` / `em.persist` for normal entity graphs. Bulk DML still skips the persistence context.

> [!tip] Interview answer
> JPQL is the JPA standard query language over entities: select, update, delete, portable across providers. HQL is Hibernate’s language; JPQL is a subset of it. Hibernate adds insert, CTEs, limits, and other extensions. If you need another JPA provider, do not use those extensions.
