<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# How do you configure `JdbcTemplate` as a bean?

> [!abstract] Short answer
> Construct **`new JdbcTemplate(dataSource)`** once and **inject that instance**. It is **thread-safe** after configuration — do **not** `new JdbcTemplate` per SQL call. Framework DAO examples take a **`DataSource`** in a constructor or init method. Boot with **`spring-jdbc`** **auto-configures** `JdbcTemplate` and **`NamedParameterJdbcTemplate`** (named reuses the same template).

## One template per DataSource

Docs: *seldom necessary to create a new instance each time*. Multiple databases → **multiple `DataSource`s and templates**. Optional: extend **`JdbcDaoSupport`** (deprecated in **7.0**) and call **`setDataSource`**.

```java
@Configuration
public class JdbcConfig {

    @Bean
    JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}

@Repository
public class JdbcCorporateEventDao implements CorporateEventDao {

    private final JdbcTemplate jdbcTemplate;

    public JdbcCorporateEventDao(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }
}
```

**Listing 1.** Conceptual — explicit `@Bean` + constructor injection. DataSource: [[How do you configure a DataSource in Spring]]. Thread-safety: [[Is JdbcTemplate thread-safe]]. Boot also autowires `JdbcTemplate` with no `@Bean` of your own.

If several `JdbcTemplate` beans exist and none is **`@Primary`**, Boot **does not** auto-configure **`NamedParameterJdbcTemplate`**. Custom **`SQLExceptionTranslator` `@Bean`** is picked up by the auto-configured template.

```d2
direction: down
ds: "DataSource" {
  width: 160
  height: 40
  style.fill: "#e8f5e9"
}
jt: "JdbcTemplate bean" {
  width: 180
  height: 45
  style.fill: "#fff3e0"
}
dao: "@Repository" {
  width: 150
  height: 40
  style.fill: "#e3f2fd"
}

ds -> jt -> dao
```

**Fig. 1.** Fluent alternative: [[What is JdbcClient]] (Boot auto-config from named template). Superclass: [[What is JdbcDaoSupport]].

> [!warning] Spring Data JPA does not need this bean
> JPA repositories use **`EntityManager`**. JDBC and JPA can coexist; they do not share a `JdbcTemplate`.

> [!warning] Per-method `new JdbcTemplate(ds)`
> Works but wastes configuration (fetch size, translator). Share one bean.

> [!tip] Interview answer
> **`JdbcTemplate` is a singleton bean built from a `DataSource`.** Inject it into `@Repository`. Boot creates it if `spring-jdbc` is on the classpath. Do not allocate a new template for every query.

## See also

- [[What is Spring JdbcTemplate]]
- [[How do you configure a DataSource in Spring]]
- [[Is JdbcTemplate thread-safe]]
