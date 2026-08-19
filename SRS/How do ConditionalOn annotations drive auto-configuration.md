<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Auto-config classes use `@Conditional` so a bean is created only when it makes sense. Dumps name:

- `@ConditionalOnClass` / `@ConditionalOnMissingClass` — classpath
- `@ConditionalOnBean` / `@ConditionalOnMissingBean` — existing beans (`MissingBean` is why your `@Bean` wins over Boot's default)
- `@ConditionalOnProperty`
- `@ConditionalOnWebApplication` / `@ConditionalOnMissingWebApplication`

Dump example: `@ConditionalOnMissingBean` `ObjectMapper` only if you did not define one.

> [!warning] Unverified traps from the dump
> - `@ConditionalOnProperty` is Boot auto-config, not the same as a generic `@Conditional` on your own `@Configuration`.
