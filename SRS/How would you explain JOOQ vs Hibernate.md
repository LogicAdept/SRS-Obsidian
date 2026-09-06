<!--
reps: 0
priority: 0
-->
#Java/Persistence/JOOQ #Java/Persistence/Hibernate #SRS

# How would you explain JOOQ vs Hibernate?

> [!abstract] Short answer
> **jOOQ** is a type-safe **SQL** DSL (plus optional schema codegen): you write queries in Java that map to SQL, compile-checked to a useful extent, and execute them. **Hibernate** is an **ORM**: it persists an **object graph** through a `Session` / JPA `EntityManager` (dirty checking, lazy proxies, caches). jOOQ is **not** a JPA replacement. Official manuals treat them as complements: SQL/analytics/ETL vs graph CRUD.

## SQL statements vs a persistence context

jOOQ models SQL as a Java DSL. Generated tables/columns make schema changes fail at compile time. The DSL’s BNF-style interfaces reject many illegal query shapes (`join` before `from`, missing `on`, degree/type mismatches in `IN` subqueries). That check is **not** a full SQL validator: codegen is optional, and plain SQL bypasses it. What Hibernate is: [[How would you explain Hibernate]]. JPA as the ORM API: [[What is the Java Persistence API JPA]].

Hibernate solves loading a graph, mutating it in memory, and writing it back (order of DML, batching, transaction footprint, optimistic locking). A managed entity is dirty-checked and flushed; associations may be uninitialized proxies. First- and second-level caches live on the `Session` / `SessionFactory`.

jOOQ’s main job is executing SQL. It also has `UpdatableRecord` CRUD: `store()` / `delete()` / `refresh()` on an attached record. Records keep per-column original/touched/modified flags so `store()` writes only dirty columns. That is **record-level** tracking you trigger with `store()`. It is not Hibernate’s persistence context: changing a POJO does not auto-flush at commit.

```d2
direction: down
app: "application" {
  width: 140
  height: 40
}
jooq: "jOOQ DSL / SQL\nfetch, store()" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
hib: "Hibernate Session\ngraph, flush, L1" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
db: "relational database" {
  width: 180
  height: 40
}
app -> jooq
app -> hib
jooq -> db
hib -> db
```

**Fig. 1.** Same database. jOOQ speaks SQL. Hibernate speaks managed entities.

```java
Result<Record> rows = create.select(BOOK.TITLE, AUTHOR.LAST_NAME)
    .from(BOOK)
    .join(AUTHOR).on(BOOK.AUTHOR_ID.eq(AUTHOR.ID))
    .where(AUTHOR.YEAR_OF_BIRTH.gt(1920))
    .fetch();

Book book = session.find(Book.class, 1L);
book.setTitle("1984"); // dirty-checked; SQL at flush
```

**Listing 1.** Conceptual. Left: jOOQ SQL (types from generated `BOOK` / `AUTHOR`). Right: Hibernate managed entity.

jOOQ 3.15+ can build nested results with `MULTISET` / `MULTISET_AGG` without an ORM session. Hibernate can run **native SQL** (windows, CTEs) too; jOOQ’s edge is composing that SQL in type-safe Java rather than strings. Spring JDBC vs Hibernate is the string-SQL cousin of this split: [[How would you explain JdbcTemplate Hibernate]].

## When manuals say to combine them

SQL is the better language for reports and analytics on large sets, ETL import/export, and complex business logic as queries — that is where jOOQ fits. Object-graph persistence is where JPA/Hibernate fit. A documented community pattern is Hibernate for most CRUD and jOOQ for the rest where SQL is required. jOOQ is not “no CRUD”: `UpdatableRecord` covers simple table CRUD without a session.

> [!warning] Compile-time safety is partial
> Removing a column breaks generated code. Illegal DSL chaining often fails to compile. Dynamic/plain SQL and a skipped generator do not get that guarantee. Hibernate JPQL is also checked only to the extent the provider/metamodel allows — neither tool makes every bad query a compiler error.

> [!warning] Two dirty models, two caches
> `session.find` then a jOOQ `UPDATE` on the same row does not update the managed instance or the second-level cache. Flush/evict/refresh, or do graph writes through Hibernate. jOOQ `store()` is explicit; Hibernate flush is implicit for persistent instances.

> [!tip] Interview answer
> Hibernate is an ORM with a persistence context: lazy loading, dirty checking, caches, entity graphs. jOOQ is type-safe SQL in Java, with optional schema codegen and compile-checked DSL, not a Session. Use Hibernate when you persist a domain graph; use jOOQ when the unit of work is a SQL statement. They are designed to sit side by side, not as drop-in replacements.
