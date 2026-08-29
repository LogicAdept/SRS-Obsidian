<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# What is the Spring Bean annotation?

> [!abstract] Short answer
> **`@Bean` (3.0)** marks a **method** that **instantiates, configures, and initializes** an object the container will manage — the Java equivalent of XML `<bean>`. You **write the `new` and setup** in the method body (third-party types, `DataSource`, multi-step construction). Default bean **name** is the **method** name (`name` / `value` set aliases; then the method name is **not** registered). Usual home is a **`@Configuration`** class so inter-`@Bean` calls go through the container. On a **`@Component`** (or `proxyBeanMethods = false`) it is **lite** mode: a plain factory — do **not** call sibling `@Bean` methods ([[What is lite Bean mode versus full Configuration in Spring]]). It is **not** `@Component` and not the word **bean** meaning the live instance ([[What is the difference between Bean and Component in Spring]], [[What is a Spring bean]]).

## Factory method, not a type stereotype

Java-based container: `@Bean` methods are a **central artifact** next to `@Configuration` ([[What annotations are used to configure a Spring application context]]). Method **parameters** are injection points (`InvoiceService invoiceService(InvoiceRepository repo)`). Scope, profile, lazy, primary, depends-on are **companion** annotations on the method — `@Bean` itself has **`name`**, **`initMethod`**, **`destroyMethod`**, `autowireCandidate`, and (6.2+) `defaultCandidate`. Destroy may be **inferred** as public no-arg `close` / `shutdown`; `destroyMethod = ""` turns that inference off.

```java
@Configuration
public class InfraConfig {

	@Bean
	DataSource dataSource(@Value("${app.jdbc-url}") String url) {
		HikariDataSource ds = new HikariDataSource();
		ds.setJdbcUrl(url);
		return ds;
	}

	@Bean
	InvoiceRepository invoiceRepository(DataSource dataSource) {
		return new JdbcInvoiceRepository(dataSource);
	}
}
```

**Listing 1.** Conceptual. Custom construction in the method. `invoiceRepository(DataSource)` takes a parameter instead of calling `dataSource()` — that style works in **full and lite** mode.

`@Bean({"b1", "b2"})` registers those names **only**. BFPP- and BPP-returning methods should be **`static`** so the `@Configuration` class is not initialized too early ([[What is Spring BeanPostProcessor]]). **`static @Bean`** is never CGLIB-intercepted.

```d2
direction: down
cfg: "@Configuration InfraConfig" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
m: "@Bean dataSource()" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
b: "DataSource bean in the factory" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}

cfg -> m -> b
```

**Fig. 1.** The annotation is on the **method**. The **bean** is the **return value** ([[How do you create a bean in Spring]]).

Lite `@Bean` on `@Component`: treated like XML `factory-method`; a Java call to another `@Bean` method is **not** `getBean`. Full `@Configuration` intercepts those calls so singleton (and other scopes) still hold.

> [!warning] `@Bean` is not valid on a class
> Dump “define components with custom logic” is the **use case**, not a substitute for `@Component`. Putting `@Bean` on `InvoiceService` does not register that class. Custom logic lives **in the factory method** that **returns** the instance.

> [!warning] Name clash with a scanned type
> `@Bean InvoiceService invoiceService()` and a scanned `@Service class InvoiceService` share the default id `invoiceService`. Two definitions of one name fail or override depending on `allowBeanDefinitionOverriding`. Rename the method or the stereotype `value`.

> [!tip] Interview answer
> @Bean marks a factory method, usually on @Configuration, where I construct an object Spring should manage — same role as a <bean> element. The default name is the method name. Parameters are injected. On a @Component it is lite mode: do not call other @Bean methods. It is not a stereotype on the application class itself.
