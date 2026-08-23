<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS

# What are Spring transaction propagation levels?

> [!abstract] Short answer
> Spring exposes **seven** `Propagation` values on `@Transactional` — the same EJB CMT names mapped to `TransactionDefinition`. **Default is `REQUIRED`**. The three most tested in interviews are **`REQUIRED`** (join or create), **`REQUIRES_NEW`** (suspend outer, independent physical TX), and **`NESTED`** (savepoint inside the current TX when supported).

## All seven levels

`org.springframework.transaction.annotation.Propagation` (Spring Framework reference + javadoc):

| Level | When a TX already exists | When none exists |
| --- | --- | --- |
| **`REQUIRED`** | Join | Create |
| **`SUPPORTS`** | Join | Non-transactional |
| **`MANDATORY`** | Join | **`IllegalTransactionStateException`** |
| **`REQUIRES_NEW`** | Suspend outer, new physical TX | New physical TX |
| **`NOT_SUPPORTED`** | Suspend outer, non-transactional | Non-transactional |
| **`NEVER`** | **`IllegalTransactionStateException`** | Non-transactional |
| **`NESTED`** | Nested TX (JDBC savepoint when supported) | Like `REQUIRED` |

```java
@Transactional // REQUIRED — default
public void updateAccount(Account a) { … }

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void writeAudit(AuditEntry e) { … }

@Transactional(propagation = Propagation.NESTED)
public void validateRow(Row row) { … }
```

**Listing 1.** Typical attribute usage from the `Propagation` enum / `@Transactional` API.

## REQUIRED vs REQUIRES_NEW vs NESTED

| | **`REQUIRED`** | **`REQUIRES_NEW`** | **`NESTED`** |
| --- | --- | --- | --- |
| Physical TX | Joins existing or creates one | **Always new**, independent | **Same** TX + savepoint |
| Inner commit before outer ends | No (shared commit) | **Yes** | No |
| Outer rollback undoes inner | Yes | **No** (if inner committed) | **Yes** |
| Typical use | Default service boundary | Audit/outbox that must survive outer rollback | Partial undo in a batch |

```d2
direction: right
req: "REQUIRED\none physical TX" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
new: "REQUIRES_NEW\n2nd connection" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
nest: "NESTED\nsavepoint" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

req -> new: "independent commit?"
req -> nest: "partial rollback?"
```

**Fig. 1.** Three propagation levels interviewers contrast most often. Overview: [[How would you explain Propagation]]; depth: [[How does REQUIRED transaction propagation work]], [[How does REQUIRES_NEW transaction propagation work]], [[How does NESTED transaction propagation work]].

> [!warning] `NESTED` needs savepoint support
> Out of the box, nested transactions apply to **`DataSourceTransactionManager`** (JDBC). Some JTA providers support nesting; many do not — see [[Does NESTED propagation require JDBC savepoints]].

> [!warning] `REQUIRES_NEW` / `NOT_SUPPORTED` need suspension
> JTA suspension may require a configured Jakarta `TransactionManager` on `JtaTransactionManager`.

> [!warning] Propagation applies only through the proxy
> Same-class `this.inner()` ignores the callee’s level — inner `REQUIRES_NEW` does not run ([[What happens when one Spring Transactional method calls another]]).

> [!tip] Interview answer
> **Seven levels: REQUIRED (default), SUPPORTS, MANDATORY, REQUIRES_NEW, NOT_SUPPORTED, NEVER, NESTED.** Know the trio: REQUIRED joins/creates one TX, REQUIRES_NEW suspends and commits independently, NESTED rolls back to a savepoint inside the same TX.
