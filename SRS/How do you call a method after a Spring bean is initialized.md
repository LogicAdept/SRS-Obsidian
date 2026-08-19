<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list four ways to run code after the bean is constructed and dependencies are injected:

- `InitializingBean.afterPropertiesSet()`
- `@PostConstruct` (JSR-250 / Jakarta; handled by a `BeanPostProcessor`)
- XML `init-method` or `@Bean(initMethod = "…")`
- a custom `BeanPostProcessor` (`postProcessBeforeInitialization` / `postProcessAfterInitialization`)

`@PostConstruct` may have any access level and any return type (ignored). It must take no arguments. It can be static, but dumps say that is pointless because it only sees static members.

> [!warning] Unverified traps from the dump
> - `@PostConstruct` is Java EE / `javax.annotation`; from JDK 11 you need `jakarta.annotation-api` (or the old `javax.annotation-api`) on the classpath.
> - Dumps treat `InitializingBean` as dated and Spring-coupled; prefer `@PostConstruct` or a named init method.
