<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Spring/Framework/WebMvc #SRS

# What is the difference between `ApplicationContext` and `WebApplicationContext`?

> [!abstract] Short answer
> **`WebApplicationContext` is an `ApplicationContext`.** Every web context **is** an `ApplicationContext` (`BeanFactory`, `MessageSource`, events, resources, parent/child). The web subtype adds **`getServletContext()`**, **`ServletContextAware`**, and scopes **`request` / `session` / `application`**. A console app uses `AnnotationConfigApplicationContext` (or XML classpath context). A servlet app uses a `WebApplicationContext` implementation. It is **not** “REST vs desktop” and not “only `DispatcherServlet`”.

## Same container, web extras

`ApplicationContext` javadoc: listable bean factory, `ResourceLoader`, `ApplicationEventPublisher`, `MessageSource`, optional **parent**. Child definitions **override** the parent. That hierarchy description is exactly the classic web split: one parent for the app, a child per servlet.

`WebApplicationContext` javadoc: **extends** `ApplicationContext` and adds `getServletContext()`, root binding (`ROOT_WEB_APPLICATION_CONTEXT_ATTRIBUTE`), and `ServletContextAware`. Implementations must invoke `setServletContext` on those beans. Web scopes exist **in addition to** singleton/prototype.

| | `ApplicationContext` | `WebApplicationContext` |
| --- | --- | --- |
| Type | Interface | Subinterface |
| Typical class | `AnnotationConfigApplicationContext` | `AnnotationConfigWebApplicationContext` (web equivalent) |
| Servlet API | No | `getServletContext()` (may be `null` early in Boot) |
| Extra scopes | No | `request`, `session`, `application` |

```java
ApplicationContext standalone = new AnnotationConfigApplicationContext(AppConfig.class);

AnnotationConfigWebApplicationContext web = new AnnotationConfigWebApplicationContext();
web.register(WebConfig.class);
container.addServlet("dispatcher", new DispatcherServlet(web));
```

**Listing 1.** Conceptual: same `@Configuration` idea, different context class. Web type: [[What is a WebApplicationContext in Spring MVC]]. Who loads root vs servlet: [[What is the difference between DispatcherServlet and ContextLoaderListener]]. Java bootstrap: [[What is WebApplicationInitializer in Spring MVC]].

```d2
direction: down
ac: "ApplicationContext\nBeanFactory + i18n + events" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
wac: "WebApplicationContext\n+ ServletContext + web scopes" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}

ac -> wac: "extends"
```

**Fig. 1.** Inject `ApplicationContext` in a controller and you still have a web context at runtime — it is a `WebApplicationContext`. Cast or use `WebApplicationContextUtils` when you need the servlet context.

`*-servlet.xml` is only the **default XML location** for a `DispatcherServlet` namespace (`[servlet-name]-servlet`). Java config uses `AnnotationConfigWebApplicationContext`. The **root** context is often created by `ContextLoaderListener`, not by the servlet.

Spring Boot still uses these types: **`ServletWebServerApplicationContext` is a `WebApplicationContext`**. Auto-config hides the `web.xml` ceremony; it does not delete the interface.

> [!warning] `ApplicationContext` in a web app is usually already a `WebApplicationContext`
> Autowiring `ApplicationContext` does not give you a second, non-web container. Call **`getServletContext()`** only after a cast or a web-specific lookup.

> [!warning] Do not start `AnnotationConfigApplicationContext` inside a servlet
> That class is not a `WebApplicationContext`. Request-scoped beans and `ServletContextAware` will not bind. Use `AnnotationConfigWebApplicationContext` or Boot’s servlet context.

> [!warning] `getServletContext()` is `@Nullable`
> Especially during embedded-container startup (Boot). The method exists; the servlet context may not be attached yet.

> [!tip] Interview answer
> **`WebApplicationContext` extends `ApplicationContext` with the Servlet API and web scopes.** Stand-alone apps use a plain context class; web apps use a web context class (or Boot’s `ServletWebServerApplicationContext`). Hierarchy — root plus per-servlet children — is already an `ApplicationContext` feature; WAC is the web-typed implementation.
