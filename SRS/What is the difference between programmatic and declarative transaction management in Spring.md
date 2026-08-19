<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

**Programmatic:** you start/commit/rollback yourself with `PlatformTransactionManager` or `TransactionTemplate`. Flexible, harder to maintain. Used when only a few code paths need explicit control.

**Declarative:** `@Transactional` (or XML) plus a proxy interceptor. Preferred. `@EnableTransactionManagement` on a `@Configuration` class; Boot with `spring-tx` / `spring-data-*` enables it by default.

`TransactionInterceptor` wraps the call: `TransactionManager` decides whether to start a new transaction (propagation, existing tx on the thread), binds `EntityManager` / JDBC `Connection` to `ThreadLocal`, then commit or rollback after the method.

> [!warning] Unverified traps from the dump
> - Declarative tx is AOP: `this.otherTransactionalMethod()` skips the proxy.
> - Calling a `@Transactional` method from a non-transactional method on the **same** class also skips the proxy.
