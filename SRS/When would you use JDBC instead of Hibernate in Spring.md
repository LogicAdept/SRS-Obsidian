<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/Persistence/Hibernate #SRS

# When would you use JDBC instead of Hibernate in Spring?

> [!abstract] Short answer
> Use **Spring JDBC** (`JdbcTemplate` / `JdbcClient`) when the unit of work is **SQL you write and map yourself**. Use **Hibernate** when the unit of work is a **mapped domain model** (`Session` / JPA `EntityManager`). Spring’s DAO layer lets **both** share **`DataAccessException`**. JDBC is not “Spring without Hibernate”; Hibernate is not required for every table.

## SQL you own vs objects you map

Boot: the SQL stack runs from **direct JDBC** (`JdbcClient` / `JdbcTemplate`) to **ORM such as Hibernate**. Spring JDBC *who does what*: **you specify SQL**; Spring opens/closes resources. ORM integration: **templating for JDBC**, **interceptors/templates for ORM**, same transaction and exception goals.

JDBC fits when:

- The query **is** the design (reporting, vendor SQL, explicit plans) — you do not want Hibernate to generate it.
- You need **JDBC-level** batching (`JdbcTemplate.batchUpdate`) or metadata inserts (`SimpleJdbcInsert`) without a session/flush model.
- Tables **do not map** cleanly to entities (legacy schemas, ETL staging). You still write SQL; you skip entity mapping.

Hibernate fits a **persistent object graph**, dirty checking, and associations. Simple CRUD **can** be JDBC; it can also be a few entities — neither Spring chapter forbids the other.

```java
int rows = jdbcTemplate.update(
        "insert into report_line (run_id, payload) values (?, ?)",
        runId, payload);

session.persist(order);
```

**Listing 1.** Conceptual contrast — SQL string vs entity lifecycle. JDBC module: [[What is Spring JDBC]]. Template: [[What is Spring JdbcTemplate]]. vs Spring Data JPA: [[What is the difference between Spring JDBC and Spring Data JPA]]. DAO exceptions: [[What is Spring DAO support]].

```d2
direction: right
jdbc: "You write SQL\nJdbcTemplate" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
orm: "You map entities\nSession / EM" {
  width: 200
  height: 55
  style.fill: "#fff3e0"
}
dao: "DataAccessException" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}

jdbc -> dao
orm -> dao
```

**Fig. 1.** Mixing JDBC next to ORM is explicitly supported in [[What is Spring DAO support]]. Batch: [[How does JdbcTemplate batchUpdate work]].

> [!warning] Not a one-line switch
> DAO support shares **exceptions**, not mappings. Replacing Hibernate with JDBC means **rewriting** access code.

> [!warning] “ORM is always slower”
> Hibernate can batch and native-query too. Prefer JDBC when **you need to own the SQL**, not as a blanket performance slogan.

> [!tip] Interview answer
> **JDBC when I want to write the SQL and map rows. Hibernate when I have a domain model to persist.** Spring lets both throw `DataAccessException`. Legacy or SQL-heavy paths are the usual JDBC reasons.

## See also

- [[What is Spring JDBC]]
- [[What is the difference between Spring JDBC and Spring Data JPA]]
- [[What is Spring DAO support]]
