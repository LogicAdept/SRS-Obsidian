<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# How do you configure a `DataSource` in Spring?

> [!abstract] Short answer
> Expose a **`javax.sql.DataSource` bean**. In Framework Java config that is often **`DriverManagerDataSource`** (tests) or a **pool** (`HikariCP`, DBCP, C3P0) with URL, user, password, and **`destroyMethod = "close"`** for pooled types. Production: a **pool** or **JNDI**. Boot: **`spring.datasource.*`** auto-configures one unless you define your own bean.

## You supply connection parameters

Spring JDBC *who does what*: **you** define connection parameters; Spring **opens/closes** connections through the DataSource. Docs show **`@Bean` `DriverManagerDataSource`** with `driverClassName`, `url`, `username`, `password`, plus XML `property-placeholder`. Same pattern for **`BasicDataSource`** (DBCP) and **`ComboPooledDataSource`** (C3P0).

```java
@Bean
DriverManagerDataSource dataSource() {
    DriverManagerDataSource dataSource = new DriverManagerDataSource();
    dataSource.setDriverClassName("org.hsqldb.jdbcDriver");
    dataSource.setUrl("jdbc:hsqldb:hsql://localhost:");
    dataSource.setUsername("sa");
    dataSource.setPassword("");
    return dataSource;
}
```

**Listing 1.** Framework sample — **not a pool**. Pooling: [[What is connection pooling in Spring JDBC]]. Boot Hikari: [[What is HikariCP in Spring Boot]]. JNDI: [[How do you use a Tomcat JNDI DataSource in Spring]].

Then construct **`JdbcTemplate`** from that bean — [[How do you configure JdbcTemplate as a bean]].

```d2
direction: right
cfg: "@Bean DataSource" {
  width: 180
  height: 45
  style.fill: "#e3f2fd"
}
jt: "JdbcTemplate" {
  width: 160
  height: 45
  style.fill: "#fff3e0"
}

cfg -> jt
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. `DataSourceBuilder` in Boot how-to is a **Boot** helper, not required in plain Framework.

> [!warning] `DriverManagerDataSource` is documented as test-only
> No pooling; concurrent checkout is expensive. Do not copy it into production as “the Spring DataSource”.

> [!warning] Two DataSource beans
> Multiple databases need **multiple templates**. Boot: a custom `@Bean DataSource` **suppresses** auto-config.

> [!tip] Interview answer
> **Define a `DataSource` bean with URL and credentials, preferably a pool (Hikari).** Tests may use `DriverManagerDataSource`. Boot fills this from `spring.datasource.*` unless you declare the bean yourself.

## See also

- [[What is connection pooling in Spring JDBC]]
- [[What is HikariCP in Spring Boot]]
- [[How do you configure JdbcTemplate as a bean]]
