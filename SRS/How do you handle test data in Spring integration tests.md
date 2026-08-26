<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Integration #Java/Annotations #Java/Spring/Transactions #SRS

# How do you handle test data in Spring integration tests?

> [!abstract] Short answer
> Prefer a **test-managed transaction that rolls back**: class- or method-level **`@Transactional`** (Boot **`@DataJpaTest`** already does). Seed with **`@Sql`** (default **`BEFORE_TEST_METHOD`**) so inserts share that transaction and **disappear on rollback** — no delete script. Persist JPA fixtures with **`TestEntityManager`** (`persist` / `persistAndFlush`). Use **`@Sql(executionPhase = AFTER_TEST_METHOD)`** plus **`@SqlConfig(transactionMode = ISOLATED)`** only when data must be **committed** outside the test TX. Needs a **`DataSource`** in the test context. Framework **6.1+**: class-level **`BEFORE_TEST_CLASS` / `AFTER_TEST_CLASS`**.

## Rollback first; scripts join that transaction

`SqlScriptsTestExecutionListener` (**order 5000**, after **`TransactionalTestExecutionListener`**) runs `@Sql`. Default **`executionPhase`** is **`BEFORE_TEST_METHOD`**. With `@Transactional` on the test, inferred mode runs scripts **inside the same Spring-managed transaction**. Official transactional `@Sql` sample: **do not clean up after the method** — listener rollback undoes both the script and the test’s writes.

`@SqlConfig.TransactionMode.ISOLATED`: scripts run in a **new transaction that commits immediately**. The Framework example pairs **ISOLATED** seed **and** **ISOLATED** `AFTER_TEST_METHOD` delete when the test must see **committed** rows (for example another thread / HTTP server).

`@Sql` paths are Spring **`Resource`s**: `"schema.sql"` is package-relative classpath; `"/org/example/schema.sql"` is absolute classpath; `classpath:` / `file:` prefixes work. Empty `@Sql` looks for **`com/example/MyTest.sql`** (class) or **`MyTest.testMethod.sql`** (method). Method-level `@Sql` **overrides** class-level unless **`@SqlMergeMode(MERGE)`**. Class-level **`BEFORE_TEST_CLASS` / `AFTER_TEST_CLASS`** cannot be overridden.

Programmatic alternative: **`ResourceDatabasePopulator.execute(DataSource)`**. Boot **`@DataJpaTest`**: embedded DB, transactional rollback, inject **`TestEntityManager`**. Must run in a transaction (`@Transactional` if you use `@AutoConfigureTestEntityManager` outside the slice).

```java
@Transactional
class UserDataTests {

    @Test
    @Sql("/test-data.sql")
    void usersAreSeeded() {
        // rows from the script; rolled back after the method
    }

    @Test
    @Sql(scripts = "create-test-data.sql",
            config = @SqlConfig(transactionMode = SqlConfig.TransactionMode.ISOLATED))
    @Sql(scripts = "delete-test-data.sql",
            config = @SqlConfig(transactionMode = SqlConfig.TransactionMode.ISOLATED),
            executionPhase = Sql.ExecutionPhase.AFTER_TEST_METHOD)
    void needsCommittedRows() {
        // another transaction / thread can see the seed
    }
}
```

**Listing 1.** Conceptual Framework 7 shapes. First method: join test TX. Second: official **ISOLATED** seed + cleanup. `@Sql`: [[What is the Sql annotation in Spring tests]]. Rollback: [[What is Transactional used for in tests]]. JPA helpers: [[What is TestEntityManager]], [[What is the DataJpaTest annotation]].

```d2
direction: down
tx: "TransactionalTestExecutionListener\nbegin test TX" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
sql: "@Sql BEFORE_TEST_METHOD\nin same TX (inferred)" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
test: "Test method" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
rb: "Default rollback\nscript + writes gone" {
  width: 280
  height: 50
  style.fill: "#c8e6c9"
}

tx -> sql -> test -> rb
```

**Fig. 1.** Default path: seed in the test transaction, then **roll it back**. `AFTER_TEST_METHOD` delete is redundant unless you **committed** with **ISOLATED** (or `@Commit`).

> [!warning] `AFTER_TEST_METHOD` cleanup is rolled back with the test TX
> Dump “setup BEFORE + cleanup AFTER + `@Transactional`” undoes the **delete** too if scripts join the test transaction. For committed data use **`transactionMode = ISOLATED`** on both scripts, as in the Framework example. Otherwise skip AFTER cleanup and rely on rollback.

> [!warning] `@Transactional` does not roll back another thread’s SQL
> **`RANDOM_PORT` / `DEFINED_PORT`**: the HTTP server uses a **different** transaction. Test-thread rollback does **not** undo servlet work. Same for **`REQUIRES_NEW`**. Isolation: [[What is the difference between DirtiesContext and Transactional in tests]].

> [!warning] `@Sql` is not production Flyway
> Scripts hit the **test** `DataSource`. A missing `DataSource` bean fails the listener. Default script detection throws **`IllegalStateException`** if no file matches.

> [!tip] Interview answer
> **Put the test in `@Transactional` and seed with `@Sql` before the method; rollback wipes the data.** `@DataJpaTest` plus `TestEntityManager.persist` is the JPA slice of that. Use **`ISOLATED` `@Sql` and `AFTER_TEST_METHOD`** only when rows must be committed outside the test transaction.
