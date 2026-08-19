<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When the `ApplicationContext` closes, dumps say Spring runs (if present):

1. `@PreDestroy`
2. `DisposableBean.destroy()`
3. `@Bean(destroyMethod)` / XML `destroy-method`

`@PreDestroy` runs once, just before the bean leaves the context. Same style rules as `@PostConstruct`: any access level, not static (dump). Typical use: close a connection or stop a background process.

Prototype beans: dumps often omit destroy callbacks unless you destroy the instance yourself.

> [!warning] Unverified traps from the dump
> - Standalone apps must `registerShutdownHook()` or `close()`; Boot registers the hook for you.
> - Dumps call `DisposableBean` dated, same as `InitializingBean`.
