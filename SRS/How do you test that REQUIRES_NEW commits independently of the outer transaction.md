<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #Java/Spring/Framework/Testing #SRS

# How do you test that `REQUIRES_NEW` commits independently of the outer transaction?

> [!abstract] Short answer
> Exercise a **cross-bean** service where the outer method is `REQUIRED` and the inner method is `REQUIRES_NEW`, then **fail the outer** after the inner returns. Assert in **`@AfterTransaction`** (or after ending the test-managed transaction) that the inner row **remains committed** while the outer row **does not**.

## What you are proving

`Propagation.REQUIRES_NEW` opens a **separate physical transaction**: it suspends any existing transaction (including the test-managed one), commits or rolls back on its own, and releases its locks when the inner scope finishes. An outer rollback must **not** undo work the inner transaction already committed. That behavior is what [[How does REQUIRES_NEW transaction propagation work]] describes; the test checks it against a real `PlatformTransactionManager` and database.

## Integration-test shape

Spring’s TestContext can wrap each test in a transaction that **rolls back by default**. Application transactions with `REQUIRED` join that test transaction, but `REQUIRES_NEW` **does not** participate the same way — Spring’s testing docs warn that propagation types other than `REQUIRED` or `SUPPORTS` need extra care. The inner `REQUIRES_NEW` scope still commits when its method completes, even while the outer scope later rolls back.

```d2
direction: down
test: "Test @Transactional\n(test-managed TX)" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
outer: "Service outer()\nREQUIRED joins test TX" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
inner: "AuditService inner()\nREQUIRES_NEW suspends test TX\ncommits on return" {
  width: 320
  height: 100
  style.fill: "#e8f5e9"
}
fail: "Outer throws\nbusiness work rolls back" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
after: "@AfterTransaction\naudit row still visible\nbusiness row gone" {
  width: 300
  height: 90
  style.fill: "#fce4ec"
}

test -> outer
outer -> inner
inner -> fail
fail -> after
```

**Fig. 1.** After the test transaction rolls back, only the independently committed `REQUIRES_NEW` work should survive.

```java
@SpringBootTest
@Transactional // default: test TX rolls back after each method
class RerequiresNewIndependenceTests {

    @Autowired OrderService orders;
    @Autowired JdbcTemplate jdbc;

    @Test
    void innerCommitSurvivesOuterRollback() {
        assertThat(count("orders")).isZero();
        assertThat(count("audit_log")).isZero();

        assertThatThrownBy(() -> orders.placeOrderAndFail(new Order("A-1")))
            .isInstanceOf(IllegalStateException.class);

        // Still inside the test transaction — outer order insert is rolled back with it
        assertThat(count("orders")).isZero();
        // audit_log was committed by REQUIRES_NEW; visible even before @AfterTransaction
        assertThat(count("audit_log")).isEqualTo(1);
    }

    @AfterTransaction
    void verifyCommittedAuditAfterTestRollback() {
        assertThat(count("orders")).isZero();
        assertThat(count("audit_log")).isEqualTo(1);
    }

    private int count(String table) {
        return jdbc.queryForObject("select count(*) from " + table, Integer.class);
    }
}
```

**Listing 1.** Conceptual integration test. `@AfterTransaction` runs once the test-managed transaction has finished rolling back — the hook Spring documents for verifying post-rollback database state.

```java
@Service
public class OrderService {

    private final OrderRepository orders;
    private final AuditService audit; // separate bean → real proxy

    @Transactional
    public void placeOrderAndFail(Order order) {
        orders.save(order);
        audit.record(order); // REQUIRES_NEW in AuditService
        throw new IllegalStateException("force outer rollback");
    }
}

@Service
public class AuditService {

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void record(Order order) {
        auditRepository.save(AuditEntry.from(order));
    }
}
```

**Listing 2.** Conceptual production code under test. A `this.record()` call would **not** prove `REQUIRES_NEW`; see [[What is the difference between a self-invocation and a cross-bean Transactional call]].

## Pitfalls that fake a failure

> [!warning] Self-invocation makes `REQUIRES_NEW` look like `REQUIRED`
> If the inner `@Transactional(REQUIRES_NEW)` method is on the **same** class and invoked as `this.inner()`, the proxy is bypassed and the inner work joins the outer transaction. The test will show both rows rolled back — a false negative for independence.

> [!warning] Do not expect independence from a single joined transaction
> If both methods use default `REQUIRED` on one bean, there is only one physical transaction. Failing the outer rolls back everything, including audit rows written earlier in the same scope.

> [!warning] ORM false positives inside the test transaction
> When asserting **before** `@AfterTransaction`, flush the persistence context (`sessionFactory.getCurrentSession().flush()` / `entityManager.flush()`) so in-memory state matches JDBC counts. Spring’s testing docs call out unflushed Hibernate/JPA work as a common source of misleading passes.

## Optional: end the test transaction explicitly

`TestTransaction.flagForCommit()` + `TestTransaction.end()` commits the **test-managed** transaction programmatically. That is useful for other scenarios, but proving `REQUIRES_NEW` independence normally needs the default rollback path plus `@AfterTransaction`, not committing the whole test.

> [!tip] Interview answer
> **Set up outer `REQUIRED` and inner `REQUIRES_NEW` on separate beans, let the inner finish, then throw in the outer.** Query after rollback — via `@AfterTransaction` or JDBC counts — and expect the audit row committed while the business row did not. If both disappear, check for self-invocation or missing cross-bean proxy calls.
