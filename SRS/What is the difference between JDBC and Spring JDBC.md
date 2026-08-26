<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is the difference between JDBC and Spring JDBC?

> [!abstract] Short answer
> **JDBC** is the JDK API: **you** open a `Connection`, create a `PreparedStatement`, `execute`, walk the `ResultSet`, handle `SQLException`, and **close** everything (and usually manage transactions). **Spring JDBC** keeps **you** on **SQL + parameters + per-row mapping**; **Spring** opens, prepares, iterates, **closes**, translates exceptions, and can **enlist the connection in a Spring transaction**. You still write SQL. It is **not** Hibernate.

## Same driver, different ownership

Spring *Data Access with JDBC* table:

- **You:** connection parameters, SQL, bind values, work **per row**.
- **Spring:** open connection, prepare/run, loop `ResultSet`, exception processing, **transactions**, close connection/statement/`ResultSet`.

Raw JDBC (shape, not a paste of a tutorial):

```java
try (Connection con = dataSource.getConnection();
     PreparedStatement ps = con.prepareStatement(
             "update t_actor set last_name = ? where id = ?")) {
    ps.setString(1, lastName);
    ps.setLong(2, id);
    ps.executeUpdate();
}
```

**Listing 1.** Conceptual JDK JDBC — you own statement lifecycle. Spring equivalent:

```java
jdbcTemplate.update(
        "update t_actor set last_name = ? where id = ?",
        lastName, id);
```

**Listing 2.** Conceptual Framework `update`. Module: [[What is Spring JDBC]]. API: [[What is Spring JdbcTemplate]].

```d2
direction: right
jdbc: "JDBC\nyou: open · execute · close" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
sj: "Spring JDBC\nyou: SQL · binds · row work" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Both talk to a `DataSource` / driver. Spring is a **template over JDBC**, not a second protocol.

Exception translation is a **`JdbcTemplate` / DAO** feature (`SQLException` → `DataAccessException`) — [[How does Spring JDBC translate SQLException]]. Connection **pooling** is a **`DataSource`** choice (Boot: often **HikariCP**). **`DriverManagerDataSource` is not a pool** (javadoc: new connection every `getConnection`) — [[What is connection pooling in Spring JDBC]], [[What is HikariCP in Spring Boot]].

> [!warning] Not an ORM
> Entities, dirty checking, and JPQL are JPA/Hibernate. Spring JDBC maps **rows you selected**.

> [!warning] `new JdbcTemplate(new DriverManagerDataSource(...))` is not “production pooling”
> You get exception translation and resource closing. You do **not** get a pool. Use a real `DataSource` bean.

> [!warning] Transactions are not “because JDBC”
> Spring **can** handle transactions when a **transaction manager** and a Spring-managed connection are in play (`DataSourceTransactionManager`). A template used outside a transaction still runs autocommit JDBC unless you begin one.

> [!tip] Interview answer
> **JDBC is the low-level API you must close by hand. Spring JDBC is `JdbcTemplate`: you write SQL, Spring runs and closes and translates `SQLException`.** Same SQL, less try/finally. Not an ORM; pooling is the `DataSource`, not the template.

## See also

- [[What is Spring JDBC]]
- [[What is Spring JdbcTemplate]]
- [[What is a RowMapper in Spring JDBC]]
- [[How do you configure a DataSource in Spring]]
- [[What is the difference between Spring JDBC and Spring Data JPA]]
- [[When would you use JDBC instead of Hibernate in Spring]]
