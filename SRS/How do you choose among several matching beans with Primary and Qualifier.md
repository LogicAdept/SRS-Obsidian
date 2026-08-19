<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When several beans share a type, injection by type is ambiguous and startup fails with `NoUniqueBeanDefinitionException`.

`@Primary` marks the default candidate used whenever an injection point does not ask for a specific bean. Use it when one implementation is preferred most of the time.

`@Qualifier` names a candidate at the injection point (and/or on the bean). Use it for the non-default case, or when every implementation has equal priority and you always pick by name.

If you need to choose the bean at runtime from configuration, these annotations are not enough: expose a `@Bean` factory method that reads a property and returns the required implementation.

> [!warning] Unverified traps from the dump
> - `@Primary` alone does not help if you must use more than one implementation in the same context — then qualify each injection or inject `List<T>` / `Map<String, T>`.
> - Runtime selection from `application.properties` is a different mechanism from `@Primary` / `@Qualifier`.
