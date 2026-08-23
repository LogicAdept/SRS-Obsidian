<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #Java/Spring/Transactions #SRS

# What is the difference between `DirtiesContext` and `Transactional` in tests?

> [!abstract] Short answer
> **`@Transactional` on a test rolls back database work** after the method (by default) while **keeping the cached `ApplicationContext`**. **`@DirtiesContext` marks the Spring context dirty**, removes it from the TestContext cache, **closes and rebuilds** it for later tests. Use transactional rollback for **data**; dirty the context only when **beans or context state** were mutated.

## Two different cleanup axes

Integration tests often need isolation, but persistence rollback and context lifecycle are separate concerns handled by different listeners:

| Annotation | What it cleans up | Context cache | Typical cost |
| --- | --- | --- | --- |
| **`@Transactional`** (test) | **Database** transaction (default rollback) | **Unchanged** — same cached context | Low |
| **`@DirtiesContext`** | **`ApplicationContext`** (close + rebuild) | **Evicted** for matching config | **High** |

Spring’s TestContext: `@Transactional` on a test method runs inside a transaction managed by **`TransactionalTestExecutionListener`**, rolled back by default after completion (override with `@Commit` / `@Rollback`).

`@DirtiesContext` means the **`ApplicationContext` was modified or corrupted** during the test — for example singleton bean state or embedded infrastructure — and **should be closed**. The framework removes it from the cache; the next test needing the same configuration metadata gets a **fresh container**.

```d2
direction: right
tx: "@Transactional test\nDB TX rollback" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
ctx: "Same ApplicationContext\ncache hit" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
dirty: "@DirtiesContext test\ncontext closed" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
rebuild: "Next test\nrebuilds context" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}

tx -> ctx
dirty -> rebuild
```

**Fig. 1.** Transactional tests isolate **rows**; `@DirtiesContext` isolates the **Spring container**.

```java
@SpringBootTest
@Transactional // class-level: each test method rolls back DB changes
class OrderRepositoryTests {

    @Autowired OrderRepository orders;

    @Test
    void savesOrder() {
        orders.save(new Order("A-1"));
        // rows rolled back after test; context stays cached
    }
}

@SpringBootTest
class CacheConfigTests {

    @Autowired MutableFeatureFlags flags;

    @Test
    @DirtiesContext // singleton flags bean mutated → rebuild context for later tests
    void togglesGlobalFlag() {
        flags.enable("beta");
    }
}
```

**Listing 1.** Conceptual split: repository data → transactional rollback; mutated singleton/config → `@DirtiesContext`.

## They can coexist but solve different problems

A test may carry **both** annotations when it changes **database rows** *and* **context-defining state**, but `@Transactional` does **not** replace `@DirtiesContext` for bean corruption, and `@DirtiesContext` does **not** roll back JDBC work unless that work ran inside the test-managed transaction.

For assertions after rollback, use **`@AfterTransaction`** on transactional tests — see [[How do you test that REQUIRES_NEW commits independently of the outer transaction]] for post-rollback verification patterns.

`@Transactional` on tests supports **limited** attribute subsets (propagation mainly `NOT_SUPPORTED` / `NEVER` to opt out); isolation/timeout/rollback rules differ from production `@Transactional` — see Spring’s test transaction management reference.

> [!warning] Overusing `@DirtiesContext` slows suites
> Rebuilding the `ApplicationContext` is expensive and defeats TestContext **caching**. Reserve it for tests that actually mutate context-level state — not for ordinary CRUD that transactional rollback already undoes.

> [!warning] `@Transactional` tests do not roll back `REQUIRES_NEW` commits
> Application code that commits in a separate physical transaction survives test rollback — transactional test demarcation is not a substitute for understanding propagation in the code under test.

> [!tip] Interview answer
> **`@Transactional` on a test rolls back the database and keeps the Spring context cached. `@DirtiesContext` closes and evicts the ApplicationContext because the test dirtied container state.** Use rollback (or `@Sql` cleanup) for data; dirty the context only when singleton beans or context configuration were changed.
