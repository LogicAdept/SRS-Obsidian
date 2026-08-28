<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Transactions #Java/Annotations #SRS

# What is the difference between `@Commit` and `@Rollback` in Spring tests?

> [!abstract] Short answer
> After a **test-managed** `@Transactional` method, TestContext **rolls back by default**. **`@Rollback`** (2.5+) makes that explicit (`value` defaults **`true`**). **`@Commit`** (4.2+) is the readable form of **`@Rollback(false)`**: persist the test’s database work. They set the **same flag** (commit vs roll back when the test transaction **ends**). Do **not** put both on one class or method.

## Default is rollback, not production `rollbackFor`

`TransactionalTestExecutionListener` (on by default) starts a transaction when the test class or method has Spring’s **`@Transactional`** and a **`PlatformTransactionManager`** is in the test context. When the method finishes, the listener **rolls back** unless you opt into commit. That default is **independent** of production `rollbackFor` / `noRollbackFor` — those attributes are **not supported** for test-managed transactions (use `TestTransaction.flagForRollback()` / `flagForCommit()` instead). See [[What is Transactional used for in tests]] and [[What is Spring default rollback policy for Transactional]].

| | `@Rollback` | `@Commit` |
| --- | --- | --- |
| **Meaning** | Roll back (`true`) or commit (`false`) | Always commit |
| **Default `value`** | `true` | (no attribute) |
| **Alias** | `@Rollback(false)` ≡ `@Commit` | Replacement for `@Rollback(false)` |
| **Scope** | Class (default for the hierarchy) or method (overrides) | Same |

```java
@SpringJUnitConfig
@Transactional(transactionManager = "txMgr")
@Commit
class FictitiousTransactionalTest {

	@Test
	@Rollback
	void modifyDatabaseWithinTransaction() {
		// class-level @Commit overridden: this method rolls back
	}
}
```

**Listing 1.** Conceptual Spring 6.2 demo: method-level `@Rollback` wins over class-level `@Commit`. Engine: [[What is the Spring TestContext Framework]]. Isolation vs context rebuild: [[What is the difference between DirtiesContext and Transactional in tests]].

`@BeforeEach` / `@AfterEach` run **inside** the test transaction (so rollback undoes their SQL too). **`@BeforeTransaction` / `@AfterTransaction`** run **outside** — use `@AfterTransaction` to assert committed rows after a `@Commit` test. Programmatic: `TestTransaction.flagForCommit()` then `end()` (flagging does not end the TX by itself).

```d2
direction: down
tx: "@Transactional test method" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
flag: "@Rollback true (default)\nor @Commit / @Rollback(false)" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
end: "transaction ends" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
rb: "DB unchanged" {
  width: 180
  height: 40
  style.fill: "#c8e6c9"
}
cm: "DB keeps writes" {
  width: 180
  height: 40
  style.fill: "#ffcdd2"
}

tx -> flag
flag -> end
end -> rb: "rollback"
end -> cm: "commit"
```

**Fig. 1.** `@Commit` / `@Rollback` only decide the **end** of an **existing** test-managed transaction. No `@Transactional` (or `propagation = NEVER` / `NOT_SUPPORTED`) means neither annotation has a test TX to finish.

> [!warning]Do not declare both on the same element
> `@Commit` plus `@Rollback` on one test class or method is **unsupported** and may behave unpredictably. Pick one. Method-level annotations override class-level defaults; nested classes inherit unless `@NestedTestConfiguration` overrides.

> [!warning]Timeouts and ORM flush still bypass the story
> A **preemptive** timeout (JUnit 4 `@Test(timeout)`, Jupiter `assertTimeoutPreemptively`, TestNG `timeOut`) runs the test body on **another thread**. Work there is **not** bound to the test TX and can **commit** even when the listener later rolls back. Hibernate/JPA tests that never **`flush()`** can pass while production would fail — rollback does not hide that if you never hit the database.

> [!tip] Interview answer
> **Test `@Transactional` rolls back by default so the database stays clean.** `@Rollback` documents that (`true`) or turns it off (`false`). `@Commit` is the explicit name for commit and equals `@Rollback(false)`. Use commit only when a test must leave data behind; never put both annotations on the same class or method. Production `rollbackFor` rules do not apply to this listener.
