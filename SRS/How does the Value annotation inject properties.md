<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/SpEL #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Value` injects a single value into a field or parameter from property sources, environment variables, or a SpEL expression.

```java
@Value("${maxReadResults}")
private int maxReadResults;
```

XML equivalent in dumps: a `PropertyPlaceholderConfigurer` / property-configure bean. For a group of related keys, dumps prefer `@ConfigurationProperties` (Boot card).

> [!warning] Unverified traps from the dump
> - Missing property fails startup unless you give a default (`${name:default}`).
> - SpEL `#{}` is not the same as placeholder `${}`.
