<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What are transaction propagation semantics in Spring or JTA?

> [!abstract] Short answer
> **Propagation defines how a new transactional method relates to an existing transaction — join, create, suspend, nest, or refuse.** In Spring, each advised method gets a **logical** transaction scope; propagation decides whether that scope maps to a **new physical** transaction, joins the current one, or runs without one. The same seven names exist on Spring’s `Propagation` enum, `TransactionDefinition`, and classic **EJB/JTA CMT**; portable behavior still depends on the **`PlatformTransactionManager`** (JDBC vs JTA).

## Physical vs logical scopes

Spring’s Transaction Propagation reference: in Spring-managed transactions, distinguish **physical** transactions (one commit/rollback on the resource) from **logical** scopes (one per `@Transactional` method that the interceptor opens).

* **`REQUIRED`:** each method gets a logical scope; nested `REQUIRED` calls usually share **one physical** transaction — inner rollback-only poisons the whole unit ([[What is UnexpectedRollbackException in Spring REQUIRED propagation]]).
* **`REQUIRES_NEW`:** each scope gets its **own physical** transaction; the outer one is **suspended** while the inner runs.
* **`NESTED`:** one physical transaction with **savepoints** for partial rollback (JDBC-first).

Propagation is evaluated at the **proxy interceptor** when a method is entered — not when SQL runs. Same-class `this` calls skip that boundary ([[What happens when one Spring Transactional method calls another]]).

```d2
direction: down
call: "Cross-bean call\nenters @Transactional method" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
logic: "Logical scope\n(propagation policy)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
phys: "Physical TX on resource\n(JDBC / JTA)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

call -> logic -> phys
```

**Fig. 1.** Propagation connects the logical scope to join/create/suspend/nest behavior on the physical transaction.

## Spring and JTA use the same names

`Propagation` javadoc: values correspond to **`TransactionDefinition`** and EJB transaction attributes (`REQUIRED`, `REQUIRES_NEW`, …). **`NESTED`** has **no EJB analogue** — Spring-specific savepoint semantics.

With **`JtaTransactionManager`**, Spring delegates begin/commit/suspend to the Jakarta **`TransactionManager`**. The enum names are portable; **capabilities are not**:

| Propagation | JDBC (`DataSourceTransactionManager`) | JTA notes |
| --- | --- | --- |
| `REQUIRED`, `SUPPORTS`, `MANDATORY` | Join/create as defined | Standard CMT mapping |
| `REQUIRES_NEW`, `NOT_SUPPORTED` | Suspend outer, new/suspended work | Suspension needs a configured **`TransactionManager`** on `JtaTransactionManager` — not automatic on every server |
| `NESTED` | Savepoints via JDBC | Only some JTA providers; often use `REQUIRED` or `REQUIRES_NEW` instead |

Level names and defaults: [[What are Spring transaction propagation levels]], [[How would you explain Propagation]]. Independent inner commit: [[How does REQUIRES_NEW transaction propagation work]].

> [!warning] JTA suspension is not guaranteed out of the box
> `Propagation.REQUIRES_NEW` / `NOT_SUPPORTED` javadoc: actual suspension may fail without a server-provided Jakarta `TransactionManager` wired into `JtaTransactionManager`.

> [!warning] Do not assume `NESTED` on JTA
> Spring maps `NESTED` to JDBC savepoints by default. On JTA, verify provider support or pick `REQUIRES_NEW` / `REQUIRED` explicitly.

> [!warning] Participating TX ignores local isolation/readOnly by default
> Under `REQUIRED`, inner isolation/timeout/readOnly are typically **ignored** unless the transaction manager runs in strict validation mode.

> [!tip] Interview answer
> **Propagation is the rule for joining or starting work when a transactional method runs.** Spring creates a logical scope per advised method and maps it to physical JDBC or JTA transactions. Same seven CMT names; `NESTED` is Spring-specific. JTA portability breaks on suspension and nesting — check the transaction manager, not just the annotation.
