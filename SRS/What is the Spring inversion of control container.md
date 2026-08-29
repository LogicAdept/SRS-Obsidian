<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is the Spring inversion of control container?

> [!abstract] Short answer
> Spring’s **IoC container** is the runtime that **implements** inversion of control / **dependency injection**: objects **declare** collaborators; the container **creates** them, **injects** dependencies, and **manages lifecycle** from **configuration metadata**. The **root API** is **`BeanFactory`**. The type you almost always start is **`ApplicationContext`**, a **complete superset** (events, i18n, resources, auto post-processors) — the IoC chapter describes the container **as** that interface ([[What is the Spring application context]]). Managed objects are **beans**. It is a **library in the JVM**, not a servlet or EJB server ([[How does a Spring IoC container differ from a web container or EJB container]]).

## Packages `beans` + `context`

IoC introduction: `org.springframework.beans` and `org.springframework.context` are the basis. **`BeanFactory`** is an advanced configuration mechanism for **any** object. **`ApplicationContext` extends it** and is what this chapter uses exclusively. You feed it XML, annotations, or Java `@Configuration`; it produces a wired graph after **`refresh()`** ([[How does Spring work under the hood]]).

```java
ApplicationContext container = new AnnotationConfigApplicationContext(AppConfig.class);
InvoiceService invoices = container.getBean(InvoiceService.class);
```

**Listing 1.** Conceptual. `AnnotationConfigApplicationContext` **is** an IoC container. `getBean` is for bootstrap; application types should **declare** constructors ([[How would you explain dependency injection]]).

**Beans** are the backbone objects the container instantiates, assembles, and manages — not every Java object in the process ([[What is a Spring bean]]). Recipes are **`BeanDefinition`s** ([[What is Spring BeanDefinition]]). `FactoryBean` is a **plugin inside** the container, not the container ([[What is the difference between BeanFactory and FactoryBean]]).

```d2
direction: down
meta: "XML / @Configuration / @Component" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
bf: "BeanFactory (kernel)" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
ac: "ApplicationContext\n(usual IoC container)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

meta -> bf
bf -> ac: "extends"
```

**Fig. 1.** Same DI engine. Context adds enterprise extras and **auto-detects** processors ([[What is the difference between BeanFactory and ApplicationContext]]).

IoC **the principle** is not this object; the container **is how Spring runs that principle** ([[What is the difference between inversion of control and ApplicationContext]]). Boot still **starts an `ApplicationContext`**. Several containers may exist (root + servlet children).

> [!warning] “The Spring container” is not Tomcat
> Tomcat is a **web** container. Spring **may run inside** it (or Boot **embeds** it). CLI and WebFlux+Netty apps still have an IoC container **without** a servlet engine.

> [!warning] A raw `DefaultListableBeanFactory` is an IoC container with the lights off
> Without registering **`BeanPostProcessor`s**, `@Autowired` and AOP **do not run**. That is why apps use an **`ApplicationContext`**.

> [!tip] Interview answer
> Spring’s IoC container creates and wires beans from metadata so classes do not new their helpers. BeanFactory is the kernel API; ApplicationContext is the container I actually bootstrap. It is not a Java EE server and not the same thing as Tomcat. I inject collaborators instead of calling getBean in business code.
