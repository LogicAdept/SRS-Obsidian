<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# When is Java configuration preferable to annotation-based configuration?

> [!abstract] Short answer
> When you want **Spring metadata off the application class**. **Annotation-based** config (2.5+) **moves wiring onto the type** — `@Component` / stereotypes, `@Autowired` on fields and methods — which is **short** but **decentralized**, and the class is **no longer an unaware POJO**. **Java configuration** (3.0+, `@Configuration` + `@Bean`) keeps those annotations on a **definition factory** and constructs the target with **`new` in a method**, **without touching** the component’s source. Prefer **`@Bean`** for **types you do not own**, for **central** infrastructure, and when **explicit construction** matters. Prefer **stereotypes + scan** for **your** application types when **wiring next to the class** is the point ([[What configuration styles exist in Spring]], [[What is the difference between a Spring configuration class and a component class]]).

## On the class vs outside the class

The annotation-config FAQ is **“it depends.”** Concise **on-type** annotations versus **central** XML. JavaConfig is the documented **third** option: annotations **without** editing the target ([[Which Spring configuration style do you prefer XML Java or annotations and why]]).

| | **Annotation-based** | **Java `@Configuration`** |
|---|---|---|
| Where metadata lives | On the **component** (`@Service`, `@Autowired`) | On a **config class** (`@Bean` methods) |
| Registers the type? | **Scan** / `@Import` of that class | **`@Bean` return value** (or you scan the config class itself) |
| Target source | **Annotated** | **Untouched** (you `new` it) |
| Control | **Scattered** across packages | **One (or few) factories** |
| Typical use | Types **you write** | **Libraries**, `DataSource`, multi-step setup |

```java
@Service // annotation-based: this class is the bean
public class BillingService {
	public BillingService(InvoiceRepository invoices) { /* … */ }
}

@Configuration // Java config: BillingService stays a plain type
public class AppConfig {
	@Bean
	BillingService billingService(InvoiceRepository invoices) {
		return new BillingService(invoices);
	}
}
```

**Listing 1.** Conceptual. Same runtime bean. Left: stereotype on the implementation. Right: factory **outside** — required when you **cannot** or **will not** annotate `BillingService`.

`@Autowired` **alone** is not a definition style: processors from `annotation-config` / `AnnotationConfigApplicationContext` inject **existing** beans ([[What does context annotation-config register]]). `@Bean` **creates** the definition ([[What is the Spring Bean annotation]]).

```d2
direction: down
ann: "annotation-based\n@Service + @Autowired on the type" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
java: "Java config\n@Configuration @Bean new Target()" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
mix: "usual mix: scan your types, @Bean the rest" {
  width: 300
  height: 44
  style.fill: "#e3f2fd"
}

ann -> mix
java -> mix
```

**Fig. 1.** Documented Java-centric mix: stereotypes for **yours**, `@Bean` for **theirs**. That mix is not “I prefer annotations” as one bucket.

Prefer **Java config** when the class is **third-party**, when a **single place** must show every infrastructure bean, when construction is **too rich** for “put `@Component` on it,” or when tests should **`new` the type** with **zero** Spring annotations on it. Prefer **annotation-based** when the team wants **discoverable** services and **constructor injection on the type itself** — fewer config classes, wiring **next to** the code.

> [!warning] Three features share the word “annotation”
> `@Autowired` on an XML/`@Bean` instance, `@Component` **scan**, and `@Bean` on `@Configuration` are **not** one switch. Answering “I prefer annotations over Java config” usually **collapses** the last two.

> [!warning] `@Bean` on a `@Service` is not Java configuration
> That is **lite** `@Bean` on a component whose **primary** job is the service. Inter-`@Bean` calls are **not** intercepted. Put factories on **`@Configuration`** if the point was a **definition class** ([[What is lite Bean mode versus full Configuration in Spring]]).

> [!tip] Interview answer
> Annotation-based config puts Spring on the class: short, but decentralized, and the type is no longer a plain POJO. Java configuration is preferable when I must not touch that class — third-party types, a central factory, or explicit new-and-setup in a @Bean method. I still scan my own @Service types and use @Bean for infrastructure. Mixing is the documented default, not a contradiction.
