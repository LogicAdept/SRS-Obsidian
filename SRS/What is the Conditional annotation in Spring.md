<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Conditional` registers a `@Component` / `@Configuration` class or a `@Bean` method only when every listed `Condition` matches. Conditions run against `BeanDefinition`s **before** the bean exists — do not look up other beans inside `matches()`.

You implement `Condition.matches(ConditionContext, AnnotatedTypeMetadata)` and pass the class to `@Conditional`. Boot’s `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`, `@ConditionalOnWebApplication`, and `@Profile` (built on `@Conditional`) are the common specializations.

> [!warning] Unverified traps from the dump
> - Interacting with live beans inside a `Condition` is unsafe; only `BeanDefinition` metadata is available.
> - `@ConditionalOnProperty` is not the same as a custom `@Conditional` — it is one built-in condition.
