<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How do transactions work in Quarkus?

> [!abstract] Short answer
> The `quarkus-narayana-jta` extension provides the **Narayana transaction manager** implementing Jakarta Transactions (JTA). You draw boundaries **declaratively** with `jakarta.transaction.Transactional` on CDI bean methods or classes — `REQUIRED` by default, plus `REQUIRES_NEW`, `MANDATORY`, `SUPPORTS`, `NOT_SUPPORTED`, `NEVER` — or **programmatically** with `QuarkusTransaction` / an injected `UserTransaction`. System exceptions roll back by default; `rollbackOn`/`dontRollbackOn` tune that, and `TransactionManager.setRollbackOnly()` marks failure without throwing. For the reactive stack, Hibernate Reactive uses `@WithTransaction` instead.

## Declarative boundaries and propagation

`@Transactional` is an interceptor resolved by ArC at build time: when the method runs, the interceptor starts, joins, suspends or refuses a transaction per the propagation mode before the business method executes ([[What bean scopes does Quarkus support]]). Class-level placement makes every public method transactional — the standard shape for a REST resource that writes. Runtime exceptions trigger rollback by default; checked exceptions do not unless listed in `rollbackOn` (the reverse of what many assume coming from plain JDBC autocommit). Manual control exists for exotic cases: inject `TransactionManager` and call `setRollbackOnly()`, or use the programmatic `QuarkusTransaction.call(...)` / `UserTransaction` API where annotations are out of reach.

```java
// Transaction + rollback proof (JDK 21, Quarkus 3.39.2, H2 via Agroal; mvn test: 6/6 green).
package org.acme.check.data;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.transaction.Transactional;

@ApplicationScoped
public class TransferService {

    @Transactional
    public void transfer(long fromId, long toId) {
        Person from = Person.findById(fromId);
        Person to = Person.findById(toId);
        from.age -= 10;
        to.age += 10;
    }

    @Transactional(rollbackOn = IllegalStateException.class)
    public void transferFailing(long fromId, long toId) {
        transfer(fromId, toId);
        throw new IllegalStateException("rolled back on purpose");
    }
}
// Test evidence (ExpansionTest, verbatim assertions):
// assertThrows(IllegalStateException.class, () -> transfers.transferFailing(id, id));
// Person after = Person.findById(id);
// assertEquals(30, after.age, "rollback must restore age");
// The UPDATE inside the failed method left no trace - Narayana rolled the tx back.
```

**Listing 1.** The money moves inside a transaction that then aborts; the value read afterwards is the pre-transaction one. That single assertion demonstrates both the JTA boundary and the rollback semantics ([[What is Panache in Quarkus]]).

```d2
direction: down
call: "Caller invokes\n@Transactional method" {
  width: 250
  height: 60
}
int: "ArC interceptor\nNarayana JTA" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
prop: "Propagation\nREQUIRED | REQUIRES_NEW | MANDATORY | SUPPORTS | NOT_SUPPORTED | NEVER" {
  width: 420
  height: 60
  style.fill: "#e3f2fd"
}
work: "Business method\nJDBC work via Agroal connection" {
  width: 300
  height: 65
  style.fill: "#fff3e0"
}
ok: "commit" {
  width: 120
  height: 40
  style.fill: "#e8f5e9"
}
rb: "runtime exception / rollbackOn\n-> rollback" {
  width: 280
  height: 55
  style.fill: "#f5c6c6"
}
call -> int -> prop -> work
work -> ok: "returns normally"
work -> rb: "throws"
```

**Fig. 1.** The annotation is the boundary, the interceptor is the mechanism, propagation decides join-vs-start, and the exception class decides commit or rollback.

## Reactive transactions

Blocking JDBC and Hibernate Reactive are separate worlds: the reactive ORM's operations are `Uni` chains that must run on Vert.x contexts, and JTA thread-bound semantics do not fit them — hence `@WithTransaction` (Panache reactive) and `@WithSession`/`@WithSessionOnDemand` for session management. Mixing both stacks against one database in the same request is a classic design smell; pick one per service ([[What is Hibernate Reactive in Quarkus]]).

> [!warning] Checked exceptions do not roll back by default
> Coming from Spring many people expect every `Exception` to abort the transaction; JTA semantics are the opposite — only runtime exceptions (and errors) roll back unless `rollbackOn` names the checked class. The second trap: `@Transactional` on **private** methods or on same-bean internal calls (`this.method()`) never passes the interceptor — the boundary is a proxy invocation, so the annotation is silently ignored. Interviewers use exactly this case as the "did you understand interceptors" probe.

> [!tip] Interview answer
> Quarkus ships the Narayana JTA transaction manager. Boundaries are declarative with jakarta @Transactional on bean methods or classes — REQUIRED by default with the full propagation set — or programmatic via QuarkusTransaction and UserTransaction. Runtime exceptions roll back by default, checked ones don't unless rollbackOn says so, and TransactionManager.setRollbackOnly covers manual cases. Reactive stacks use @WithTransaction instead, because JTA's thread binding doesn't fit Uni pipelines.
