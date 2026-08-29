<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# What is the Spring ComponentScan annotation?

> [!abstract] Short answer
> **`@ComponentScan` (3.1)** on a **`@Configuration`** class **enables classpath autodetection**: Spring walks **`basePackages`** (alias **`value`**) and **subpackages**, registers types with `@Component` or a **meta-stereotype** (`@Service`, `@Repository`, `@Controller` / `@RestController`, `@Configuration`, custom `@Component` meta-annotations) as **`BeanDefinition`s**, then instantiates **beans**. If you omit packages, it scans **recursively from the package of the class that declares the annotation**. XML: `<context:component-scan>`. Without a scan (or `@Import` / `register`), a `@Component` on the classpath is **invisible** ([[What is the difference between Component and ComponentScan]]).

## Where to look, then register

Classpath-scanning chapter: you need `@ComponentScan` on configuration so stereotyped classes become definitions. `@ComponentScan("org.example")` is `value` = `basePackages`. **`basePackageClasses`** is the type-safe form (often a marker type in that package). Package strings may include **`${…}`** (Environment) and Ant-style **`org.example.**`**. Repeatable; a **local** `@ComponentScan` **hides** meta-annotated ones.

```java
@Configuration
@ComponentScan("com.example.app")
public class AppConfig { }
```

**Listing 1.** Conceptual. Finds `com.example.app.BillingService` and `com.example.app.web.HomeController`. Nested `@Configuration` types in those packages are registered too, so their **`@Bean` methods** join the container ([[What is the Spring Bean annotation]]).

This annotation has **no** `annotation-config` flag: `@Autowired` processing is **assumed**. On `AnnotationConfigApplicationContext` those processors are **always** on. Programmatic: `ctx.scan("com.example.app")`. `@Import(BillingService.class)` registers **one** class **without** a package walk ([[How does Import register beans in Spring]]). Boot’s `@SpringBootApplication` **includes** `@ComponentScan` with the same default package (put that class in the **root** of the app).

Default filters (`useDefaultFilters = true`) match `@Component` and meta-stereotypes; Jakarta `@Named` is an extra include if present. **`includeFilters` / `excludeFilters`** change that set ([[How do ComponentScan include and exclude filters work]]). After filters, the scanner keeps **concrete** top-level classes (not interfaces), except types with `@Lookup`. **`lazyInit`**, **`scopedProxy`**, **`nameGenerator`**, **`resourcePattern`** (`**/*.class`) tune registration.

```d2
direction: down
ann: "@ComponentScan on @Configuration" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
pkg: "basePackages + subpackages" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
hit: "stereotype types → BeanDefinition" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}

ann -> pkg -> hit
```

**Fig. 1.** Search directive, not a stereotype on the service class ([[What annotations are used to configure a Spring application context]]).

`<context:component-scan base-package="…"/>` also **turns on** `annotation-config`. You rarely need both tags.

> [!warning] Default package is the **declaring** class, not the whole classpath
> A config in `com.example.config` does **not** see `com.example.web` unless you name a **parent** or that package. Scanning `com` or `org` is too wide. Dump “default = `@SpringBootApplication` package” is true **on Boot’s main class**, not on every `@Configuration`.

> [!warning] Do not put `@ComponentScan` on a random `@Service`
> The scanner is configured from **configuration** (and Boot’s application class). Stereotypes belong on **components**; the scan annotation belongs on **config**.

> [!tip] Interview answer
> @ComponentScan tells Spring which packages to walk for @Component and its stereotypes, defaulting to the package of the annotated @Configuration class and all subpackages. Found classes become beans. It is how the container learns about those annotations; without it they do nothing. XML is context:component-scan. Filters, lazyInit, and scopedProxy are optional knobs.
