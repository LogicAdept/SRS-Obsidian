<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/Persistence/Hibernate #SRS

# How would you explain JdbcTemplate Hibernate?

> [!abstract] Short answer
> **`JdbcTemplate`** is Spring’s JDBC workhorse: **you write the SQL**, it runs the JDBC workflow (statements, `ResultSet` iteration, close, `SQLException` → `DataAccessException`). **Hibernate** is an ORM: you map entities and work through a **`Session`** / JPA **`EntityManager`**, which generates or coordinates SQL and a persistence context. They are complementary. Spring can wire both on the same `DataSource` and the same transaction / DAO exception hierarchy.

## SQL you own vs objects Hibernate maps

`JdbcTemplate` (`org.springframework.jdbc.core`, Spring Framework 7) is the central JDBC delegate. Once configured it is **thread-safe** (a `DataSource`, not conversational state). `batchUpdate` groups the same prepared statement to cut round trips. As of 6.1, `JdbcClient` is a fluent facade on top of it. What the template is: [[What is Spring JdbcTemplate]].

Hibernate sits on JDBC as a Jakarta Persistence provider. `SessionFactory` maps the domain model; each `Session` is a short-lived, **not thread-safe** unit of work with a first-level cache. What Hibernate is: [[How would you explain Hibernate]]. Spring’s ORM chapter sets up `LocalSessionFactoryBean` on a JDBC `DataSource` and lets DAOs call `sessionFactory.getCurrentSession()`.

Official guidance is to **use both**. Hibernate’s query language is an object-oriented dialect of SQL; native SQL (window functions, CTEs, vendor clauses) is a first-class Hibernate API and a migration path from JDBC. If a particular access path is easier as handwritten SQL without an entity graph, `JdbcTemplate` (or Hibernate native SQL) is that path — not “never use Hibernate.” Choosing JDBC vs Hibernate in Spring: [[When would you use JDBC instead of Hibernate in Spring]].

```d2
direction: down
app: "DAO / service" {
  width: 160
  height: 40
}
jdbc: "JdbcTemplate\nyou supply SQL" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
orm: "Session / EntityManager\nmapped entities" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
db: "DataSource / database" {
  width: 180
  height: 40
}
app -> jdbc
app -> orm
jdbc -> db
orm -> db
```

**Fig. 1.** Same database, two programming models. Spring transactions and `DataAccessException` can wrap both.

```java
jdbcTemplate.query(
    "select id, name from t_actor where id = ?",
    (rs, rowNum) -> new Actor(rs.getLong("id"), rs.getString("name")),
    actorId);

session.find(ActorEntity.class, actorId);
```

**Listing 1.** Conceptual. `JdbcTemplate` maps a `ResultSet`. Hibernate returns a managed entity (dirty-checked until the `Session` ends).

## What the dump’s “use JdbcTemplate when…” actually means

- **Analytics (windows, CTEs):** that SQL can run on `JdbcTemplate` *or* `Session.createNativeQuery`. Hibernate documents native SQL specifically for windows, CTEs, and Oracle `CONNECT BY`.
- **Thousands of INSERTs:** `JdbcTemplate.batchUpdate` is the JDBC batch API. Hibernate can batch DML with `hibernate.jdbc.batch_size`, and `StatelessSession` is the no-persistence-context path for bulk row work. A set-based SQL `INSERT … SELECT` / HQL bulk update often beats row-by-row batching.
- **ORM SQL you dislike:** first option inside Hibernate is native SQL or a rewritten mapping/fetch; dropping to `JdbcTemplate` is when you do not want a persistence context at all.
- **Legacy JDBC:** Hibernate native SQL is documented as a migration path *from* JDBC; keeping `JdbcTemplate` for leftover statements is valid, not a Hibernate ban.
- **“Simple CRUD, no associations”:** not an official JdbcTemplate-only zone. That is typical ORM work. JdbcTemplate is the lowest-level Spring JDBC approach, not a CRUD micro-ORM.

> [!warning] JDBC writes are invisible to Hibernate’s caches
> A `JdbcTemplate` update does not dirty-check a managed entity. The second-level cache is not aware of changes made directly via JDBC. Flush/evict/refresh (or do the write through the `Session`) if the same rows are loaded as entities in that transaction.

> [!warning] Thread-safety is not the same product
> Share one `JdbcTemplate`. Do not share a `Session`. Mixing them in one method is fine only if you treat Hibernate’s persistence context as the source of truth for mapped instances, or you stay on SQL-only rows.

> [!tip] Interview answer
> JdbcTemplate means you write SQL and Spring runs JDBC: resources, iteration, and DataAccessException. Hibernate means you map entities and a Session dirty-checks and flushes them. Use Hibernate for the domain model, JdbcTemplate or Hibernate native SQL when you need a specific statement without an entity graph, and never assume a JDBC update is seen by a loaded entity until you refresh.
