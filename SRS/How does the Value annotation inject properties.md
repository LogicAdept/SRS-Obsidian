<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/SpEL #Java/Annotations #SRS

# How does the `@Value` annotation inject properties?

> [!abstract] Short answer
> `@Value` is processed by `AutowiredAnnotationBeanPostProcessor` on a **field** or **method/constructor parameter**. `${catalog.name}` is a property placeholder resolved against the `Environment` (files via `@PropertySource`, JVM system properties, environment variables, …). `#{…}` is a **SpEL** expression evaluated at runtime. They are not interchangeable. Framework’s default resolver is **lenient**; a missing `${}` becomes the literal placeholder string unless you install a strict `PropertySourcesPlaceholderConfigurer`.

## Placeholders versus SpEL

`@Value` (since 3.0) is one expression, one injection point — not a typed bag of keys ([[What is the difference between Value and ConfigurationProperties]]). Typical wiring:

1. Put keys in a file and attach it with `@PropertySource` so they join the `Environment` ([[What is the PropertySource annotation in Spring]], [[What is the Spring Environment]]).
2. Annotate a constructor parameter or field: `@Value("${catalog.name}")`.
3. Spring converts the resolved `String` with a `ConversionService` (`int` / `Integer` work; comma-separated values become a `String[]`).

`StandardEnvironment` already searches JVM **system properties** and **environment variables**. `PropertySourcesPlaceholderConfigurer` also falls back to `Environment` and `System` properties after any files you give it. XML equivalent: a `PropertySourcesPlaceholderConfigurer` bean or `<context:property-placeholder location="…"/>` — not the older `PropertyPlaceholderConfigurer` name from dumps.

`${catalog.name:defaultCatalog}` supplies a default when the key is absent. You can change prefix, suffix, value separator, and escape character on the configurer (`setValueSeparator`, `spring.placeholder.escapeCharacter.default` as a JVM / `SpringProperties` setting).

`#{systemProperties['user.catalog'] + 'Catalog'}` is SpEL ([[What is Spring Expression Language]]): computed at runtime, can call into the object graph, maps, beans. That is not placeholder lookup. A property key written as `#{catalog.name}` does not resolve `application.properties`.

```java
@Component
public class MovieRecommender {

    private final String catalog;
    private final int maxReadResults;

    public MovieRecommender(
            @Value("${catalog.name}") String catalog,
            @Value("${maxReadResults:25}") int maxReadResults) {
        this.catalog = catalog;
        this.maxReadResults = maxReadResults;
    }
}

@Configuration
@PropertySource("classpath:application.properties")
public class AppConfig {
}
```

**Listing 1.** Conceptual. Constructor `@Value` placeholders; `maxReadResults` converts to `int` and uses `:25` if the key is missing.

```java
@Configuration
public class AppConfig {

    @Bean
    public static PropertySourcesPlaceholderConfigurer propertyPlaceholderConfigurer() {
        return new PropertySourcesPlaceholderConfigurer();
    }
}

@Component
public class MovieRecommender {

    public MovieRecommender(
            @Value("#{systemProperties['user.catalog'] + 'Catalog'}") String catalog) {
        // SpEL, not ${}
    }
}
```

**Listing 2.** Conceptual. A **static** `@Bean` `PropertySourcesPlaceholderConfigurer` makes unresolved `${}` fail context startup. `#{}` is a different language.

```d2
direction: down
sources: "@PropertySource files\nSystem properties\nenv vars" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
env: "Environment" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
val: "@Value on field\nor parameter" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
ph: "${key:default}\nplaceholder" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
spel: "#{expression}\nSpEL" {
  width: 180
  height: 70
  style.fill: "#fce4ec"
}

sources -> env -> val
val -> ph
val -> spel
```

**Fig. 1.** `@Value` either resolves a placeholder through the `Environment` (and optional `PropertySourcesPlaceholderConfigurer`) or evaluates SpEL. Same annotation, two languages.

Without a `PropertySourcesPlaceholderConfigurer`, Spring still ships a **lenient** embedded resolver: an unknown `${catalog.name}` injects the string `${catalog.name}` instead of failing. Declaring that configurer (the `@Bean` method **must** be `static` in Java config) fails initialization on unresolved placeholders. Spring Boot registers such a configurer by default and loads `application.properties` / `application.yml`.

`@Value` cannot be used on `BeanPostProcessor` or `BeanFactoryPostProcessor` types — the same post-processor that reads `@Value` (`AutowiredAnnotationBeanPostProcessor`) does not apply to those types. Custom conversion: register a `ConversionService` bean (`DefaultFormattingConversionService` plus your `Converter`).

For XML bean definitions the same `${property-name}` tokens are substituted by `PropertySourcesPlaceholderConfigurer` ([[What is PropertySourcesPlaceholderConfigurer]]). One placeholder configurer per syntax; extra property files belong in that configurer’s locations, not a second conflicting `${}` configurer.

> [!warning] Missing key does not always fail startup
> Core Spring is lenient until you add `PropertySourcesPlaceholderConfigurer` (Boot already does). `${name:default}` is the placeholder default, not a SpEL default. After a strict configurer is in place, a typo with no default **does** abort refresh.

> [!warning] `${}` is not `#{}`
> `${catalog.name}` is a placeholder against the `Environment`. `#{…}` is SpEL (`systemProperties`, maps, bean references). A property key inside `#{}` is not looked up as `${}` unless the expression actually consults the environment. `@Value` on a `BeanFactoryPostProcessor` or `BeanPostProcessor` is not processed.

> [!tip] Interview answer
> @Value injects one expression into a field or constructor parameter. Dollar-brace placeholders resolve against the Environment and optional property files; hash-brace is SpEL evaluated at runtime. By default an unknown placeholder is injected as the literal ${key} unless you declare a PropertySourcesPlaceholderConfigurer, which Boot already does. Use a colon default on the placeholder, and do not put @Value on a BeanPostProcessor.
