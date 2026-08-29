<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Annotations #Java/Spring/Core/IoC/Configuration #SRS

# What is the difference between Bean and Component in Spring?

> [!abstract] Short answer
> **`@Component` (2.5)** is a **type** stereotype: the **annotated class** is a scan candidate; the container **constructs that class** ([[How do you create a bean in Spring]]). **`@Bean` (3.0)** is a **method** that **produces** an object you `new` and configure in the method body — the Java equivalent of XML `<bean>`. Typical home for `@Bean` is a **`@Configuration`** class (third-party types, `DataSource`, custom `RestClient`). `@Bean` on a **`@Component`** is legal **lite** mode: a bonus factory, **no** CGLIB inter-bean calls ([[What is lite Bean mode versus full Configuration in Spring]]). Neither word is the live instance; that is just a **bean** ([[What is a Spring bean]]).

## Who instantiates what

`@Component` (and `@Service` / `@Repository` / `@Controller`) means “this type is eligible for autodetection.” Default bean **name** is the decapitalized simple class name. You need `@ComponentScan`, `scan()`, XML component-scan, or `@Import` of that class ([[What is the difference between a Spring configuration class and a component class]]).

`@Bean` means “this **method** instantiates, configures, and initializes a container-managed object.” Default bean **name** is the **method** name (`name` / `value` can set aliases; then the method name is **not** a name). Scope / profile / lazy / primary are **companion** annotations (`@Scope`, `@Profile`, …), not `@Bean` attributes. `initMethod` / `destroyMethod` (destroy may be **inferred** as `close` / `shutdown`) live on `@Bean`.

```java
@Component
public class BillingService { /* container: new BillingService(...) */ }

@Configuration
public class InfraConfig {
	@Bean
	DataSource dataSource() { // you construct a type you do not own
		return new HikariDataSource();
	}
}
```

**Listing 1.** Conceptual. Scan builds `billingService`. `dataSource()` is a factory method; full `@Configuration` intercepts sibling `@Bean` calls.

| | **`@Component`** | **`@Bean`** |
| --- | --- | --- |
| Target | Type | Method |
| Instantiates | The annotated class | Whatever the method **returns** |
| Typical for | Your application types | Library types / multi-step setup |
| Name default | Class → decapitalized | Method name |
| XML cousin | `<context:component-scan>` | `<bean>` |

```d2
direction: down
scan: "@ComponentScan" {
  width: 180
  height: 36
  style.fill: "#e8f5e9"
}
cmp: "@Component class\n= that instance" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
cfg: "@Configuration" {
  width: 180
  height: 36
  style.fill: "#fff3e0"
}
bean: "@Bean method\n= returned object" {
  width: 200
  height: 50
  style.fill: "#f3e5f5"
}

scan -> cmp
cfg -> bean
```

**Fig. 1.** Two registration paths. A stereotype on a class is **not** a `@Bean` method; a `@Bean` method is **not** a stereotype.

Lite `@Bean` on `@Component`: container treats the method like XML `factory-method`. Calling another `@Bean` method is a **plain Java** call. BFPP/BPP-returning `@Bean` methods should be **`static`**.

> [!warning] Do not “replace `@Component` with `@Bean`” on the class
> `@Bean` is **not** valid on a type. Writing `@Bean` on a service class does not register it. Putting `@Bean` methods on that `@Component` does not turn it into full `@Configuration`.

> [!warning] Two beans, two names
> `@Component` `InvoiceService` → id `invoiceService`. `@Bean InvoiceService invoiceService()` on a config is the **same default id** — a clash if both are registered. `@Bean({"b1","b2"})` **drops** the method name as an alias.

> [!tip] Interview answer
> @Component marks my class for scanning; Spring constructs it. @Bean marks a factory method, usually on @Configuration, where I construct objects I do not own. @Bean on a @Component is lite mode — no intercepted inter-bean calls. I do not confuse either annotation with the word bean meaning a managed instance.
