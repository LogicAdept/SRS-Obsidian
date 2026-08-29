<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS

# How do you work effectively with the Spring framework?

> [!abstract] Short answer
> Treat Spring as **infrastructure for POJOs**: let the **IoC container** create and inject objects, pick **only the modules** you need, and keep domain types free of container APIs. The overview’s design line is **choice** (swap a persistence provider in configuration), not one true architecture. For a new application, **Spring Boot** is the documented on-ramp (convention over configuration **on top of** the Framework — not a rename of it) ([[What is the Spring Framework]]). Day to day: **constructor injection**, Java-centric config, tests without a locator ([[How do you use dependency injection in practice]]).

## Use the container; do not fight it

**Start from the container.** Register beans (`@Component` / `@Bean` / XML) and depend on **interfaces**. `refresh()` builds the graph. `new` in a `@Service` for a collaborator, or `getBean` in business methods, is the Service Locator the DI chapter tells you to avoid.

**Stay modular.** You can run IoC under another web stack, or use JDBC/ORM/tx without MVC. Pulling every Spring jar “because it is Spring” fights the design.

**Stay non-invasive.** Domain logic should not implement `ApplicationContextAware` for routine wiring. Cross-cutting concerns (`@Transactional`, security, retries) go through **AOP proxies** — call through the injected reference, not `this`, or extract another bean.

**Pick a configuration entry point and mix on purpose.** `@Configuration` + scan for types you own; `@Bean` for types you do not; XML namespaces via `@ImportResource` when they are still the cleanest API ([[Which Spring configuration style do you prefer XML Java or annotations and why]]). The Framework does not crown a single winner.

**Prefer constructors for required deps.** Immutable, non-null, fully initialized; a huge constructor is a smell. `@Autowired` is optional on a single constructor.

**Know the version.** Framework **6+** is **Java 17+** and **`jakarta.*`**. Copy-pasting `javax.servlet` is not a DI bug.

**Test the POJO.** `new InvoiceService(fakeRepo)` for unit tests; `spring-test` when you need a context.

```java
@Service
public class SettlementService {

    private final Ledger ledger;

    public SettlementService(Ledger ledger) {
        this.ledger = ledger;
    }
}
```

**Listing 1.** Conceptual. Effective use is a constructor-injected POJO the container instantiates — not a class that reaches into the factory.

```d2
direction: down
you: "your types (POJOs)" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
ioc: "IoC + chosen modules" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
boot: "Boot (optional on-ramp)" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}

you -> ioc
boot -> ioc
```

**Fig. 1.** Boot and extra projects sit on the Framework. Effective work is still POJOs plus the container.

> [!warning] “Spring” is several products
> Answering with only Boot auto-config, or only XML from 2008, misses the **project** in play. Name Framework vs Boot vs Data vs Security.

> [!warning] Using every extension is not “being thorough”
> Circular constructor graphs, field injection to hide cycles, and `AopContext.currentProxy()` are documented **escapes**, not the happy path. Refactor first.

> [!tip] Interview answer
> I work with Spring by writing POJOs, constructor-injecting interfaces, and letting the ApplicationContext wire them. I take only the modules I need, start new apps with Boot, and keep domain code off the container APIs. Tests new the class with fakes; I do not look up beans in business logic.
