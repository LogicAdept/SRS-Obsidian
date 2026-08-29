<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/IoC #Java/Spring/Core/IoC/DI #SRS

# What is the difference between dependency injection and inversion of control?

> [!abstract] Short answer
> In Spring’s IoC chapter they **name the same process**: **“IoC is also known as dependency injection (DI).”** Objects **declare** collaborators (constructor args, factory-method args, or properties after construction); the **container injects** them when it creates the bean. That is the **inverse** of the bean doing `new` or a **service locator** lookup ([[How would you explain dependency injection]]). Interview split that still fits: **IoC** is the **principle** (the container, not the object, controls obtaining helpers); **DI** is the **push** mechanism Spring uses for that. Other IoC-shaped tricks (locator, `getBean`, `@Lookup`) are **not** DI ([[Which methods can implement inversion of control]]).

## Same process in the reference, two words in interviews

The inversion is **control of construction and location**. With DI, `InvoiceService` does not choose `JdbcInvoiceRepository`. The `ApplicationContext` does, from `BeanDefinition` metadata ([[What is Spring BeanDefinition]]). Traits: the bean is **passive**, does not know **where** or **which class**, and stays a **POJO** ([[How would you explain distinctive traits of dependency injection]]).

```d2
direction: down
ioc: "IoC principle\nobject does not locate helpers" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
di: "DI (Spring's usual mechanism)\ncontainer pushes constructor/setter" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
loc: "Service locator / getBean\nobject still pulls" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}

ioc -> di
ioc -> loc
```

**Fig. 1.** Spring **contrasts** DI with locator/`new`, even though both move some control out of `new` in the service. Prefer DI ([[What core ideas underpin the Spring Framework]]).

Spring’s **two major DI variants** are **constructor** and **setter** (plus factory-method arguments). Field and config-method `@Autowired` are extra injection points, not a third classic “interface injection” style ([[Which dependency injection styles do you know]]).

The **IoC container** (`BeanFactory` / `ApplicationContext`) is the runtime that **does** DI (and lifecycle, events, …). IoC is not “the Spring class named ApplicationContext” by itself, and it is **not** the Dependency Inversion Principle (depend on abstractions) — related design, different term.

```java
public class InvoiceService {
	private final InvoiceRepository invoices;
	public InvoiceService(InvoiceRepository invoices) {
		this.invoices = invoices; // DI: declared, not located
	}
}
```

**Listing 1.** Conceptual. Tests: `new InvoiceService(mockRepo)` — still DI, **no** container required.

> [!warning] Dump’s “three types” includes interface injection
> Spring does **not** document Pico/Avalon-style **interface injection**. Do not list it as a Spring DI mode. Constructor + setter are the documented pair; `@Autowired` on fields/methods is annotation injection on top.

> [!warning] “IoC relies on DI” reverses the usual wording
> DI **is** how this container implements IoC for collaborators. IoC as a **broader** idea can also be a locator or a template-method framework. Spring still calls the injection process **IoC / DI** and tells you **not** to `getBean` in business code.

> [!tip] Interview answer
> Spring’s docs treat IoC and DI as names for the container injecting constructor or setter dependencies — the inverse of new or a service locator. If they want a split: IoC is the principle that something else controls how you get collaborators; DI is the push style Spring uses. I do not call getBean DI, and I do not recite interface injection as a Spring feature.
