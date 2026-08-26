<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/JDBC #Java/Annotations #SRS

# What is the JdbcTest annotation?

> [!abstract] Short answer
> **`@JdbcTest`** (module **`spring-boot-jdbc-test`**, package **`org.springframework.boot.jdbc.test.autoconfigure`**) is Boot’s **JDBC slice for tests that need a `DataSource` and `JdbcTemplate` and do not use Spring Data JDBC**. Default: **embedded in-memory database** (replaces the app `DataSource`) and **`@Transactional` rollback** after each method. Regular **`@Component` / `@ConfigurationProperties` are not scanned**. Spring Data JDBC repositories: **`@DataJdbcTest`**. JPA: **`@DataJpaTest`**. Full app + embedded DB: **`@SpringBootTest` + `@AutoConfigureTestDatabase`**.

## DataSource + `JdbcTemplate`, no Spring Data

`@EnableConfigurationProperties` if you need properties beans. Real DB: **`@AutoConfigureTestDatabase(replace = Replace.NONE)`** (same idea as the JPA slice; Boot **4** also has **`Replace.NON_TEST`** for Testcontainers URLs). Disable rollback with **`@Transactional(propagation = NOT_SUPPORTED)`**. Two **`@…Test`** annotations on one class are **unsupported**. Family: [[What are Spring Boot test slices]]. JPA sibling: [[What is the DataJpaTest annotation]]. Rollback: [[What is Transactional used for in tests]]. SQL scripts: [[What is the Sql annotation in Spring tests]]. Full context: [[What is SpringBootTest]].

```java
@JdbcTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)
class MyNonTransactionalJdbcTests { }
```

**Listing 1.** Conceptual Boot **4.1**. Class-level **NOT_SUPPORTED** turns rollback off.

```java
@JdbcTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
class MyJdbcAgainstAppDatasourceTests {

    @Autowired JdbcTemplate jdbcTemplate;
}
```

**Listing 2.** Conceptual: keep the application `DataSource`. Still **no** MVC, **no** Spring Data JDBC repos.

```d2
direction: down
jdbc: "@JdbcTest\nDataSource + JdbcTemplate" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
data: "@DataJdbcTest\nSpring Data JDBC repos" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
jpa: "@DataJpaTest\nEntityManager + JPA repos" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Three slices. Pick from the access API, not from “it talks to a database.”

> [!warning] Not `@DataJdbcTest`
> **`@JdbcTest`** skips Spring Data JDBC. If you `@Autowired` a `CrudRepository` from **spring-data-jdbc**, this slice **does not** load it.

> [!warning] Not `@DataJpaTest`
> No **`EntityManager`**, no **`TestEntityManager`**, no **`@Entity` scan**. Hibernate mappings will not run here.

> [!warning] Embedded H2 is not production SQL
> Vendor dialects still need **`Replace.NONE`** (or a Testcontainers URL **`NON_TEST` will keep**). The slice still does **not** start the web stack.

> [!tip] Interview answer
> **`@JdbcTest` is the JDBC slice: embedded DB, `JdbcTemplate`, transactional rollback — no Spring Data JDBC.** Repositories of that kind are `@DataJdbcTest`. JPA is `@DataJpaTest`.
