<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Servlet #SRS

# What is the difference between `DispatcherServlet` and `ContextLoaderListener`?

> [!abstract] Short answer
> **`DispatcherServlet` is the HTTP front controller** (maps requests, runs interceptors, invokes handlers, resolves views or writes the body). **`ContextLoaderListener` is a `ServletContextListener`** that **starts and closes the root `WebApplicationContext`** and binds it to the `ServletContext`. The servlet’s context is typically a **child** of that root: services live in the root, web beans (`HandlerMapping`, controllers, `ViewResolver`) live in the child. A **single** `WebApplicationContext` is enough when you do not need the split.

## Two jobs, optional parent/child

`DispatcherServlet` javadoc: central dispatcher for HTTP handlers. Any number of them may exist; **each** loads its **own** namespace (mappings, handlers). Only the root context from `ContextLoaderListener`, **if any**, is shared.

`ContextLoader` (used by `ContextLoaderListener`): `initWebApplicationContext` / `closeWebApplicationContext` on servlet-context start and shutdown. The root is stored under **`WebApplicationContext.ROOT_WEB_APPLICATION_CONTEXT_ATTRIBUTE`**. If startup fails, that attribute can hold the **error**, not a context — look up with **`WebApplicationContextUtils`**.

Classic split: root = data sources, repositories, services; child = controllers and MVC strategy beans. Child **inherits** parent beans and may **re-declare** them. Parent does **not** see child beans. Lookup of the servlet’s context: `RequestContextUtils`. Types: [[What is a WebApplicationContext in Spring MVC]], [[What is the difference between ApplicationContext and WebApplicationContext]].

```java
public class MyWebAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {

    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class<?>[] { RootConfig.class };
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class<?>[] { WebConfig.class };
    }

    @Override
    protected String[] getServletMappings() {
        return new String[] { "/" };
    }
}
```

**Listing 1.** Conceptual Framework 7 pattern: root config for `ContextLoaderListener`, servlet config for `DispatcherServlet`. Java bootstrap: [[What is WebApplicationInitializer in Spring MVC]]. Front controller: [[What is the Front Controller pattern in Spring MVC]], [[What is Spring MVC DispatcherServlet]].

```d2
direction: down
sc: "ServletContext" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
cll: "ContextLoaderListener\nroot WebApplicationContext" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
ds: "DispatcherServlet\nchild WebApplicationContext" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
http: "HTTP request" {
  width: 180
  height: 50
  style.fill: "#fce4ec"
}

sc -> cll
cll -> ds: "parent"
http -> ds
```

**Fig. 1.** Listener owns the root lifecycle; the servlet owns request dispatch and (usually) a child context. Views in the child: [[What is a ViewResolver in Spring MVC]].

You can skip the hierarchy: `getServletConfigClasses()` returns **`null`** and all `@Configuration` goes through **`getRootConfigClasses()`**, or `web.xml` leaves the servlet’s `contextConfigLocation` empty.

Spring Boot does **not** hook `ContextLoaderListener` via `web.xml`. It starts a **`ServletWebServerApplicationContext`**, then registers `DispatcherServlet` from Spring config with the embedded container.

> [!warning] Injected servlet context may already have no parent
> `DispatcherServlet(WebApplicationContext)` sets the **root as parent only if the given context has none**. Boot’s single context is that case — do not assume two beans factories in every app.

> [!warning] Same bean name in the child hides the parent
> Inheritance is override, not merge. A `@Controller` accidentally scanned into the **root** is visible to every servlet; a service only in a **child** is invisible to another servlet.

> [!warning] Several `DispatcherServlet`s share one root
> Each servlet still has its own child. Shared infrastructure belongs in the listener-loaded root, not copied per servlet XML.

> [!tip] Interview answer
> **`DispatcherServlet` handles HTTP. `ContextLoaderListener` loads the root Spring context for the whole web app.** In the classic WAR layout the servlet context is a child: it sees services from the root; the root does not see controllers. Boot usually runs one `ServletWebServerApplicationContext` instead of that two-context `web.xml` story.
