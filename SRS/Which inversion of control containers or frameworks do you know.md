<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/IoC #Java/Spring/Core/IoC #Career/Experience #Java/JavaEE #SRS

# Which inversion of control containers or frameworks do you know?

> [!abstract] Short answer
> Name **DI containers**, not every product with the word “container.” Day-to-day: **Spring** — `BeanFactory` is the root API; **`ApplicationContext` is the container you actually start** ([[What is the Spring inversion of control container]], [[What is the difference between BeanFactory and ApplicationContext]]). Also know **Jakarta CDI** (typesafe injection **plus** lifecycle **contexts**; the spec’s runtime is **the CDI container**) and **Guice** (`Injector` + `Module`, constructor `@Inject`). Spring **does not implement CDI**; it **understands** `jakarta.inject` / JSR-330. **Tomcat and an EJB container are not this list** ([[How does a Spring IoC container differ from a web container or EJB container]]). Only claim what you have **run**; the rest is **literacy**.

## Products vs principle

**IoC** here means a runtime that **creates objects and injects collaborators** (Spring: IoC **is also known as DI**) — not a servlet engine ([[What is the difference between dependency injection and inversion of control]]).

| Name | What it is | How you start it |
|---|---|---|
| **Spring IoC** | Library: `BeanFactory` / `ApplicationContext`, beans from XML / `@Configuration` / scan | `AnnotationConfigApplicationContext`, Boot `SpringApplication`, `ContextLoaderListener` |
| **Jakarta CDI** | **Specification**: typesafe DI, **contextual** lifecycle, interceptors/events; implemented by an EE server (or a CDI Lite environment) | The **platform container**, not `new ApplicationContext` |
| **Guice** | Library: bind types in a `Module`, `Guice.createInjector`, `injector.getInstance` | Explicit `Injector` |
| **PicoContainer** | Small by-type container; Spring’s `autowireByType` javadoc still compares that “exactly one bean of the type” default to PicoContainer | Historical / niche |

```java
ApplicationContext spring = new AnnotationConfigApplicationContext(AppConfig.class);
InvoiceService invoices = spring.getBean(InvoiceService.class);

Injector guice = Guice.createInjector(new BillingModule());
BillingService billing = guice.getInstance(BillingService.class);
```

**Listing 1.** Conceptual. Same DI idea: **push** collaborators. Different **bootstrap types**. CDI looks like `@Inject` on a **contextual bean** inside an EE/CDI container — not this `main`.

JSR-330 **`@Inject` / `@Named`** are **annotations**, not a container. Spring and Guice (and CDI) **read** them. Using `@Inject` in Spring is **not** “I used CDI.”

```d2
direction: down
di: "DI / IoC containers" {
  width: 220
  height: 36
  style.fill: "#e8f5e9"
}
spring: "Spring ApplicationContext" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
cdi: "Jakarta CDI container" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
guice: "Guice Injector" {
  width: 180
  height: 40
  style.fill: "#f3e5f5"
}
not: "Servlet / EJB containers\n(different contracts)" {
  width: 260
  height: 44
  style.fill: "#ffebee"
}

di -> spring
di -> cdi
di -> guice
```

**Fig. 1.** Interview map. Servlet and EJB columns can **host** Spring; they do **not** replace `ApplicationContext` ([[What is Jakarta EE Spring]]). Locator / `getBean` in business code is IoC-shaped but **not** DI ([[Which methods can implement inversion of control]]).

> [!warning] “I know IoC containers” ≠ Tomcat
> A **web container** owns HTTP and servlets. An **EJB container** owns enterprise beans, JNDI, CMT. Spring IoC **wires POJOs** and can **run inside** those processes. Mixing the three is the usual fail.

> [!warning] Do not pad the list
> Naming Weld, Dagger, HK2, PicoContainer, and Avalon without **one** concrete fact (bootstrap type, spec vs library) sounds like a blog index. Prefer **Spring in depth** plus **CDI vs Guice vs Spring** in one sentence each. `@Inject` in a Boot app is still **Spring**.

> [!tip] Interview answer
> I use Spring’s ApplicationContext as the IoC container: BeanFactory underneath, beans from configuration metadata, constructor injection. I distinguish that from Tomcat and from an EJB container. I know Jakarta CDI as the EE typesafe DI-and-context spec — not the same as Spring reading jakarta.inject — and Guice as Injector plus modules. I only claim production experience for the ones I have actually started.
