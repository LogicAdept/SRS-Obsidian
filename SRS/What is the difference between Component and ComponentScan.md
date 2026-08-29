<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Annotations #Java/Spring/Core/IoC/Configuration #SRS

# What is the difference between Component and ComponentScan?

> [!abstract] Short answer
> **`@Component` (2.5)** marks **this class** as a **candidate** for autodetection — “I am a Spring-managed type” ([[What is the difference between Bean and Component in Spring]]). **`@ComponentScan` (3.1)** sits on a **`@Configuration`** class and **tells the container where to look**: scan `basePackages` (or, if omitted, the **package of that config class**, recursively) and register matching stereotypes as `BeanDefinition`s ([[What is the Spring ComponentScan annotation]]). XML cousin is `<context:component-scan>`. A `@Component` with **no** scan / `@Import` / `register` is **not** a bean. `@ComponentScan` without any `@Component` (or meta-stereotype) in those packages registers **nothing**.

## Marker vs search directive

Classpath scanning: stereotyped classes become definitions only after you **enable detection**. Default candidates: `@Component`, `@Repository`, `@Service`, `@Controller`, `@Configuration`, or a custom annotation **meta-annotated** with `@Component` ([[How do you create a bean in Spring]]). Filters can widen or narrow that set ([[How do ComponentScan include and exclude filters work]]).

```java
@Component
public class BillingService { }

@Configuration
@ComponentScan("com.example.app") // or @ComponentScan — this config’s package
public class AppConfig { }
```

**Listing 1.** Conceptual. `BillingService` is a **candidate**. `AppConfig` **runs the scanner**. `@ComponentScan("org.example")` is `value` = `basePackages`. `basePackageClasses` is the type-safe form.

`@ComponentScan` does **not** have XML’s `annotation-config` flag: with this annotation, `@Autowired` processing is **assumed**. On `AnnotationConfigApplicationContext` those processors are **always** registered. Repeatable; local `@ComponentScan` **hides** meta-annotated ones. Placeholders `${…}` and Ant-style `org.example.**` are allowed in package names.

Programmatic equivalent: `AnnotationConfigApplicationContext.scan("com.example.app")`. `@Import(BillingService.class)` registers **one** component **without** a package walk ([[How does Import register beans in Spring]]). Boot’s `@SpringBootApplication` **includes** `@ComponentScan` (same default: the application class’s package).

```d2
direction: down
scan: "@ComponentScan on @Configuration" {
  width: 280
  height: 45
  style.fill: "#fff3e0"
}
pkg: "basePackages / this package" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
hit: "@Component / @Service / …" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

scan -> pkg -> hit
```

**Fig. 1.** Scan is the **search**. Stereotype is the **hit**. They are not interchangeable ([[What annotations are used to configure a Spring application context]]).

| | **`@Component`** | **`@ComponentScan`** |
| --- | --- | --- |
| Target | Your **component type** | A **`@Configuration`** type |
| Role | “Register **me** if found” | “**Search** these packages” |
| Instantiates | The annotated class | Nothing by itself |
| XML | (stereotype on the class) | `<context:component-scan base-package="…"/>` |

> [!warning] `@ComponentScan` on a `@Service` does not “turn scanning on”
> The scanner is configured from **configuration** classes (and Boot’s main class). Putting `@ComponentScan` next to `@Component` on a random service is the wrong type and is easy to miss. `@Component` without a scan that **covers its package** stays invisible.

> [!warning] Default package is easy to get wrong
> Bare `@ComponentScan` scans the **declaring class’s** package **and subpackages**, not the whole classpath. A config in `com.example.config` will **not** see `com.example.web` unless you name that package (or a parent). Scanning `com` or `org` pulls far too much.

> [!tip] Interview answer
> @Component labels a class as a bean candidate. @ComponentScan on a @Configuration class is the instruction to walk packages and register those candidates, defaulting to the config class’s own package. I need both: the marker on application types and a scan (or Import/register) that actually finds them. They are not two names for the same annotation.
