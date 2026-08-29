<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #Patterns/GoF #Patterns/Architecture/UI/MVC #SRS

# What design patterns does the Spring Framework use?

> [!abstract] Short answer
> Spring does not implement “one pattern.” The container documents **Singleton** and **Prototype** on `FactoryBean`/`BeanFactory`, **Observer** on context events, **Proxy** on AOP and scoped beans, and **Front Controller** on `DispatcherServlet` / `DispatcherHandler`. JDBC uses a **template class** with callbacks (`JdbcTemplate`). `FactoryBean.getObject()` is a factory in the container — not every bean is built that way. A Spring singleton is **per container**, not a JVM-wide GoF singleton.

## Patterns the docs actually name

**Factory / FactoryBean.** A `FactoryBean` is a bean that is itself a factory: the container exposes `getObject()`, not the factory instance (`getBean("&id")` returns the `FactoryBean`). Spring ships many (`ProxyFactoryBean`, `JndiObjectFactoryBean`, …). `getObject()` “allows support for both the Singleton and Prototype design patterns.” Most application beans are still plain classes created by the container — you do **not** write a `FactoryBean` for each type ([[What is the difference between BeanFactory and FactoryBean]]). `ServiceLocatorFactoryBean` builds a locator **proxy** so clients avoid calling `BeanFactory.getBean` (that lookup would violate IoC).

**Singleton vs Prototype.** Default bean scope is one instance **per IoC container** per bean definition — not the GoF “one per ClassLoader” singleton ([[How does a Spring singleton differ from the Gang of Four Singleton pattern]], [[Is a singleton Spring bean thread-safe]]). Prototype: a new instance per request for that bean.

**Observer.** `ApplicationContext` event publication to `ApplicationListener` / `@EventListener` is the standard Observer pattern ([[How does ApplicationContext publish events]]).

**Proxy.** `BeanPostProcessor`s may wrap the instance (AOP). Scoped beans injected into a longer-lived bean use an AOP **scoped proxy**. `ProxyFactoryBean` is a `FactoryBean` for AOP proxies ([[What is an AOP proxy in Spring]]).

**Front controller / MVC.** Spring MVC is designed around the **front controller** pattern: `DispatcherServlet` runs a shared algorithm and delegates mapping, adaptation, and views. WebFlux does the same with `DispatcherHandler`. `HandlerAdapter` exists so the dispatcher can invoke **any** handler interface without knowing the invocation details ([[What is Spring MVC DispatcherServlet]]).

**Template (JDBC).** `JdbcTemplate` is a thread-safe **template class**: it runs the JDBC workflow (connection, statements, exception translation) and leaves SQL and result extraction to callback interfaces (`PreparedStatementSetter`, `RowMapper`, …) ([[What is Spring JdbcTemplate]]).

`getBean(name)` is the container lookup API, not a documented “Simple Factory” type. `ApplicationContext` is the IoC / configuration facade, not a named “Context Object” pattern in the reference.

```java
public class Client {
    private final ApplicationEventPublisher events; // Observer publication
    private final JdbcTemplate jdbc;                // template + callbacks

    public Client(ApplicationEventPublisher events, JdbcTemplate jdbc) {
        this.events = events;
        this.jdbc = jdbc;
    }
}
```

**Listing 1.** Conceptual. Typical application code **uses** these abstractions; it does not reimplement the patterns.

```d2
direction: down
ioc: "BeanFactory / ApplicationContext" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
fb: "FactoryBean.getObject\nSingleton / Prototype" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
obs: "publishEvent\nObserver" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}
proxy: "AOP / scoped proxy" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}
mvc: "DispatcherServlet\nFront Controller" {
  width: 220
  height: 70
  style.fill: "#fce4ec"
}

ioc -> fb
ioc -> obs
ioc -> proxy
mvc -> ioc
```

**Fig. 1.** Container patterns sit under `BeanFactory` / `ApplicationContext`. Web MVC adds a front controller in front of that context.

> [!warning] Spring “singleton” ≠ GoF Singleton
> One shared instance **per container** (and you can register two bean definitions of the same class). Mutable fields are still shared across threads. Prototype injected into a singleton is still **one** captured instance.

> [!warning] `FactoryBean` is opt-in infrastructure
> `getBean("myService")` returns a normal bean, not `FactoryBean.getObject()`, unless that definition **is** a `FactoryBean`. Prefix `&` to ask for the factory itself. Do not describe every `getBean` as the Factory Method pattern.

> [!tip] Interview answer
> Spring uses several GoF ideas: the container’s default scope is a per-container singleton, FactoryBean can produce singleton or prototype objects, context events are Observer, and AOP plus scoped beans use proxies. Web MVC’s DispatcherServlet is a front controller that talks to HandlerAdapters. JdbcTemplate is a template that runs JDBC and calls your callbacks. None of that makes every bean a FactoryBean or a JVM-wide singleton.
