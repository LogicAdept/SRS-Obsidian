<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Persistence/Hibernate/Query #SRS

# What kinds of queries can Hibernate run?

> [!abstract] Short answer
> Hibernate’s `QueryProducer` (`Session` / `StatelessSession`) names **three ways to write** a query: **HQL** (object SQL, **superset of JPQL**), **native SQL** of the database, and the **JPA Criteria API** (plus Hibernate’s `HibernateCriteriaBuilder`). Orthogonal to that: **selection** (`select` → `SelectionQuery` / `getResultList`) vs **mutation** (`insert`/`update`/`delete` → `MutationQuery` / `executeUpdate`). **Named queries** are the same four cells, looked up by name. JPA’s `Query` mixes select and mutate; Hibernate splits them. Result type is a **`Class`**: entity, scalar, or constructor/record.

## Language × select vs mutate

| | **Selection** | **Mutation** |
| --- | --- | --- |
| **HQL / JPQL** | `createSelectionQuery(hql, Class)` | `createMutationQuery(hql)` |
| **Native SQL** | `createNativeQuery(sql, Class)` (+ optional `SqlResultSetMapping` name) | `createNativeMutationQuery(sql)` |
| **Criteria** | `createSelectionQuery(CriteriaQuery)` | `createMutationQuery(CriteriaUpdate/Delete/JpaCriteriaInsert)` |
| **Named** | `createNamedSelectionQuery(name, Class)` | `createNamedMutationQuery(name)` |

Passing a **select** string to `createMutationQuery` throws **`IllegalMutationQueryException`** (and the reverse **`IllegalSelectQueryException`**). Untyped `createQuery(String)` is **deprecated** — pass a result class.

**HQL** is [[What is Hibernate Query Language HQL]]; portable subset is [[What is the difference between JPQL and Hibernate HQL|JPQL]]. Criteria is type-safe JPQL; `HibernateCriteriaBuilder` adds HQL-only trees (CTEs, `from` a subquery, `createQuery(hql, Class)` to **edit** HQL as criteria). Native SQL is **not** portable; Hibernate **does not parse** it — you map columns via result class / `@SqlResultSetMapping`. Legacy `addEntity`/`addScalar` is **disfavored**.

**Stored procedures** sit on the same `CommonQueryContract` family (`createStoredProcedureQuery` / `ProcedureCall`).

```d2
direction: down
lang: "HQL | native SQL | Criteria" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
kind: "SelectionQuery vs MutationQuery" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
run: "getResultList / executeUpdate" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

lang -> kind -> run
```

**Fig. 1.** Express the query one of three ways; execute as select or DML.

## Native flush and named strings

Before a **native** select, Hibernate must know **query spaces** (tables) to decide **auto-flush**. JPA has no standard for that. Declare spaces with `NamedNativeQuery.querySpaces()` or `addSynchronizedEntityClass`. **JPA-compliant `FlushModeType.AUTO`**: flush native queries when spaces are **unknown**. **Native Hibernate AUTO**: **do not** flush unless spaces are known and overlap pending writes — stale reads after unflushed `persist` are a classic trap.

[[What are Hibernate named queries|Named queries]] register HQL or SQL **once** (`@NamedQuery` / `@NamedNativeQuery`). `createNamedSelectionQuery` / `createNamedMutationQuery` run them.

```java
List<Book> books = session
    .createSelectionQuery("from Book b where b.title like :t", Book.class)
    .setParameter("t", "Hibernate%")
    .getResultList();

int n = session.createMutationQuery("delete Draft d where d.expired = true")
    .executeUpdate();

List<IsbnTitle> rows = session.createNativeQuery(
    "select isbn, title from books order by title", IsbnTitle.class)
    .getResultList();
```

**Listing 1.** Conceptual: HQL select, HQL delete, native select into a DTO/record.

Bulk mutation **does not** update the persistence context. `JOIN FETCH` is HQL/Criteria, not native SQL.

> [!warning] Native SQL is a different contract than HQL
> Tables and columns are legal in SQL and **illegal** in HQL. Without synchronized query spaces, Hibernate AUTO **may skip flush**, so a native select **misses** entities you just `persist`. `createNativeQuery("select * from books", Book.class)` still needs a matching entity mapping. Criteria is not “no SQL” — it compiles to the same dialects. Do not call `getResultList` on a `MutationQuery`.

> [!tip] Interview answer
> Hibernate runs HQL (JPQL plus extensions), native SQL, and Criteria, each as either a selection or a mutation. I use createSelectionQuery with a result class for reads and createMutationQuery plus executeUpdate for bulk writes. Named queries are those same strings registered once. Native SQL is for vendor features and needs explicit result mapping and query spaces so flush stays correct.

See [[What is Hibernate Query Language HQL]], [[What is the difference between JPQL and Hibernate HQL]], [[What are Hibernate named queries]], [[What is Hibernate as an ORM framework]], [[What is Hibernate performance tuning]], and [[What is the N plus one problem in Hibernate]].
