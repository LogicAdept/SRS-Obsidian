<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Integration #Java/Annotations #Java/Spring/Transactions #SRS

# What is the Sql annotation in Spring tests?

> [!abstract] Short answer
> **`@Sql`** (`org.springframework.test.context.jdbc`, since **4.1**) declares **SQL scripts and/or inlined `statements`** to run against a **`DataSource` in the test `ApplicationContext`**. **`SqlScriptsTestExecutionListener`** (on by default) executes them. Default **`executionPhase` is `BEFORE_TEST_METHOD`** (before JUnit **`@BeforeEach`**). Class or method. Repeatable; **`@SqlGroup`** if you need an explicit container. Needs **`spring-jdbc`** and **`spring-tx`**.

## Scripts join the test transaction unless you isolate them

Inferred mode: **no TX**, **same Spring-managed test TX**, or **`@SqlConfig(transactionMode = ISOLATED)`** (new TX that **commits**). With **`@Transactional`** on the test, default seed **rolls back** — no delete script. **`AFTER_TEST_METHOD`** is for cleanup when you **did** commit (`ISOLATED`). Framework **6.1+**: class-level **`BEFORE_TEST_CLASS` / `AFTER_TEST_CLASS`** (cannot be overridden; **`BEFORE_TEST_CLASS` loads the context early** — **`@DynamicPropertySource` runs before `@BeforeAll`**).

Paths are **`Resource`s**: `"schema.sql"` package-relative; `"/org/example/schema.sql"` absolute classpath; `classpath:` / `file:`. Empty `@Sql` looks for **`MyTest.sql`** / **`MyTest.testMethod.sql`**. Method-level **overrides** class-level unless **`@SqlMergeMode(MERGE)`**. **`statements` run after `scripts`**. How-to: [[How do you handle test data in Spring integration tests]]. Rollback: [[What is Transactional used for in tests]]. JPA slice: [[What is the DataJpaTest annotation]]. JDBC slice: [[What is the JdbcTest annotation]]. Context: [[What is the Spring TestContext Framework]].

```java
@Transactional
class TransactionalSqlScriptsTests {

    @Test
    @Sql("/test-data.sql")
    void usersTest() {
        // seed shares the test TX; listener rollback undoes it
    }
}
```

**Listing 1.** Conceptual Framework **7**. No after-method delete.

```java
@Test
@Sql(scripts = "create-test-data.sql", config = @SqlConfig(transactionMode = ISOLATED))
@Sql(scripts = "delete-test-data.sql", config = @SqlConfig(transactionMode = ISOLATED),
        executionPhase = AFTER_TEST_METHOD)
void userTest() { }
```

**Listing 2.** Conceptual: committed rows for another thread / HTTP server, then isolated cleanup.

```d2
direction: down
ann: "@Sql scripts / statements" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
lis: "SqlScriptsTestExecutionListener" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
ds: "test DataSource" {
  width: 200
  height: 35
  style.fill: "#e8f5e9"
}

ann -> lis -> ds
```

**Fig. 1.** Production `DataSource` is never implied. The bean in **this** context is.

> [!warning] Method `@Sql` replaces class `@Sql`
> Default is **OVERRIDE**. Schema-on-class + data-on-method needs **`@SqlMergeMode(MERGE)`**. Class **`BEFORE_TEST_CLASS`** still always runs.

> [!warning] `ISOLATED` commits
> Those rows **survive** the test TX. Pair with **`AFTER_TEST_METHOD`** cleanup or you leak into the next method that shares the DB.

> [!warning] Empty `@Sql` is not a no-op
> Missing default file → **`IllegalStateException`**. Put **`scripts`** or **`statements`** explicitly in interview code.

> [!tip] Interview answer
> **`@Sql` runs scripts against the test `DataSource` via `SqlScriptsTestExecutionListener`.** Default is before the method, inside the test transaction so rollback cleans up. Use `ISOLATED` only when another thread must see committed rows.
