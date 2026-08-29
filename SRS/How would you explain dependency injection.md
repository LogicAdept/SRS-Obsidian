<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/DI #SRS

# How would you explain dependency injection?

> [!abstract] Short answer
> **Dependency injection (DI)** is how Spring implements **Inversion of Control** for objects: a type **declares** what it needs (constructor arguments, factory-method arguments, or properties after construction) and **does not** `new` those collaborators or look them up. The **container** creates the graph and **injects** the dependencies when it creates the bean. Spring’s docs also call that process **wiring**. **Explicit** wiring names the other bean (`ref`, `<constructor-arg>`, `@Qualifier`); **autowiring** infers it by type or name. That is the **inverse** of the bean controlling location of its helpers (direct construction or a **service locator**).

## Who creates the collaborator?

Without DI, `InvoiceService` constructs `new JdbcInvoiceRepository()`. The service **owns** the choice of implementation, is hard to unit-test, and is coupled to JDBC.

With DI, `InvoiceService` only knows `InvoiceRepository`. Something **outside** — in Spring, the `ApplicationContext` reading `BeanDefinition` metadata — supplies the instance at creation time.

```d2
Locator: {
  S1: InvoiceService
  S1 -> "new JdbcRepo()": "service locates"
}
Injected: {
  Ctx: ApplicationContext
  S2: InvoiceService
  R: InvoiceRepository
  Ctx -> S2: creates
  Ctx -> R: creates
  Ctx -> S2: "injects R"
}
```

**Fig. 1.** Control of `new` moves to the container. The service still **uses** the repository; it no longer **chooses** it.

Spring’s IoC chapter uses **IoC** and **DI** as names for this same process. The **container** (`BeanFactory` / `ApplicationContext`) instantiates, configures, and assembles beans. You are not required to call `getBean` in business code ([[How do you use dependency injection in practice]]).

```java
public class InvoiceService {

	private final InvoiceRepository invoices;

	public InvoiceService(InvoiceRepository invoices) {
		this.invoices = invoices;
	}
}
```

**Listing 1.** The dependency is a constructor argument. Tests: `new InvoiceService(mockRepo)` with **no** Spring. A single constructor does not need `@Autowired` ([[Why is Autowired often omitted on a single constructor in modern Spring]]).

## Constructors, setters, and mixing

Official variants: **constructor-based** (including a **static factory method** with arguments) and **setter-based** (properties after a no-arg constructor/factory). You can **mix**: mandatory deps on the constructor, optional ones on setters. Annotation injection also covers **fields** and config methods — that is still DI, just a different injection **point** ([[Which dependency injection styles do you know]]).

The team **advocates constructors** for required collaborators: immutable fields, not `null`, object complete before any client sees it. A **long** constructor is a smell (too many responsibilities). Setters suit **optional** deps with defaults, or later reconfiguration (for example JMX). Third-party types may force one style (no setters → constructor only).

## Explicit wiring vs autowiring

Configuration metadata (`BeanDefinition`) is loaded first; `ref`s and property values are applied **when the bean is created**, not when XML or `@Configuration` is parsed ([[What is Spring BeanDefinition]]). Default singleton pre-instantiation makes many wiring mistakes fail at context startup.

**Explicit** wiring names the collaborator: XML `ref` / `<constructor-arg>`, `@Bean` method parameters you write by type, `@Qualifier`. An **inner bean** is also explicit: nested in the outer definition, not a shared id ([[What is a Spring inner bean]]).

**Autowiring** is still DI: XML `autowire="byType"` / `byName` / `constructor`, or `@Autowired` / `@Inject` processed by a `BeanPostProcessor`. Explicit `<property>` / `<constructor-arg>` **always override** XML autowire. Type-based autowire fails fast if two beans match ([[What are the limitations of XML autowiring in Spring]]).

## What DI is not

**Not** `@Autowired` — that is one **matching** API. XML `<constructor-arg>` / `<property>` and `@Bean` method parameters are DI too ([[How can you apply dependency injection with a Spring bean]]).

**Not** the Dependency Inversion Principle. DIP is a SOLID rule about depending on abstractions; DI is a **technique** that makes that easy. You can invert dependencies with `new` behind a factory; you can inject a concrete class. Spring does not make them the same word.

**Not** unique to Spring. Any code that passes collaborators in is DI; the container automates the graph.

> [!warning] Service locator is the other inversion
> `ctx.getBean(InvoiceRepository.class)` inside `InvoiceService` still inverts **who** finds the repo, but the class **depends on the container**. Official DI keeps those lookup APIs out of ordinary beans so tests construct the type with stubs.

> [!warning] Parsing `BeanDefinition`s is not wiring
> The container can accept the XML or `@Configuration` class and still fail later if a `ref` is missing, a constructor cycle exists, or a property is invalid — especially for lazy or non-singleton beans. Injection happens at populate time, not parse time.

> [!warning] Constructor cycles are unresolvable
> If A’s constructor needs B and B’s constructor needs A, the container throws `BeanCurrentlyInCreationException`. Setter injection can break that cycle; it is not recommended as a design. Prefer breaking the cycle in the model ([[How does Spring resolve circular dependencies]]).

> [!tip] Interview answer
> DI (Spring also says **wiring**): objects list collaborators as constructor/factory/property inputs; a container injects them at creation. Inverse of `new` or a locator. Explicit wiring names the other bean; autowiring infers by type or name. Prefer constructors for required deps; setters for optional. `@Autowired` is optional sugar, not the definition.
