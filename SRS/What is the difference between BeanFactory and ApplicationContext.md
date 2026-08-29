<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is the difference between BeanFactory and ApplicationContext?

> [!abstract] Short answer
> **`BeanFactory`** is the **root container API**: named `BeanDefinition`s, `getBean`, scopes, parent factories ([[What is the difference between BeanFactory and FactoryBean]]). **`ApplicationContext` extends it** (`ListableBeanFactory`, `HierarchicalBeanFactory`) and **adds** enterprise services: **automatic** `BeanPostProcessor` / `BeanFactoryPostProcessor` registration, **`MessageSource`**, **event publication**, **integrated `Lifecycle`**, plus `Environment` and resource loading. Official advice: **use an `ApplicationContext`** (`GenericApplicationContext` / `AnnotationConfigApplicationContext`) unless you need raw control. A plain `DefaultListableBeanFactory` does **not** detect post-processors, so `@Autowired` and AOP **stay off** until you register them yourself. Boot always starts an `ApplicationContext` ([[What ApplicationContext type does Spring Boot create for a web app]]).

## Same `getBean`, different bootstrap

`ApplicationContext` **includes all `BeanFactory` functionality**. Application code should **push** collaborators (constructors), not pull `getBean`. The BeanFactory API is for **framework integration**; `DefaultListableBeanFactory` is the delegate **inside** `GenericApplicationContext`.

```java
BeanFactory factory = new AnnotationConfigApplicationContext(AppConfig.class);
InvoiceService invoices = factory.getBean(InvoiceService.class);
```

**Listing 1.** Conceptual. An `ApplicationContext` **is** a `BeanFactory`. You almost never `new DefaultListableBeanFactory()` in an app ([[Which ApplicationContext implementations are commonly used]]).

| Feature (docs matrix) | `BeanFactory` | `ApplicationContext` |
| --- | --- | --- |
| Instantiate / wire beans | Yes | Yes |
| Integrated lifecycle (`Lifecycle` / start) | No | Yes |
| Auto-register `BeanPostProcessor` | No | Yes |
| Auto-register `BeanFactoryPostProcessor` | No | Yes |
| `MessageSource` (i18n) | No | Yes |
| `ApplicationEvent` publication | No | Yes |

“Integrated lifecycle” is **not** `InitializingBean` / `init-method` (those exist at factory level). It is context **start/stop** of `Lifecycle` / `SmartLifecycle` beans after `refresh()` ([[What is the difference between close and refresh on ApplicationContext]]).

**Eager vs lazy:** `ApplicationContext.refresh()` **pre-instantiates** non-lazy **singletons** so wiring errors fail at startup ([[How do you create a singleton Spring bean at application startup]]). A bare `DefaultListableBeanFactory` typically creates a singleton on **first** `getBean` unless you call `preInstantiateSingletons()`.

Without auto-detected processors, annotation injection and AOP proxies **do not run**. You must `addBeanPostProcessor` and invoke `BeanFactoryPostProcessor.postProcessBeanFactory` yourself — why the context variants exist ([[What is Spring BeanPostProcessor]]). `AnnotationConfigApplicationContext` registers the usual annotation processors for you.

```d2
direction: down
bf: "BeanFactory\ngetBean + definitions" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
ac: "ApplicationContext\n+ events, i18n, Environment,\nauto post-processors, Lifecycle" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

bf -> ac: "extends"
```

**Fig. 1.** Context is a factory **plus** convention-based extras. `FactoryBean` is an unrelated **bean type** inside either container.

> [!warning] `@Autowired` on a plain `BeanFactory` looks “broken”
> The XML/`@Bean` metadata can be fine. Post-processors were **never registered**. That is not a matching bug. Do not use deprecated `XmlBeanFactory` (removed); use a context.

> [!warning] Do not inject `BeanFactory` to look up collaborators
> That is a **service locator**. Inject the collaborator. `ApplicationContextAware` + `getBean` is the same smell. Prefer the context only for **events**, **messages**, or **resources** ([[How does ApplicationContext publish events]], [[What is MessageSource in Spring]]).

> [!tip] Interview answer
> BeanFactory is the IoC kernel: getBean and definitions. ApplicationContext extends it and auto-registers post-processors, so you get annotation config, AOP, events, and i18n without manual bootstrap. It also eagerly creates singletons at refresh. Boot and almost every app use an ApplicationContext. FactoryBean is a different interface that manufactures another object.
