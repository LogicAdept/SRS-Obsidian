<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Annotations #Java/Spring/Core/IoC/Configuration #SRS

# What is the difference between a Spring configuration class and a component class?

> [!abstract] Short answer
> A **`@Configuration` class** is a **source of bean definitions**: its **`@Bean` methods** are the Java form of `<bean>` elements, and **full** mode (default `proxyBeanMethods = true`) **CGLIB-subclasses** the type so calls between those methods go through the container ([[What is lite Bean mode versus full Configuration in Spring]]). A **component class** (`@Component` and stereotypes such as `@Service`) is a **scan candidate**: Spring **constructs that class** and manages **that instance**. `@Configuration` is **meta-annotated with `@Component`**, so a config class is *also* a bean — but its **primary purpose** is the extra `@Bean` factory methods, not “I am the service.” `@Bean` is a **method**; `@Component` is a **type**. They are not substitutes ([[What annotations are used to configure a Spring application context]]).

## Definition factory vs “this type is the bean”

Java-based container: central artifacts are `@Configuration` classes and `@Bean` methods. Annotating a class `@Configuration` means **primary purpose = bean definitions**. A component is only “this class is eligible for autodetection” ([[How do you create a bean in Spring]]).

```java
@Configuration
public class AppConfig {
	@Bean
	InvoiceRepository invoiceRepository() {
		return new JdbcInvoiceRepository(); // type you often do not own
	}
}

@Service
public class BillingService {
	private final InvoiceRepository invoices;
	public BillingService(InvoiceRepository invoices) { this.invoices = invoices; }
}
```

**Listing 1.** Conceptual. `AppConfig` is processed by `ConfigurationClassPostProcessor`: extra definitions from `@Bean`. `BillingService` **is** the bean; no factory method. Both can be found by `@ComponentScan` because `@Configuration` carries `@Component`.

`@Bean` **may** sit on a `@Component` (lite mode): a **bonus factory** on a type whose job is something else. Those methods must **not** call sibling `@Bean` methods; use **parameters**. `@Configuration(proxyBeanMethods = false)` is **behaviorally lite** despite the annotation name. Full `@Configuration` must be a **class** the container constructs, **non-final**, not a `@Bean`-produced instance.

Register a config with `AnnotationConfigApplicationContext(AppConfig.class)`, `@Import`, or a scan. A `@Component` without scan / `@Import` / `register` is **not** a bean. `@Import` can list **component classes** directly (since **4.2**) without a package scan ([[How does Import register beans in Spring]]).

```d2
direction: down
cfg: "@Configuration AppConfig\n(+ CGLIB in full mode)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
bean: "@Bean methods → other beans" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
cmp: "@Component BillingService\n(the instance is the bean)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

cfg -> bean
cfg -> cmp: "@ComponentScan / @Import"
```

**Fig. 1.** Config class **emits** definitions (including itself). Component class **is** a definition of its own type ([[What configuration styles exist in Spring]]).

`@Service` / `@Repository` / `@Controller` specialize **component** role, not configuration ([[What happens if you replace Service with Component or Repository on a service class]]). Putting `@Configuration` on a service to “make Spring see it” is the wrong stereotype: scan already sees `@Service`.

> [!warning] Dump asked `@Bean` vs `@Component`
> That is a **different** pair. `@Bean` **creates** some other object from a method. `@Component` **registers the annotated class**. A configuration class **uses** `@Bean`; a component class **is** `@Component`. You do not replace one with the other.

> [!warning] `@Bean` on `@Component` does not make it `@Configuration`
> Lite factories skip CGLIB. `otherBean()` is a plain Java call (second instance). Do not treat every class that has a `@Bean` method as a full configuration class.

> [!tip] Interview answer
> A configuration class is a definition factory: @Bean methods, CGLIB so inter-bean calls stay singletons. A component class is the bean itself, found by stereotype scanning. @Configuration is a @Component so it is scannable, but I still put application services on @Service and infrastructure factories on @Configuration. @Bean and @Component are not the same question.
