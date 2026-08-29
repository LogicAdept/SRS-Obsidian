<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# Which Spring annotation indicates that beans are being created or scanned?

> [!abstract] Short answer
> **Two different annotations — not one.** **`@ComponentScan` (3.1)** on a **`@Configuration`** class **indicates scanning**: walk packages, register `@Component` (and meta-stereotypes) as definitions, then **construct those classes**. **`@Bean` (3.0)** **indicates creation from a factory method**: you `new` and configure in the method — the Java `<bean>`. **`@Configuration`** is the usual **host** for both. Stereotypes (`@Service`, …) mark **candidates**; they do **not** turn scanning on. **`@Autowired` indicates injection, not creation or scan** ([[What is the difference between Component and ComponentScan]], [[What is the Spring Bean annotation]]).

## Scan switch vs factory method vs mark on the type

Interview dumps squeeze three features into “the annotation for beans”:

| Annotation | What it indicates |
|---|---|
| **`@ComponentScan`** | **Scanning is on** for `basePackages` (default: package of the annotated config, recursively) ([[What is the Spring ComponentScan annotation]]) |
| **`@Bean`** | **This method creates** a managed object |
| **`@Component` / `@Service` / …** | **This class** is a scan **candidate** if a scanner/`@Import`/`register` sees it ([[Which annotations tell Spring to create beans from your classes]]) |
| **`@Configuration`** | This type is a **definition factory** (itself a `@Component`, so it can be scanned) |

```java
@Configuration
@ComponentScan("com.example.app")
public class AppConfig {

	@Bean
	DataSource dataSource() {
		return new HikariDataSource();
	}
}
```

**Listing 1.** Conceptual. `@ComponentScan` → beans **from your stereotyped classes**. `@Bean` → bean **from this method** (`HikariDataSource` has no stereotype). Boot’s `@SpringBootApplication` **includes** `@ComponentScan` **and** `@Configuration` (plus auto-config) — same two stories, one type.

XML: `<context:component-scan>` is the scan switch; `<bean>` is creation. Programmatic scan: `AnnotationConfigApplicationContext.scan(…)`. `@Import(SomeService.class)` registers **one** class **without** a package walk ([[How does Import register beans in Spring]]).

```d2
direction: down
cfg: "@Configuration" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
scan: "@ComponentScan\n→ stereotyped classes" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
bean: "@Bean methods\n→ new in the method" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}

cfg -> scan
cfg -> bean
```

**Fig. 1.** Created **or** scanned are **parallel** definition sources on the same config type ([[What annotations are used to configure a Spring application context]]).

Without `@ComponentScan` (and without `@Import` / `register` / XML scan), a `@Service` on the classpath is **invisible**. `@ComponentScan` with **no** matching stereotypes registers **no** application beans from that walk ([[What is the difference between Bean and Component in Spring]]).

> [!warning] There is no single “beans annotation”
> Answering only `@Component`, only `@Bean`, or only `@SpringBootApplication` without the split fails. Scan **finds** types; `@Bean` **constructs** what you write; stereotypes **label** types.

> [!warning] `@Autowired` is the wrong box
> It does not register a class and does not start a scan. Putting it on a type you `new` yourself also does nothing.

> [!tip] Interview answer
> @ComponentScan means we are scanning packages for @Component and stereotypes. @Bean means this method creates a bean. I put both on @Configuration. @Service only marks a candidate; without a scan or @Import it is not a bean. @Autowired never creates or scans.
