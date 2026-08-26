<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is Spring JDBC?

> [!abstract] Short answer
> **Spring JDBC** is the Spring Framework **`spring-jdbc`** support: a **JDBC abstraction** so you write **SQL and per-row work**, while Spring **opens/closes** the connection, statement, and `ResultSet`, **runs** the statement, **iterates** results, **translates `SQLException`**, and can **join Spring transactions**. The central API is **`JdbcTemplate`** (fluent **`JdbcClient`** since **6.1**). It is **not** an ORM and **not** Spring Data JPA.

## Who does what

Spring *Data Access with JDBC* — the point of the abstraction:

| Action | Spring | You |
| --- | --- | --- |
| Define connection parameters | | X |
| Open the connection | X | |
| Specify the SQL | | X |
| Declare parameters and values | | X |
| Prepare and run the statement | X | |
| Loop the `ResultSet` | X | |
| Work for each row | | X |
| Process exceptions | X | |
| Handle transactions | X | |
| Close connection, statement, `ResultSet` | X | |

That is **plain JDBC with less ceremony**, not derived-query repositories. Compare: [[What is the difference between JDBC and Spring JDBC]], [[What is the difference between Spring JDBC and Spring Data JPA]].

```java
int updated = jdbcTemplate.update(
        "insert into t_actor (first_name, last_name) values (?, ?)",
        "Leonor", "Watling");
```

**Listing 1.** Conceptual Framework `update` — you still wrote the SQL. Template: [[What is Spring JdbcTemplate]].

```d2
direction: down
you: "SQL + params\n+ RowMapper / update args" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
mod: "spring-jdbc\nJdbcTemplate / JdbcClient" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
jdbc: "JDBC Driver\nDataSource" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}

you -> mod -> jdbc
```

**Fig. 1.** Pieces that usually sit together: [[What are the key components of Spring JDBC]], pooling [[What is connection pooling in Spring JDBC]], exceptions [[How does Spring JDBC translate SQLException]].

DAO chapter: same **`DataAccessException`** tree as other Spring templates so JDBC code can live next to JPA/Hibernate without catching vendor `SQLException` in every method — [[What is Spring DAO support]]. `@Repository` is the documented way to keep translation on.

> [!warning] Not Spring Data
> **Spring Data JPA** (and **Spring Data JDBC**) are **separate projects** with repository interfaces. Framework **Spring JDBC** is `JdbcTemplate` and friends.

> [!warning] No official “60–70% less boilerplate”
> Spring shows the **who-does-what table**, not a measured percentage. Do not quote a dump number.

> [!warning] You still own the SQL
> Bad queries, missing indexes, and wrong bind types are still yours. Spring does not parse business intent out of a string.

> [!tip] Interview answer
> **Spring JDBC is Framework support so JDBC does not mean a page of try/finally around `Connection`.** You supply SQL and row logic; Spring runs, iterates, closes, and maps `SQLException` to `DataAccessException`. `JdbcTemplate` is the usual entry. It is not JPA.

## See also

- [[What is Spring JdbcTemplate]]
- [[What is JdbcClient]]
- [[What is NamedParameterJdbcTemplate]]
- [[Is JdbcTemplate thread-safe]]
- [[How do you configure a DataSource in Spring]]
- [[What is the DataAccessException hierarchy]]
