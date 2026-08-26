<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# What is connection pooling in Spring JDBC?

> [!abstract] Short answer
> Spring JDBC **does not implement a pool**. It uses a **`javax.sql.DataSource`**. A **pool** keeps **open connections** and hands them out, so each `JdbcTemplate` call does not pay **connect/close**. Framework: obtain a DataSource from **JNDI** or configure a **third-party pool**. Modern recommendation: **HikariCP**. **`DriverManagerDataSource` is not a pool** — test-only.

## Pool is the DataSource bean

Docs: a `DataSource` lets a container hide **pooling and transactions**. Traditional beans: **Apache Commons DBCP**, **C3P0**. **HikariCP** with a builder-style API is the modern choice. **`DriverManagerDataSource` / `SimpleDriverDataSource`**: *only for testing* — *no pooling*, poor under concurrent checkout.

`JdbcTemplate` obtains connections through **`DataSourceUtils`**, so it **participates in Spring transactions** on a pooled DataSource.

```java
@Bean(destroyMethod = "close")
BasicDataSource dataSource() {
    BasicDataSource dataSource = new BasicDataSource();
    dataSource.setDriverClassName("org.hsqldb.jdbcDriver");
    dataSource.setUrl("jdbc:hsqldb:hsql://localhost:");
    dataSource.setUsername("sa");
    dataSource.setPassword("");
    return dataSource;
}
```

**Listing 1.** Framework DBCP sample — `destroy-method="close"`. Boot default pool: [[What is HikariCP in Spring Boot]]. Bean setup: [[How do you configure a DataSource in Spring]]. JNDI: [[How do you use a Tomcat JNDI DataSource in Spring]].

```d2
direction: down
dao: "JdbcTemplate" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
ds: "DataSource (pool)" {
  width: 200
  height: 45
  style.fill: "#fff3e0"
}
db: "database" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}

dao -> ds -> db
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Exhausted pool + leaked connections is an ops failure, not a Spring JDBC API.

> [!warning] `DriverManagerDataSource` in production examples
> It opens a **new connection** every time. Docs: a JavaBean pool is *almost always preferable* even in tests.

> [!warning] Closing connections
> Application code must not leak `Connection`/`Statement`/`ResultSet`. `JdbcTemplate` closes them; raw JDBC next to it must still close. Container pools may have **abandoned-connection** recovery (Tomcat DBCP `removeAbandoned*`).

> [!tip] Interview answer
> **Pooling is a `DataSource` implementation, not `JdbcTemplate` itself.** Use HikariCP (Boot default) or JNDI. `DriverManagerDataSource` is not a pool.

## See also

- [[What is HikariCP in Spring Boot]]
- [[How do you configure a DataSource in Spring]]
- [[What is Spring JdbcTemplate]]
