<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Annotations #Java/Spring/Core/IoC/Configuration #SRS

# Which annotations tell Spring to create beans from your classes?

> [!abstract] Short answer
> **Type stereotypes** whose root is **`@Component` (2.5)**: the **annotated class** is a scan candidate; after a scanner (or `@Import` / `register`) writes a **`BeanDefinition`**, the container **constructs that class**. Built-in meta-stereotypes: **`@Service`**, **`@Repository`**, **`@Controller`**, **`@RestController`**, **`@Configuration`**. You can compose **your own** `@Component` meta-annotation. **`@Named` / `@ManagedBean`** are scan equivalents, **not** composable. **`@ComponentScan`** (or Boot’s **`@SpringBootApplication`**) is what **finds** those types — it does not mark them. **`@Bean`** creates a bean from a **method body**, not by annotating the implementation. **`@Autowired` does not create beans** ([[What is the relationship between a Spring stereotype component and a Spring bean]], [[What is the difference between Bean and Component in Spring]]).

## Marks on the class, then a scan

Classpath scanning registers **concrete** types that carry `@Component` or a **meta-stereotype** of it ([[What is the Spring ComponentScan annotation]]). Default bean **name** is the decapitalized simple class name (`value` on the annotation overrides).

| Annotation | What it means on **your** class |
|---|---|
| **`@Component`** | Generic scan candidate; Spring **constructs this type** |
| **`@Service` / `@Repository` / `@Controller`** | Same registration; **role** (and `@Repository` exception translation) ([[What is the difference between Repository Component Controller and Service annotations]], [[What is the Spring Service annotation]]) |
| **`@RestController`** | `@Controller` + `@ResponseBody` — still a component |
| **`@Configuration`** | Also a `@Component` (the config class **is** a bean) **plus** `@Bean` factories |
| **Custom `@Component` meta-annotation** | Your stereotype; default filters still match |
| **`@Named` / `@ManagedBean`** | JSR-330 / JSR-250 stand-ins for `@Component` — **cannot** build custom stereotypes from them |

```java
@Service
public class InvoiceService {
	public InvoiceService(InvoiceRepository invoices) { /* … */ }
}

@RestController
public class InvoiceResource {
	public InvoiceResource(InvoiceService invoices) { /* … */ }
}

@Configuration
@ComponentScan("com.example.app")
public class AppConfig { }
```

**Listing 1.** Conceptual. `InvoiceService` and `InvoiceResource` become beans **because** they are stereotyped **and** `AppConfig` scans their package. `@Service` alone on the classpath does **nothing**.

Without `@ComponentScan`, XML `<context:component-scan>`, `AnnotationConfigApplicationContext.scan`, or `@Import` of that class, stereotypes are **invisible** ([[What is the difference between Component and ComponentScan]], [[How do you create a bean in Spring]]).

```d2
direction: down
mark: "@Component / @Service / @Controller / …" {
  width: 300
  height: 40
  style.fill: "#fff3e0"
}
scan: "@ComponentScan / @Import / register" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
bean: "container constructs your class" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}

mark -> scan -> bean
```

**Fig. 1.** Annotation on the type is only **eligibility**. Instantiation is later, from the definition.

**`@Bean`** on a `@Configuration` method is the other creation path: you **`new`** (often a **library** type). That class usually has **no** stereotype ([[What is the Spring Bean annotation]]). **`@Autowired` / `@Inject` / `@Value` / `@Qualifier`** wire **existing** beans.

> [!warning] Stereotypes are not a container by themselves
> A `@Service` in a jar Spring never scans is **not** a bean. Boot’s `@SpringBootApplication` scan starts at **that class’s package** — types in a **sibling** package are missed.

> [!warning] `@Autowired` is not a creation annotation
> It does not register the declaring class. Putting it on a POJO you `new` yourself also does nothing; there is no container to inject.

> [!tip] Interview answer
> @Component and its meta-stereotypes — @Service, @Repository, @Controller, @RestController, @Configuration — tell Spring the class itself should become a bean once a scan or @Import sees it. @ComponentScan is the finder, not a mark on the service. @Bean is a factory method, not a class stereotype. @Autowired never creates beans.
