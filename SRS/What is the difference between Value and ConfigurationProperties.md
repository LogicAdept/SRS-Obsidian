<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #Java/Annotations #Java/Spring/Core/IoC/SpEL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Value("${payment.gateway.api-key}")` binds **one** property to a field. No grouped validation, no nested structure, easy to scatter related keys across classes.

`@ConfigurationProperties(prefix = "payment.gateway")` binds a related group into one typed object (often a record), optionally with Bean Validation (`@Validated`, `@NotBlank`, `@Min`). Missing or malformed config fails at startup instead of as a `null` later.

Dump guidance: use `@ConfigurationProperties` for anything beyond a single standalone value. Enable with `@EnableConfigurationProperties` or `@ConfigurationPropertiesScan`.

> [!warning] Unverified traps from the dump
> - Scattered `@Value` for a cohesive config surface has no built-in validation.
> - Immutable records need constructor binding (Boot 2.2+ / 3.x style); mutable JavaBean binding is the older pattern.
