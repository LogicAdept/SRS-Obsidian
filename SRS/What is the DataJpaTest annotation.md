<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Data/JPA #Java/Annotations #SRS

# What is the DataJpaTest annotation?

> [!abstract] Short answer
> **`@DataJpaTest`** is Boot’s **JPA slice** (module **`spring-boot-data-jpa-test`**, package **`org.springframework.boot.data.jpa.test.autoconfigure`**). It scans **`@Entity`** and Spring Data JPA repositories, enables **JPA-relevant auto-config only**, and — if an **embedded database** is on the classpath — **configures that as the `DataSource`**. Tests are **`@Transactional` and roll back** after each method. Inject the repository and **`TestEntityManager`**. Regular **`@Component` / MVC are not loaded**. Prefer this over **`@SpringBootTest`** for repository tests.

## Entities, repos, in-memory DB, rollback

**`showSql` defaults to `true`** (`spring.jpa.show-sql`; disable with **`showSql = false`**). **`JdbcTemplate`** is also there. **`TestEntityManager`** is a test-oriented persist/flush/find helper (`org.springframework.boot.jpa.test.autoconfigure`). Outside the slice, add **`@AutoConfigureTestEntityManager`** and keep a **transaction**.

Real database: **`@AutoConfigureTestDatabase(replace = Replace.NONE)`** — do **not** swap the application `DataSource`. Boot **4** also has **`Replace.NON_TEST`**: still replace a normal app DataSource, but **keep** Testcontainers / `@ServiceConnection` / TC JDBC / `@DynamicPropertySource` URLs. Disable rollback with **`@Transactional(propagation = NOT_SUPPORTED)`** on the class. **`@ConfigurationProperties`** need **`@EnableConfigurationProperties`**. Full app **plus** an embedded DB is **`@SpringBootTest` + `@AutoConfigureTestDatabase`**, not this slice. Helper: [[What is TestEntityManager]]. Family: [[What are Spring Boot test slices]]. Full app: [[What is SpringBootTest]]. Rollback: [[What is Transactional used for in tests]]. Seed SQL: [[How do you handle test data in Spring integration tests]].

```java
@DataJpaTest
class MyRepositoryTests {

    @Autowired TestEntityManager entityManager;
    @Autowired UserRepository repository;

    @Test
    void testExample() {
        this.entityManager.persist(new User("sboot", "1234"));
        User user = this.repository.findByUsername("sboot");
        assertThat(user.getUsername()).isEqualTo("sboot");
    }
}
```

**Listing 1.** Conceptual Boot **4.1**. Persist via **`TestEntityManager`**, query via the **repository**. Method rolls back.

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
class MyRepositoryAgainstAppDatasourceTests { }
```

**Listing 2.** Conceptual: keep the application `DataSource` (Postgres, Testcontainers URL you already wired, …). **Still no MVC.**

```d2
direction: down
ann: "@DataJpaTest" {
  width: 200
  height: 35
  style.fill: "#e3f2fd"
}
keep: "@Entity + Spring Data repos\nembedded DataSource" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
tx: "@Transactional rollback" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
drop: "@Service / @Controller / MVC" {
  width: 260
  height: 40
  style.fill: "#ffebee"
}

ann -> keep -> tx
ann -> drop
```

**Fig. 1.** A slice is still an **`ApplicationContext`**. H2 dialect is **not** production PostgreSQL.

> [!warning] Explicit `@ComponentScan` on the application class
> It can **disable slice exclude filters**, so `@DataJpaTest` loads **the whole app**. Keep Boot’s default scan.

> [!warning] Embedded H2 is not the production engine
> Vendor SQL / JSONB can pass here and fail on Postgres. **`Replace.NONE`** (or a Testcontainers URL that **`NON_TEST`** will not overwrite) is the follow-up — still **without** `@SpringBootTest`.

> [!warning] Unflushed persists
> A query may miss a `persist` until **`persistAndFlush` / `flush`**. **`TestEntityManager` is not production `EntityManager`.**

> [!tip] Interview answer
> **`@DataJpaTest` is the JPA slice: entities, repositories, in-memory DB, transactional rollback, `TestEntityManager`.** No web layer. Use **`@AutoConfigureTestDatabase(replace = NONE)`** for a real DataSource. Do not boot `@SpringBootTest` just to test a repository.
