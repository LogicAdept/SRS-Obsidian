<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# When should you use `REQUIRES_NEW` transaction propagation?

> [!abstract] Short answer
> Use **`Propagation.REQUIRES_NEW`** when inner work must **commit on its own** and **survive an outer rollback** — audit rows, attempt counters, outbox inserts that must not vanish with the failed business TX. Prefer **`NESTED`** or joining **`REQUIRED`** when you only need a partial undo **inside** one physical transaction.

## Independent commit is the decision criterion

Spring’s reference docs: `REQUIRES_NEW` **always** uses a **separate physical transaction**. The outer transaction is **suspended**; the inner scope can commit or roll back without changing the outer rollback-only status, and its locks release when the inner TX ends.

Reach for it when:

* A side effect must **remain** after the caller fails (audit trail, “attempts” counter, durable outbox marker)
* Inner work needs its **own** isolation, timeout, or read-only settings (they are not inherited from the outer TX)
* You explicitly want the inner commit **before** the outer method returns

Do **not** use it as a default for every helper call — that is usually `REQUIRED`.

```java
@Service
public class PaymentService {

    private final AuditService audit;

    @Transactional
    public void charge(Payment payment) {
        ledger.debit(payment);
        audit.recordAttempt(payment); // REQUIRES_NEW — must survive charge failure
        gateway.charge(payment);      // may throw → outer rolls back
    }
}

@Service
public class AuditService {

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void recordAttempt(Payment payment) {
        attempts.save(Attempt.of(payment));
    }
}
```

**Listing 1.** Conceptual cross-bean pattern: attempt row commits even if `charge` rolls back. Mechanism: [[How does REQUIRES_NEW transaction propagation work]].

```d2
direction: down
need: "Inner work must survive\nouter rollback?" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
yes: "REQUIRES_NEW\nindependent physical TX" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
no: "REQUIRED or NESTED\nsame physical TX" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

need -> yes: "yes"
need -> no: "no"
```

**Fig. 1.** Choose `REQUIRES_NEW` only when independent persistence is a hard requirement — contrast [[What is the difference between REQUIRED and REQUIRES_NEW propagation]] and [[When should you use NESTED transaction propagation]].

> [!warning] Two connections while the outer TX is suspended
> The outer connection stays bound; the inner TX takes another. Undersized pools can stall or deadlock under load — [[Why can REQUIRES_NEW exhaust the connection pool]]. Size the pool above concurrent threads by at least one, as Spring’s docs warn.

> [!warning] Same-row locks between outer and inner
> Outer holds locks on rows the inner TX also touches → classic deadlock. Prefer not to update the same rows in both scopes — [[Why can REQUIRES_NEW deadlock when inner and outer touch the same rows]].

> [!warning] Self-invocation skips the new transaction
> `this.recordAttempt(...)` never opens `REQUIRES_NEW`. Use a separate bean (or AspectJ / self-injection) so the proxy applies.

> [!tip] Interview answer
> **Use `REQUIRES_NEW` when the inner work must commit independently and remain after an outer rollback** — classic audit or attempt logging. Spring suspends the outer TX and starts a new physical one, which costs a second connection. If you only need a savepoint-style partial undo, prefer `NESTED`.
