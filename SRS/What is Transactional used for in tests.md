<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #Java/Spring/Transactions #SRS

# What is `Transactional` used for in tests?

> [!abstract] Short answer
> On a Spring integration test, **`@Transactional` wraps the test method in a test-managed transaction that rolls back by default**, so database changes do not leak between tests. It is **data isolation**, not context rebuild — that is **`@DirtiesContext`**. Slice tests such as **`@DataJpaTest`** include `@Transactional` and roll back at the end of each test by default.

## Test-managed transaction rollback

Spring’s TestContext framework runs `@Transactional` test methods through **`TransactionalTestExecutionListener`**. With a `PlatformTransactionManager` in the test `ApplicationContext`, each annotated test (or each method when the class is annotated) runs inside a transaction that **rolls back after completion** unless you opt into commit with **`@Commit`** or **`@Rollback(false)`**.

That lets tests insert/update through repositories or `JdbcTemplate` and leave the database clean without manual delete scripts — as long as the work ran in the **test thread’s** transaction.

```d2
direction: down
start: "Test method starts\ntest-managed TX" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
work: "Repository / JDBC work\nin same thread" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
end: "Default: rollback\ncontext stays cached" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

start -> work -> end
```

**Fig. 1.** Test `@Transactional` isolates **rows**, not the Spring container.

```java
@DataJpaTest
class OrderRepositoryTests {

    @Autowired OrderRepository orders;

    @Test
    void savesOrder() {
        orders.save(new Order("A-1"));
        assertThat(orders.count()).isEqualTo(1);
        // rolled back after the method — next test sees a clean DB
    }
}
```

**Listing 1.** Conceptual: `@DataJpaTest` is meta-annotated with `@Transactional` and rolls back by default (Boot docs).

Disable transaction management for a test or class with `@Transactional(propagation = Propagation.NOT_SUPPORTED)` when you need real commits or no test TX.

## Not `@DirtiesContext`

| | `@Transactional` (test) | `@DirtiesContext` |
| --- | --- | --- |
| Cleans | **Database** (rollback) | **`ApplicationContext`** |
| Context cache | Kept | Evicted / rebuilt |
| Cost | Low | High |

See [[What is the difference between DirtiesContext and Transactional in tests]].

## Commit visibility and HTTP traps

Default rollback means the test never proves that production code **commits** successfully. Use `@Commit` / programmatic `TestTransaction` when you must assert durable state, then clean up explicitly.

Spring Boot warns: with `@SpringBootTest` and **`RANDOM_PORT` / `DEFINED_PORT`**, the HTTP client and server run on **separate threads** and thus **separate transactions**. Server-side work initiated by `TestRestTemplate` / `WebTestClient` against a real port **does not** roll back with the test method’s transaction.

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Transactional // does NOT roll back server-thread commits via TestRestTemplate
class OrderApiTests {

    @Autowired TestRestTemplate rest;

    @Test
    void placesOrder() {
        rest.postForEntity("/orders", new Order("A-1"), Void.class);
        // DB cleanup must be explicit — not the test TX
    }
}
```

**Listing 2.** Conceptual: real-server HTTP tests + `@Transactional` is a classic false sense of cleanup.

`REQUIRES_NEW` application transactions can also commit independently of the test TX — [[How do you test that REQUIRES_NEW commits independently of the outer transaction]].

> [!warning] Rollback hides real commit paths
> A green `@Transactional` repository test proves behavior inside an open unit of work, not that the service boundary commits in production. Pair with at least one non-rollback or end-to-end check when commit semantics matter.

> [!warning] Real HTTP ports break test-TX rollback
> Do not rely on class-level `@Transactional` to undo data created through `RANDOM_PORT` / `DEFINED_PORT` HTTP calls. Prefer `MockMvc` in the same thread, or explicit cleanup / `@Sql`.

> [!tip] Interview answer
> **`@Transactional` on a Spring test starts a test-managed transaction that rolls back by default so DB changes do not leak.** `@DataJpaTest` does this automatically. It is not `@DirtiesContext`. Watch for `RANDOM_PORT` HTTP clients: server work runs in another thread and will not roll back with the test transaction.
