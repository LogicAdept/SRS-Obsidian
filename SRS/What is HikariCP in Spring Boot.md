<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Spring/Framework/DataAccess #SRS

# What is HikariCP in Spring Boot?

> [!abstract] Short answer
> **HikariCP** is the **connection pool Boot prefers**. If Hikari is on the classpath, Boot **always chooses it** for a pooling `DataSource`. **`spring-boot-starter-jdbc`** and **`spring-boot-starter-data-jpa`** pull Hikari in. Tune with **`spring.datasource.hikari.*`**. A **custom `DataSource` `@Bean` disables** that auto-configuration.

## Default pool, then properties

Boot *SQL Databases*: production connections auto-configure as a **pooling** DataSource. Preference order: **HikariCP**, else Tomcat JDBC pool, else DBCP2, else Oracle UCP. Standard URL/user/password: **`spring.datasource.*`**. Pool-specific: **`spring.datasource.hikari.*`** (also `tomcat.*`, `dbcp2.*`, `oracleucp.*`).

```properties
spring.datasource.url=jdbc:postgresql://localhost/app
spring.datasource.username=app
spring.datasource.password=secret
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.connection-timeout=30000
```

**Listing 1.** Conceptual Boot properties — names from Boot DataSource / Hikari prefixes. Generic pooling: [[What is connection pooling in Spring JDBC]]. Framework bean: [[How do you configure a DataSource in Spring]].

If you need a typed builder: **`DataSourceBuilder.create().type(HikariDataSource.class)`**. Hikari’s JDBC URL property is **`jdbc-url`**, not `url` — Boot’s **`DataSourceProperties.initializeDataSourceBuilder()`** maps `spring.datasource.url` correctly; a raw Hikari bean that only calls `setUrl` is a common miss.

```d2
direction: down
props: "spring.datasource.*" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
auto: "DataSource auto-config" {
  width: 220
  height: 45
  style.fill: "#fff3e0"
}
hikari: "HikariDataSource" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}

props -> auto -> hikari
```

**Fig. 1.** `JdbcTemplate` auto-config sits on this DataSource — [[How do you configure JdbcTemplate as a bean]]. JNDI instead of URL: [[How do you use a Tomcat JNDI DataSource in Spring]].

> [!warning] Your `@Bean DataSource` replaces auto-config
> No `spring.datasource.hikari.*` metadata unless you wire **`DataSourceProperties`** (or set Hikari in code). Extra DataSource beans without `@Primary` / `@Qualifier` confuse `JdbcTemplate` auto-config.

> [!warning] Pool exhaustion is not a Hibernate bug
> Too-small **`maximum-pool-size`**, leaked connections, or a transaction that holds a connection (including **OSIV** holding it for the whole request) starves the pool. Actuator Hikari metrics help, they do not enlarge the pool.

> [!tip] Interview answer
> **Boot’s default JDBC pool is HikariCP** when the starter is on the classpath. Configure `spring.datasource.*` and `spring.datasource.hikari.*`. A custom `DataSource` bean turns auto-config off.

## See also

- [[What is connection pooling in Spring JDBC]]
- [[How do you configure a DataSource in Spring]]
- [[What is Spring JdbcTemplate]]
