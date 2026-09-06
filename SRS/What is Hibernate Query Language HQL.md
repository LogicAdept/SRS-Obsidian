<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Java/Persistence/Hibernate/Query #SRS

# What is Hibernate Query Language HQL?

> [!abstract] Short answer
> **HQL** is Hibernate’s **object query language**: SQL-shaped statements whose `from` items are **entity classes** and whose paths are **Java attributes**, not tables and columns. It is a **superset of JPQL** (JPQL began as a subset of early HQL). You write `select` / `update` / `delete`, plus HQL-only **`insert … values` / `insert … select`**. Hibernate 6/7 **recompiled** the language; the current HQL guide is the reference. Run it on a `Session` with **`createSelectionQuery(hql, Class)`** or **`createMutationQuery(hql)`**. Strict JPQL-only mode is `hibernate.jpa.compliance.query=true` (an exception if you use an HQL extension).

## Object SQL, not table SQL

If you can read SQL `select … from Book join Publisher … where title like …`, you can read the HQL twin. The difference: **`Book` is an entity**, **`book.title` is a field**. Tables and columns are **not** legal in HQL/JPQL. The compiler emits SQL through the **`Dialect`**. Queries are usually **shorter** than that SQL.

**JPQL is a proper subset.** Portable JPA sticks to JPQL; HQL adds `insert`, richer functions, optional `select` inference, and more. See [[What is the difference between JPQL and Hibernate HQL]].

| Kind | Role |
| --- | --- |
| **`select`** | Load entities, scalars, constructors / records. `getResultList` / `getSingleResult`. |
| **`update` / `delete`** | Bulk mutation. `executeUpdate()`. **Polymorphic** (subclasses too). **No direct join**; implicit join or subquery joins only. Default `update` **does not** bump `@Version` unless **`update versioned`**. |
| **`insert`** | **Not JPQL.** `insert … values` or `insert … select`. **Not polymorphic.** Prefer `persist()` except for bulk/test data. |

Keywords and function names are **case-insensitive**; **Java class names, attributes, and identification variables are case-sensitive** (JPQL treats identification variables as case-insensitive; compliance mode follows that). Standard style is **lowercase keywords**.

Queries are **polymorphic**: `from Payment` returns `Payment` **and mapped subclasses**. `from java.lang.Object` is legal and returns **every mapped entity** — almost never what you want.

```d2
direction: right
hql: "HQL string\nentities + paths" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
cmp: "HQL compiler\n(Hibernate 6+)" {
  width: 180
  height: 80
  style.fill: "#fff3e0"
}
sql: "SQL + Dialect\nJDBC" {
  width: 160
  height: 80
  style.fill: "#e8f5e9"
}

hql -> cmp -> sql
```

**Fig. 1.** HQL names the domain model; Hibernate compiles it to vendor SQL.

## How you run it

`QueryProducer` (`Session` / `StatelessSession`): HQL **selection** → `createSelectionQuery(String, Class)`; HQL **mutation** → `createMutationQuery(String)`. `createQuery` still exists for JPA `TypedQuery` compatibility. Pass a **result class**. Bind **parameters** — never concatenate user text into HQL.

| Parameter | Example | Bind |
| --- | --- | --- |
| Named | `:title` | `setParameter("title", v)` |
| Ordinal | `?1` | `setParameter(1, v)` |
| JDBC `?` | deprecated | inferred index |

Comments are Java `/* … */` only — not `--` or `//`.

```java
List<Book> books = session
    .createSelectionQuery(
        "from Book b left join fetch b.authors where b.title like :title",
        Book.class)
    .setParameter("title", title)
    .setMaxResults(50)
    .getResultList();
```

**Listing 1.** Conceptual: typed HQL select with a named parameter and `join fetch`.

Named strings live in [[What are Hibernate named queries]]. Native SQL is a **different** API (`createNativeQuery`). Criteria is the type-safe sibling. Together they are [[What kinds of queries can Hibernate run]].

**Mutation vs L1:** `update`/`delete` **do not** refresh managed instances. You must keep memory in sync (or `clear`). Bulk HQL is a [[What is Hibernate performance tuning]] tool precisely because it **skips** loading entities.

> [!warning] String-built HQL is SQL injection
> Concatenating request strings into HQL lets the client run **arbitrary database code**. Use `:name` / `?1`. After `createMutationQuery("update …").executeUpdate()`, objects already in the **persistence context still have the old field values**. `insert` is **not** portable JPQL. `from Object` scans the whole metamodel.

> [!tip] Interview answer
> HQL is Hibernate’s SQL-like language over entities and attributes, and JPQL is the portable subset of it. I run selects with createSelectionQuery and a result class, always with named or ordinal parameters. HQL also has insert plus bulk update and delete, which hit SQL without updating the persistence context. Hibernate 6 rebuilt the compiler; I do not treat table-and-column SQL as legal HQL.

See [[What is the difference between JPQL and Hibernate HQL]], [[What kinds of queries can Hibernate run]], [[What are Hibernate named queries]], [[What is Hibernate as an ORM framework]], [[What is Hibernate performance tuning]], and [[What is the N plus one problem in Hibernate]].
