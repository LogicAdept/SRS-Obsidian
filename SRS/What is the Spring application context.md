<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is the Spring application context?

> [!abstract] Short answer
> **`ApplicationContext`** is the **interface that represents the Spring IoC container** in almost every app: it **instantiates, configures, and assembles beans** from configuration metadata (XML, annotations, Java `@Configuration`) ([[What is a Spring bean]]). It **extends `BeanFactory`** (`ListableBeanFactory`, `HierarchicalBeanFactory`) and adds **resources**, **events**, **i18n (`MessageSource`)**, **`Environment`**, parent/child hierarchy, and **automatic** post-processor registration ([[What is the difference between BeanFactory and ApplicationContext]]). It is **read-only while running** (some implementations can **reload**). You program to this interface; you `new` a concrete type or let Boot pick one ([[Which ApplicationContext implementations are commonly used]]). Prefer **constructor injection** over `getBean`.

## The container you actually start

IoC-chapter Container Overview: `org.springframework.context.ApplicationContext` **is** the container responsible for the bean graph. After it is **created and initialized** (`refresh()`), you have a configured system. Javadoc: central **configuration** for an application. Also a **complete superset** of `BeanFactory` — this chapter describes the container **as** an `ApplicationContext`.

```java
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
InvoiceService invoices = ctx.getBean(InvoiceService.class);
```

**Listing 1.** Conceptual. The `Class` constructor **`refresh()`es** immediately. `getBean` is for **bootstrap / tests**; business types should **declare** collaborators ([[What is the difference between inversion of control and ApplicationContext]]).

Javadoc capabilities:

- **Bean factory** access (`getBean`, by-type listing)
- **Resource** loading (`ResourceLoader` / `ResourcePatternResolver`)
- **Event** publication (`ApplicationEventPublisher`) ([[How does ApplicationContext publish events]])
- **Messages** (`MessageSource`) ([[What is MessageSource in Spring]])
- **Parent context** — child definitions **override**; lookup walks **up** (classic: one root + a child per `DispatcherServlet`)

It also **detects** `ApplicationContextAware` / `ResourceLoaderAware` / `ApplicationEventPublisherAware` / `MessageSourceAware`. `ConfigurableApplicationContext` adds **`refresh()` / `close()`** ([[What is the difference between close and refresh on ApplicationContext]]). `getAutowireCapableBeanFactory()` is for applying the lifecycle to objects **born outside** the context — not everyday DI.

```d2
direction: down
meta: "XML / @Configuration / scan" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
ac: "ApplicationContext\n(IoC container)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
beans: "beans + events + messages" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

meta -> ac: refresh
ac -> beans
```

**Fig. 1.** Metadata in; managed graph out. Boot still **is** this type (`SpringApplication` chooses a subclass) ([[What ApplicationContext type does Spring Boot create for a web app]]).

Web apps often never `new` a context in `main`: `ContextLoaderListener` / `DispatcherServlet` or Boot’s embedded servlet context start it. Several contexts may exist; there is no “one per JVM” rule.

> [!warning] `ApplicationContext` is not a class you subclass in application code
> It is an **interface**. Pick `AnnotationConfigApplicationContext`, `ClassPathXmlApplicationContext`, a `WebApplicationContext` implementation, or Boot’s type. `GenericApplicationContext` usually **cannot** `refresh()` twice.

> [!warning] The context is not “all objects in the JVM”
> Only **beans**. DTOs you `new` in a DAO, servlet API objects, and most domain entities are **not** in the context unless you registered them.

> [!tip] Interview answer
> The Spring application context is the IoC container interface: it reads configuration, creates and wires beans, and adds events, messages, resources, and a parent hierarchy on top of BeanFactory. I start it with AnnotationConfigApplicationContext or Spring Boot. I inject collaborators instead of calling getBean from business code.
