<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# What annotations are used to configure a Spring application context?

> [!abstract] Short answer
> Java-centric context setup is **`@Configuration` + `@Bean`**. Compose graphs with **`@Import`** (other configs / components / selectors), **`@ImportResource`** (XML), and **`@ComponentScan`** (stereotypes). Feed the `Environment` with **`@PropertySource`**; gate definitions with **`@Profile`** and **`@Conditional`**. Stereotypes (`@Component`, `@Service`, …) **register** beans only if a scan (or equivalent) sees them. **`@Autowired` / `@Value` / `@Qualifier` do not configure the context** — they inject into beans that already exist. Boot’s **`@SpringBootApplication`** is `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`. Bootstrap with `AnnotationConfigApplicationContext(AppConfig.class)` (that constructor **`refresh()`es**).

## Annotations that *define* the container

The Java-based container chapter’s **central artifacts** are `@Configuration` classes and `@Bean` methods. `@Configuration` marks a class as a **source of bean definitions**; `@Bean` on a method is the Java equivalent of a `<bean>` element (instantiate / configure / initialize). Inter-`@Bean` calls are intercepted only in **full** `@Configuration` (CGLIB); `@Bean` on a plain `@Component` is **lite** mode ([[Which Spring configuration style do you prefer XML Java or annotations and why]]).

```java
@Configuration
@ComponentScan("com.example.app")
@PropertySource("classpath:app.properties")
@Import(InfraConfig.class)
public class AppConfig {

	@Bean
	InvoiceRepository invoiceRepository() {
		return new JdbcInvoiceRepository();
	}
}
```

**Listing 1.** One entry `@Configuration`: scan, property files, imported config, explicit `@Bean`. No `http` schema on the class.

| Annotation | Role |
| --- | --- |
| **`@Configuration`** | This type is a definition factory (`@Component` meta-annotation — scannable). |
| **`@Bean`** | Method-produced bean; optional `initMethod` / `destroyMethod` / `@Scope` / `@Lazy` / `@Primary` / `@DependsOn` on the method. |
| **`@ComponentScan`** | Register `@Component` and meta-stereotypes (`@Service`, `@Repository`, `@Controller`, nested `@Configuration`) under `basePackages` (default: the config class’s package). |
| **`@Import`** | Pull in other `@Configuration` types, components (4.2+), `ImportSelector` / `ImportBeanDefinitionRegistrar` ([[How does Import register beans in Spring]]). |
| **`@ImportResource`** | Import XML when a namespace still earns its keep. |
| **`@PropertySource`** | Add a `.properties` (or XML Properties) file to the `Environment` ([[What is the PropertySource annotation in Spring]]). |
| **`@Profile` / `@Conditional`** | Register the class or `@Bean` only when the `Environment` / `Condition` matches ([[What is the Profile annotation in Spring]], [[What is the Conditional annotation in Spring]]). |

`@Enable*` annotations (`@EnableTransactionManagement`, `@EnableAspectJAutoProxy`, …) are **composed `@Import`s** of framework configuration — still context configuration, not injection.

```d2
AC: "AnnotationConfigApplicationContext"
Cfg: "@Configuration AppConfig"
Scan: "@ComponentScan → stereotypes"
Imp: "@Import / @ImportResource"
Bean: "@Bean methods"
AC -> Cfg: register + refresh
Cfg -> Scan
Cfg -> Imp
Cfg -> Bean
```

**Fig. 1.** Annotations on (and imported by) `@Configuration` become `BeanDefinition`s at `refresh()`. Processors that honor `@Autowired` are installed because this is an `AnnotationConfigApplicationContext` ([[What does context annotation-config register]]) — those processors are **not** the configuration annotations.

## What people mix in by mistake

**Injection:** `@Autowired`, `@Inject`, `@Resource`, `@Value`, `@Qualifier` — matching, not registration.

**Lifecycle / AOP on a bean:** `@PostConstruct`, `@Transactional` — they assume the bean is **already** a definition.

**XML-only equivalent:** `<context:component-scan>` / `<import>` with **no** Java annotations; still a valid context.

Boot: `@SpringBootApplication` on the main class is the usual **one** annotation that stands in for `@Configuration` + scan + auto-config. It is **not** required to have an `ApplicationContext`.

> [!warning] `@Component` without a scan does nothing
> A `@Service` sitting on the classpath is **not** in the context until `@ComponentScan`, `scan()`, XML component-scan, or an `@Import` of that class registers it. `@Configuration` without being passed to `AnnotationConfigApplicationContext` / `@Import` / a scan is equally invisible.

> [!tip] Interview answer
> Context configuration annotations: `@Configuration`, `@Bean`, `@ComponentScan`, `@Import` / `@ImportResource`, `@PropertySource`, plus `@Profile` / `@Conditional`. Stereotypes register types when scanned. `@Autowired` is not one of them. Boot wraps the first three as `@SpringBootApplication`.
