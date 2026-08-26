<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Data/JPA #Java/Annotations #SRS

# How do you test JPA repositories in Spring?

> [!abstract] Short answer
> Use Boot’s **`@DataJpaTest`** (module **`spring-boot-data-jpa-test`**, package **`org.springframework.boot.data.jpa.test.autoconfigure`**). It scans **`@Entity`** and Spring Data JPA repositories, **replaces the `DataSource` with an embedded in-memory database** when one is on the classpath, and is **`@Transactional` with rollback after each test**. Inject the repository and **`TestEntityManager`** (`persist` / `persistAndFlush`, then `findBy…` on the repo). **Regular `@Component` / MVC are not loaded.** For a real DB: **`@AutoConfigureTestDatabase(replace = Replace.NONE)`**. Full app + embedded DB: **`@SpringBootTest` + `@AutoConfigureTestDatabase`**, not this slice.

## Slice: entities, repos, embedded DB

`@DataJpaTest` enables only JPA-relevant auto-config. **`showSql` defaults to `true`** (`spring.jpa.show-sql`). **`JdbcTemplate`** is available. **`TestEntityManager`** is a test-oriented subset of `EntityManager` (persist/flush/find). Outside the slice, add **`@AutoConfigureTestEntityManager`** and keep the test **`@Transactional`**.

That is the interview path. `@SpringBootTest` against production Postgres is a **full context** (web, security, everything) — slower, not the slice. Keep the slice and point at a real DB with **`Replace.NONE`** (or Testcontainers / `NON_TEST` replacement rules). Isolation: [[What is the DataJpaTest annotation]]. Helper: [[What is TestEntityManager]]. Rollback: [[What is Transactional used for in tests]]. Seed SQL: [[How do you handle test data in Spring integration tests]].

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
        assertThat(user.getEmployeeNumber()).isEqualTo("1234");
    }
}
```

**Listing 1.** Conceptual Boot **4.1** sample. Persist through **`TestEntityManager`**, query through the **repository under test**. Changes roll back.

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
class MyRepositoryAgainstAppDatasourceTests { }
```

**Listing 2.** Conceptual: do **not** swap in H2; use the application `DataSource`.

```d2
direction: down
slice: "@DataJpaTest\n@Entity + repositories" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
db: "Embedded DataSource\n(unless Replace.NONE)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
tx: "@Transactional\nrollback after method" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

slice -> db -> tx
```

**Fig. 1.** No `DispatcherServlet`, no `@Service`. If an explicit `@ComponentScan` on the application class **disables slice exclude filters**, `@DataJpaTest` can suddenly load the whole app.

> [!warning] `@SpringBootTest` is not the repository slice
> It loads **auto-config for the whole app**. Use it when you **need** that. For “does this Spring Data query work?”, **`@DataJpaTest`**.

> [!warning] `TestEntityManager` is not a production `EntityManager`
> Use it in tests. Outside `@DataJpaTest` it still needs a **transaction**. Unflushed persists may be invisible to a query until **`persistAndFlush`** / **`flush`**.

> [!warning] Embedded H2 is not production SQL
> Vendor-specific PostgreSQL / JSONB queries can pass on H2 and fail on the real engine. **`Replace.NONE`** (or a Testcontainers URL) is the follow-up, still without MVC.

> [!tip] Interview answer
> **`@DataJpaTest`, autowire the repository and `TestEntityManager`, persist a fixture, assert the query, rely on rollback.** In-memory DB by default; `@AutoConfigureTestDatabase(replace = NONE)` to keep the app DataSource. Do not pull in `@SpringBootTest` just to test a repository.
