<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# What configuration styles exist in Spring?

> [!abstract] Short answer
> The container is **decoupled from metadata format**. Official styles: **XML** (`<bean>`, namespaces); **Java `@Configuration` / `@Bean`** (3.0+); **classpath stereotypes** (`@Component` + `@ComponentScan`); **annotation-driven injection** on existing beans (`@Autowired` — **2.5+**, does **not** register types); **Groovy** (`GenericGroovyApplicationContext` / `GroovyBeanDefinitionReader`); **programmatic** (`GenericApplicationContext` + a reader, or `register`/`scan`). You **mix** them (`@ImportResource`, XML `<bean class="…@Configuration">`). Preference is a separate question ([[Which Spring configuration style do you prefer XML Java or annotations and why]]).

## Formats that become `BeanDefinition`s

IoC intro: metadata may be **XML, annotations, or Java code**. Same `ApplicationContext.refresh()` either way ([[Which ApplicationContext implementations are commonly used]]).

```java
ApplicationContext xml = new ClassPathXmlApplicationContext("services.xml");
ApplicationContext java = new AnnotationConfigApplicationContext(AppConfig.class);
ApplicationContext groovy = new GenericGroovyApplicationContext("context.groovy");
```

**Listing 1.** Three convenience bootstraps. `AnnotationConfigApplicationContext` also accepts **package names** (`scan`) or `register(Class…)` then `refresh()`.

| Style | What you write | Typical loader |
| --- | --- | --- |
| **XML** | `<bean id class>`, `<import>`, `tx`/`aop` namespaces | `ClassPathXmlApplicationContext` / `XmlBeanDefinitionReader` |
| **Java config** | `@Configuration` + `@Bean`, `@Import` | `AnnotatedBeanDefinitionReader` + `ConfigurationClassPostProcessor` |
| **Component scan** | `@Component` / `@Service` / … on the type | `ClassPathBeanDefinitionScanner` / `@ComponentScan` |
| **Injection annotations** | `@Autowired`, `@Inject`, `@Resource`, `@Value` | Processors from `annotation-config` — beans must **already** exist ([[What does context annotation-config register]]) |
| **Groovy** | Groovy bean DSL (XML-like, not angle brackets) | `GenericGroovyApplicationContext` / `GroovyBeanDefinitionReader` |
| **Mix** | `@ImportResource`, or XML that lists a `@Configuration` class | Java-centric or XML-centric bootstrap |

```d2
Meta: "XML / @Configuration / @Component / Groovy"
BD: BeanDefinition
Ctx: ApplicationContext
Meta -> BD -> Ctx: refresh()
```

**Fig. 1.** Styles differ in **how you write** recipes. They do not replace the container.

`AnnotationConfigApplicationContext` holds both a **reader** (register `@Configuration` / components you pass in) and a **scanner** (packages). `@Conditional` (4.0+) can skip a class or `@Bean` **before** the definition is registered ([[What annotations are used to configure a Spring application context]]).

XML still matters where **namespaces** are the documented fit; `@Configuration` is **not** a 100% XML replacement. Boot typically hides the choice behind `@SpringBootApplication` (Java config + scan + auto-config).

> [!warning] “Annotation config” is three styles
> Dumps merge **(1)** `@Autowired` on a class that XML/`@Bean` registered, **(2)** `@Component` scan, **(3)** `@Configuration`. Only (2) and (3) **create** definitions. (1) without a definition does nothing. `@Component` without a scan/`@Import` is equally invisible.

> [!tip] Interview answer
> XML, Java `@Configuration`/`@Bean`, stereotype scan, Groovy, and programmatic registration — mixable. Annotation **injection** is not a fourth way to **define** the context. Java-centric + `@ImportResource` for leftover XML is the usual modern combination, not a unique style.
