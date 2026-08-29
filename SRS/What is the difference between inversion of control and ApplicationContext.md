<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/IoC #Java/Spring/Core/IoC #SRS

# What is the difference between inversion of control and ApplicationContext?

> [!abstract] Short answer
> **Inversion of Control** is a **principle** (Spring also uses **IoC** as another name for **dependency injection**): the object does not `new` or look up collaborators; something **outside** supplies them ([[What is the difference between dependency injection and inversion of control]]). **`ApplicationContext`** is a **Spring type** — the usual **IoC container** you bootstrap (`refresh()`). It **extends `BeanFactory`** and adds events, i18n, `Environment`, auto-registered post-processors, and `Lifecycle` ([[What is the difference between BeanFactory and ApplicationContext]]). IoC is not a class. `ApplicationContext` is not “IoC itself”; it is **one container API** that **implements** that principle. `BeanFactory` is the **smaller** container API; both are IoC containers.

## Principle vs the object you `new`

Dump line “ApplicationContext is the implementation of IoC in Spring” is **close** and **too tight**. Spring’s IoC chapter describes a **process** (declare deps → container injects). That process runs inside a **container**. The client interface for the full container is `ApplicationContext`; the root is `BeanFactory`. Concrete contexts (`AnnotationConfigApplicationContext`, `ClassPathXmlApplicationContext`, Boot’s servlet/reactive subtypes) **implement** `ApplicationContext` ([[Which ApplicationContext implementations are commonly used]]).

```java
public class InvoiceService {
	public InvoiceService(InvoiceRepository invoices) { /* IoC/DI: declared */ }
}

ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
InvoiceService invoices = ctx.getBean(InvoiceService.class);
```

**Listing 1.** Conceptual. The **constructor** is the inversion. The **context** is the runtime that performed it. `new InvoiceService(mock)` in a unit test is still DI — **no** `ApplicationContext` required.

```d2
direction: down
prin: "IoC / DI principle" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
bf: "BeanFactory\n(kernel container)" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
ac: "ApplicationContext\n(BeanFactory + enterprise extras)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

prin -> bf: "implemented by"
bf -> ac: "extends"
```

**Fig. 1.** You almost always hold an `ApplicationContext`. You still **explain IoC** without naming that interface ([[How would you explain dependency injection]]).

`ApplicationContext` is also `MessageSource`, `ApplicationEventPublisher`, `ResourcePatternResolver`, `EnvironmentCapable`. Those extras are **not** the definition of IoC; they are why Spring recommends a context over a raw `DefaultListableBeanFactory`. Injecting `ApplicationContext` only to `getBean` **abandons** IoC style (service locator).

> [!warning] “IoC = ApplicationContext” fails the follow-up
> Then they ask what `BeanFactory` is. Answer: **also** an IoC container, without automatic processors / events / i18n. Or they ask you to unit-test without Spring: you still use constructor injection.

> [!warning] `ApplicationContext` is an interface
> You never “the ApplicationContext class.” You pick an **implementation** (or Boot does). `WebApplicationContext` is a **subtype** for web, not a second principle.

> [!tip] Interview answer
> Inversion of Control is the idea that the container injects what a bean needs instead of the bean creating or looking up helpers. ApplicationContext is Spring’s full IoC container interface: a BeanFactory plus events, messages, and auto post-processors. I use a context in the app; I do not call the principle ApplicationContext.
