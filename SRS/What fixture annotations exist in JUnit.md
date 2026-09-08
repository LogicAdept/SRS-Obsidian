<!--
reps: 0
priority: 0
-->
#Java/Testing/JUnit #Java/Annotations #SRS

# What fixture annotations exist in JUnit?

> [!abstract] Short answer
> In **JUnit Jupiter** the fixture (lifecycle) annotations are **`@BeforeEach`**, **`@AfterEach`**, **`@BeforeAll`**, and **`@AfterAll`**. They run setup/teardown around tests. JUnit 4’s names were **`@Before`**, **`@After`**, **`@BeforeClass`**, **`@AfterClass`**. `@BeforeAll` / `@AfterAll` must be **`static`** unless the class uses **`@TestInstance(PER_CLASS)`**.

## Four hooks, two timescales

A **fixture** here is code that prepares or cleans the test’s world — not `@Test` itself. Jupiter methods annotated with:

- **`@BeforeEach`** — before **every** `@Test` / `@RepeatedTest` / `@ParameterizedTest` / `@TestFactory` in the class (JUnit 4 `@Before`)
- **`@AfterEach`** — after each of those (JUnit 4 `@After`)
- **`@BeforeAll`** — **once** before all of them (JUnit 4 `@BeforeClass`)
- **`@AfterAll`** — **once** after all of them (JUnit 4 `@AfterClass`)

They are **inherited** unless overridden. Superclass `@BeforeEach` runs **before** subclass; superclass `@AfterEach` runs **after** subclass.

Default instance lifecycle is **per-method**: a **new** test-class instance per test, so instance fields do not carry state between tests. `@BeforeAll` / `@AfterAll` therefore attach to the **class** (`static`) unless you opt into `@TestInstance(Lifecycle.PER_CLASS)` — required for non-static class-level hooks and for `@Nested` inner classes that cannot hold statics (before Java 16). The fixture concept itself: [[What is a test fixture in JUnit]].

```java
class LedgerTest {
    static EmbeddedDb db;

    @BeforeAll
    static void startDb() { db = EmbeddedDb.start(); }

    @BeforeEach
    void seed() { db.clean().insert("ledger.sql"); }

    @Test
    void postsDebit() { /* ... */ }

    @AfterEach
    void noOpenTx() { db.rollback(); }

    @AfterAll
    static void stopDb() { db.close(); }
}
```

**Listing 1.** Class-scoped resource in `*All`; per-test reset in `*Each`.

```d2
direction: down
all0: "@BeforeAll" {
  width: 140
  height: 40
}
each0: "@BeforeEach" {
  width: 140
  height: 40
}
t: "@Test" {
  width: 140
  height: 40
}
each1: "@AfterEach" {
  width: 140
  height: 40
}
all1: "@AfterAll" {
  width: 140
  height: 40
}
all0 -> each0 -> t -> each1
each1 -> each0: "next test"
each1 -> all1: "class done"
```

**Fig. 1.** `*Each` wraps every test; `*All` wraps the class.

> [!warning] Wrong package, or non-static `@BeforeAll`
> `org.junit.Before` on a Jupiter class is **not** `@BeforeEach` — Vintage vs Jupiter. A non-static `@BeforeAll` **fails** under the default per-method lifecycle. `@Nested` classes need `PER_CLASS` or (Java 16+) `static` `*All` methods.

> [!tip] Interview answer
> JUnit Jupiter fixture annotations are BeforeEach, AfterEach, BeforeAll, and AfterAll. The first pair runs around every test; the second pair once per class and must be static unless you switch to PER_CLASS. JUnit 4 used Before, After, BeforeClass, and AfterClass for the same jobs.
