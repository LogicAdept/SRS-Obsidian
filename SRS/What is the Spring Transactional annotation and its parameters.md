<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #Java/Annotations #SRS

# What is the Spring `Transactional` annotation and its parameters?

> [!abstract] Short answer
> **`@Transactional` is metadata** on a class or method that tells Spring’s transaction infrastructure how to demarcate work around that method once **`@EnableTransactionManagement`** and a **`PlatformTransactionManager`** are registered. Defaults: **`REQUIRED`**, **`ISOLATION_DEFAULT`**, read-write, default timeout, rollback on **`RuntimeException`/`Error`** only. Attributes tune propagation, isolation, timeout, read-only, rollback rules, and which manager to use.

## Metadata plus AOP proxy (default)

The annotation alone does not open transactions. `@EnableTransactionManagement` (or XML `<tx:annotation-driven/>`) switches on infrastructure that reads the metadata and wraps the bean in an AOP **proxy** (JDK interface proxy or CGLIB class proxy). **`TransactionInterceptor`** delegates begin/commit/rollback to the chosen **`PlatformTransactionManager`** — see [[How do you use AOP to manage transactions]].

Only **external** calls through the proxy are advised; **`this.inner()`** bypasses it ([[What happens when one Spring Transactional method calls another]]). Class-level `@Transactional` applies to methods of the class and **subclasses**; inherited methods on ancestors are **not** covered unless redeclared on the subclass.

Method-level attributes **override** class-level defaults for that method.

```java
@Transactional(readOnly = true)
@Service
public class ReportService {

    public Report load(String id) { … }

    @Transactional(readOnly = false, propagation = Propagation.REQUIRES_NEW)
    public void rebuild(String id) { … }
}
```

**Listing 1.** Method settings take precedence — from Spring Framework `@Transactional` reference.

## Parameter reference

| Attribute | Default | Role |
| --- | --- | --- |
| **`propagation`** | `REQUIRED` | Join/create/suspend/nest policy — [[What are Spring transaction propagation levels]] |
| **`isolation`** | `DEFAULT` | Isolation level; applies only when a **new** TX starts (`REQUIRED` / `REQUIRES_NEW`) |
| **`timeout`** / **`timeoutString`** | `-1` (system default) | Seconds; same new-TX rule as isolation |
| **`readOnly`** | `false` | Hint for read-only optimization; same new-TX rule |
| **`rollbackFor`**, **`noRollbackFor`** | none | Type-safe rollback rules |
| **`rollbackForClassName`**, **`noRollbackForClassName`** | none | Pattern-based rules (easy to over-match) |
| **`value`** / **`transactionManager`** | `""` | Bean name / qualifier of the `TransactionManager` to use |
| **`label`** | `{}` | Optional labels for manager-specific behavior |

Rollback defaults and overrides: [[What is Spring default rollback policy for Transactional]]. Spring **6.2+**: `@EnableTransactionManagement(rollbackOn = ALL_EXCEPTIONS)` can flip the global default to roll back on checked exceptions too.

```java
@Transactional(
    propagation = Propagation.REQUIRED,
    isolation = Isolation.READ_COMMITTED,
    timeout = 30,
    readOnly = false,
    rollbackFor = { IOException.class },
    noRollbackFor = { BusinessWarningException.class },
    transactionManager = "orderTxManager"
)
public void placeOrder(Order order) throws IOException { … }
```

**Listing 2.** Conceptual combination of attributes from Table 2 in the reference docs.

```d2
direction: right
ann: "@Transactional\nmetadata" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
proxy: "AOP proxy +\nTransactionInterceptor" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
mgr: "PlatformTransactionManager" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

ann -> proxy -> mgr
```

**Fig. 1.** Attributes configure the interceptor; the manager drives the resource transaction.

> [!warning] Private methods are not advised in default proxy mode
> `@Transactional` is typically on **public** methods; as of Spring **6.0**, **protected** / package-visible methods can work on class-based proxies. Interface-based proxies still require **public** methods on the interface.

> [!warning] Long non-DB work inside the boundary
> A transaction holds the JDBC connection (or JTA enlistment) for the whole method — external HTTP calls inside `@Transactional` can starve the pool. Shorten the boundary or move I/O outside.

> [!warning] `@EnableTransactionManagement` scans its own context only
> Transaction metadata on beans in a **different** application context (for example services vs a child `WebApplicationContext`) is not picked up unless transaction management is enabled there too.

> [!tip] Interview answer
> **`@Transactional` declares transaction metadata; Spring’s proxy and `TransactionInterceptor` apply it at runtime.** Know defaults: `REQUIRED`, default isolation, read-write, rollback on unchecked only. Tune propagation, isolation, timeout, readOnly, rollback rules, and `transactionManager`. It only works on proxied external calls — not `this` self-invocation.
