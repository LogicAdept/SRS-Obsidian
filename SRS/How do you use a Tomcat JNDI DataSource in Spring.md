<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# How do you use a Tomcat JNDI `DataSource` in Spring?

> [!abstract] Short answer
> Tomcat binds a pool as a **JNDI resource** (typical name **`jdbc/…`**, lookup **`java:comp/env/jdbc/…`**). Spring **looks that object up** and injects it as **`javax.sql.DataSource`**. Framework: **`JndiObjectFactoryBean`** (`jndiName`, often **`expectedType = DataSource.class`**). Boot WAR on an app server: **`spring.datasource.jndi-name=…`** instead of URL/user/password.

## Container pool, Spring lookup

Framework JDBC: you **may obtain a DataSource from JNDI** rather than constructing a pool bean. **`JndiObjectFactoryBean`**: singleton factory for a JNDI object (explicitly **DataSource** for DAOs). Default: **lookup on startup** and **cache**. Switching to **`DriverManagerDataSource`** for tests is a **config swap**, not a code change.

Tomcat: `<Resource name="jdbc/TestDB" type="javax.sql.DataSource" …/>` in context — applications look up **`java:comp/env/jdbc/TestDB`**.

```java
@Bean
JndiObjectFactoryBean dataSource() {
    JndiObjectFactoryBean bean = new JndiObjectFactoryBean();
    bean.setJndiName("java:comp/env/jdbc/TestDB");
    bean.setExpectedType(DataSource.class);
    return bean;
}
```

**Listing 1.** Conceptual Framework lookup — return type of the `@Bean` method is often **`DataSource`** via `getObject()` / factory. Boot: `spring.datasource.jndi-name=java:comp/env/jdbc/TestDB` (Boot’s own example uses a JBoss name). Pooling idea: [[What is connection pooling in Spring JDBC]]. Local bean: [[How do you configure a DataSource in Spring]].

```d2
direction: down
tomcat: "Resource jdbc/TestDB" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
jndi: "java:comp/env/jdbc/TestDB" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
spring: "JndiObjectFactoryBean /\nspring.datasource.jndi-name" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}

tomcat -> jndi -> spring
```

**Fig. 1.** Then inject into [[How do you configure JdbcTemplate as a bean]]. Embedded Boot JAR usually **does not** use Tomcat JNDI — local Hikari: [[What is HikariCP in Spring Boot]].

> [!warning] Lookup name vs Resource `name`
> Resource **`jdbc/TestDB`** is not the full JNDI string. The Java EE env prefix is **`java:comp/env/`**.

> [!warning] Lazy lookup needs a proxy interface
> If **`lookupOnStartup=false`** or **`cache=false`**, javadoc requires **`proxyInterface`** because the JNDI type is not known yet.

> [!tip] Interview answer
> **Tomcat publishes a DataSource in JNDI; Spring looks it up.** `JndiObjectFactoryBean` or Boot `spring.datasource.jndi-name`. Typical name: `java:comp/env/jdbc/…`. Local Hikari is the Boot-embedded default.

## See also

- [[How do you configure a DataSource in Spring]]
- [[What is connection pooling in Spring JDBC]]
- [[What is HikariCP in Spring Boot]]
