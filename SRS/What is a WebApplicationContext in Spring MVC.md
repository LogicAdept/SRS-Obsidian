<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Core/IoC #SRS

# What is a `WebApplicationContext` in Spring MVC?

> [!abstract] Short answer
> **`WebApplicationContext` is `ApplicationContext` for a web app:** it adds **`getServletContext()`**, web bean scopes **`request` / `session` / `application`**, and **`ServletContextAware`** callbacks. Contexts are **hierarchical**: one **root** per application (often from `ContextLoaderListener`) and a **child** per servlet (including each `DispatcherServlet`). The root is bound on the `ServletContext` as **`ROOT_WEB_APPLICATION_CONTEXT_ATTRIBUTE`**.

## IoC container with a `ServletContext`

`WebApplicationContext` javadoc (Spring Framework 7): still an `ApplicationContext` (`BeanFactory`, `MessageSource`, events, resources). Extra contract:

- **`getServletContext()`** — the Servlet API context.
- **`ServletContextAware`** beans get **`setServletContext`**.
- Well-known factory beans: **`servletContext`**, context init-params, context attributes (`SERVLET_CONTEXT_BEAN_NAME`, `CONTEXT_PARAMETERS_BEAN_NAME`, `CONTEXT_ATTRIBUTES_BEAN_NAME`). ServletConfig params **override** ServletContext params of the same name.

Lookup: **`WebApplicationContextUtils.getRequiredWebApplicationContext(ServletContext)`** for the root. During a request, `DispatcherServlet` also binds **its** context under **`DispatcherServlet.WEB_APPLICATION_CONTEXT_ATTRIBUTE`** (`RequestContextUtils`). Vs a console `ApplicationContext`: [[What is the difference between ApplicationContext and WebApplicationContext]].

```java
WebApplicationContext root =
        WebApplicationContextUtils.getRequiredWebApplicationContext(servletContext);
ServletContext sc = root.getServletContext();
```

**Listing 1.** Conceptual root lookup. Do not `getAttribute` yourself — on failed startup the attribute may be an **exception**, not a context.

```d2
direction: down
root: "Root WebApplicationContext\nservices, DataSource" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
child: "DispatcherServlet child\ncontrollers, HandlerMapping, ViewResolver" {
  width: 360
  height: 80
  style.fill: "#e8f5e9"
}
sc: "ServletContext\nROOT_WEB_APPLICATION_CONTEXT_ATTRIBUTE" {
  width: 360
  height: 70
  style.fill: "#e3f2fd"
}

sc -> root
root -> child: "parent"
```

**Fig. 1.** Child sees (and may override) root beans; root does not see child beans. Who creates which: [[What is the difference between DispatcherServlet and ContextLoaderListener]]. Front controller: [[What is Spring MVC DispatcherServlet]].

Typical child contents: `@Controller`s, `HandlerMapping`, `HandlerAdapter`, `ViewResolver`, `LocaleResolver`. Typical root: data sources, services. A **single** context is valid: put all `@Configuration` in the root and return **`null`** servlet config classes ([[What is WebApplicationInitializer in Spring MVC]]).

Boot’s embedded server uses **`ServletWebServerApplicationContext`**, a `WebApplicationContext` that starts the container itself — usually **one** context, not the classic WAR pair.

> [!warning] `getServletContext()` can still be null during Boot startup
> With an embedded container the `ServletContext` is attached **while** the context initializes. Do not assume it is ready in every `@Bean` method; wait for **`ApplicationStartedEvent`** or inject `WebApplicationContext` and read the servlet context later.

> [!warning] Web scopes are not on a plain `ApplicationContext`
> `"request"`, `"session"`, and `"application"` are extra scopes on a `WebApplicationContext`. They do not exist in a command-line `AnnotationConfigApplicationContext`.

> [!warning] Several servlets, one root
> Each `DispatcherServlet` still gets its **own** child. Shared infrastructure belongs in the root, not copied into every `*-servlet.xml`.

> [!tip] Interview answer
> **`WebApplicationContext` is the web `ApplicationContext`: `ServletContext` plus request/session/application scopes.** In a classic WAR the listener loads the root and each `DispatcherServlet` loads a child that can see those shared beans. Boot usually runs a single `ServletWebServerApplicationContext` instead.
