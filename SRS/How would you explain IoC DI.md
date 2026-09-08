<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/IoC #Java/Spring/Core/IoC/DI #SRS

# How would you explain IoC DI?

> [!abstract] Short answer
> **Inversion of Control (IoC)** is the principle: an object does **not** control how its helpers are **created or located**. **Dependency injection (DI)** is Spring’s **specialized form** of that: the object **declares** collaborators (constructor, factory-method, or setter properties); the **IoC container injects** them when it creates the bean. That is the inverse of `new` or a **service locator** inside the bean. IoC is not “the container owns lifecycle” as a slogan — lifecycle is what the container **also** does for beans; the inversion is **who obtains dependencies**.

## Principle versus mechanism

Spring’s IoC chapter implements the **IoC principle**. In current wording, **DI is a specialized form of IoC**, not a synonym you should collapse in an interview. Older 4.x text said “IoC is also known as DI” for the **same injection process**. Keep both: IoC is the **idea**; DI is the **push** Spring uses ([[What is the difference between dependency injection and inversion of control]], [[How would you explain DI]]).

```d2
direction: down
ioc: "IoC principle\nobject does not locate helpers" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
di: "DI\ncontainer pushes constructor / setter" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
loc: "Service locator / getBean\nobject still pulls" {
  width: 260
  height: 55
  style.fill: "#ffebee"
}

ioc -> di
ioc -> loc
```

**Fig. 1.** Locator also moves some `new` out of the service, but the object **still pulls**. Prefer DI.

The **container** (`BeanFactory`, usually `ApplicationContext`) instantiates, assembles, and manages **beans** from configuration metadata. That includes lifecycle callbacks. Calling `getBean` from business code is a locator-shaped pull, not constructor DI ([[What is the Spring inversion of control container]], [[What is the difference between inversion of control and a service locator]]).

```java
public class InvoiceService {

	private final InvoiceRepository invoices;

	public InvoiceService(InvoiceRepository invoices) {
		this.invoices = invoices;
	}
}
```

**Listing 1.** Conceptual. `InvoiceService` does not construct or look up the repository. The container injects it — DI as IoC ([[How would you explain dependency injection]]).

Constructor injection is the usual Spring default for **required** collaborators (`final`, fully initialized). Setter injection is for **optional** deps. Constructor–constructor cycles fail at startup with `BeanCurrentlyInCreationException` ([[Why is constructor injection preferred in Spring]]).

> [!warning] Do not equate IoC with “Spring Map of beans”
> `ApplicationContext` is not “just `Map<id, Object>`”. It is a `BeanFactory` plus events, i18n, resources, and lifecycle. Beans are recipes (`BeanDefinition`) the container **creates**, not entries you stuff in by hand.

> [!tip] Interview answer
> IoC means the object does not decide how helpers are created or found. DI is how Spring usually does that: the container pushes constructor or setter dependencies when it builds the bean. Lifecycle management is the container’s job for beans; the inversion itself is who obtains collaborators — inject, do not look up.
