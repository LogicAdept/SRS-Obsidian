<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# Which methods can implement inversion of control?

> [!abstract] Short answer
> **IoC** means the container — not the object — controls how dependencies are obtained. Common mechanisms: **dependency injection** (Spring's default), **Service Locator**, **factory-based creation** (factory methods / `FactoryBean`), and **contextualized lookup** (runtime `getBean`, `ObjectProvider`, `@Lookup`).

## Four IoC mechanisms (Spring lens)

| Mechanism | Who resolves the dependency | Spring example |
|---|---|---|
| **Dependency injection** | Container pushes collaborators in at creation | Constructor / setter / `@Autowired` — [[Which dependency injection styles do you know]] |
| **Service Locator** | Object asks a registry for a service | `ServiceLocatorFactoryBean`; contrasted with DI in Spring's IoC intro |
| **Factory pattern** | A factory (often container-managed) creates the object | `@Bean` methods, XML `factory-method`; args are container-supplied deps |
| **Contextualized lookup** | Object pulls a bean from the **current context** when needed | `ApplicationContext.getBean()`, `ObjectProvider`, `@Lookup` |

Spring's IoC introduction states that **DI is a specialized form of IoC**: dependencies arrive via constructor args, factory-method args, or properties — the inverse of the bean locating them itself through **direct `new`** or the **Service Locator** pattern.

## Dependency injection — the preferred path

The container **creates** the bean and **injects** collaborators. The bean does not look up types or locations. This is what `@Component` scanning, XML `<bean>`, and `@Configuration` `@Bean` methods configure.

Spring recommends **constructor injection** for required dependencies — [[Why is constructor injection preferred in Spring]].

## Factory-based creation

When construction is non-trivial, a **factory method** (static or on a `@Configuration` class) still receives dependencies as **method arguments** the container resolves — same DI idea, different creation hook.

`FactoryBean` goes further: a Spring bean whose **`getObject()`** produces the object callers actually need (e.g. proxies, JNDI resources).

## Service Locator vs contextualized lookup

Both involve **the object asking** for a dependency, but they differ in coupling:

- **Service Locator** — a dedicated registry API (`ServiceLocatorFactoryBean` maps an interface to bean names).
- **Contextualized lookup** — query the **active `ApplicationContext`** for a bean when the dependency's **scope or lifecycle** does not fit a single injection point (prototype inside singleton).

Spring's method-injection docs show the naive form — `ApplicationContextAware` + **`getBean("command")`** — and call it **undesirable** because business code couples to the framework. Cleaner variants: **`@Lookup`**, **`ObjectProvider.getObject()`**, scoped proxies — [[What is ObjectProvider and a scoped proxy in Spring]].

```d2
direction: right
di: "Dependency\ninjection" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
loc: "Service Locator\n/ lookup" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
factory: "Factory method\n/ FactoryBean" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
container: "IoC container\n(ApplicationContext)" {
  width: 160
  height: 50
  style.fill: "#fce4ec"
}
bean: "Your bean" {
  width: 120
  height: 50
  style.fill: "#f3e5f5"
}

container -> di -> bean: "push deps"
container -> factory -> bean: "create via factory"
bean -> loc -> container: "pull when needed"
```

**Fig. 1.** Push (DI), create-via-factory, and pull (locator / contextual lookup) are all ways to invert control of dependency acquisition.

> [!warning] Lookup is a last resort
> Prefer **constructor injection**. Use **contextualized lookup** only when lifecycle mismatch forces it (prototype per call, scoped beans) — not as a default substitute for DI.

> [!tip] Interview answer
> DI (constructor/setter/factory-method args), Service Locator, factory-based creation, and contextualized lookup from the ApplicationContext. Spring implements IoC primarily through DI; Service Locator and getBean-style lookup are alternatives Spring documents but generally discourages for normal collaborators.
