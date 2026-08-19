<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/SpEL #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@PropertySource("classpath:custom.properties")` on a `@Configuration` class loads that file into the Spring `Environment` so `@Value` / `Environment.getProperty` can see the keys.

```java
@Configuration
@PropertySource("classpath:custom.properties")
public class AppConfig {
    @Value("${custom.dir}")
    private String dirName;
}
```

Repeat the annotation (or `@PropertySources`) for several files. Boot still layers `application.yml` with higher-precedence sources.

> [!warning] Unverified traps from the dump
> - `@PropertySource` is lower precedence than env vars / command line in Boot’s order.
> - It does not replace `@ConfigurationProperties` binding of a typed prefix.
