<!--
reps: 0
priority: 0
-->
#Java/Servlet/Context #SRS

# How would you explain ServletContext in Java web applications?

> [!abstract] Short answer
> **`ServletContext` is one web application’s view of itself** inside the container: **one instance per deployed app** (per JVM if the app is distributed). It is rooted at the **context path**. From it you **log**, read **context init parameters**, share **application-wide attributes**, look up **static resources**, and obtain **dispatchers**. Get it from **`ServletConfig.getServletContext()`** (or `GenericServlet` / `FilterConfig` / `HttpSession` / a context event). Per-servlet setup is **`ServletConfig`**, not this object: [[What is the difference between ServletContext and ServletConfig]]. Config API: [[How would you explain ServletConfig in the servlet API]]. App layout: [[How do you write a web application in Java]]. Files: [[How do you get the real filesystem path of a servlet on the server]]. Sessions are a **different** scope: [[How would you explain HTTP sessions in servlet based applications]].

## One context per web application

The container implements `ServletContext`. Every servlet, filter, and listener in that WAR talks to the **same** object (on this JVM). **Virtual hosts** do not share contexts. A **distributed** app has **one `ServletContext` per JVM**; **attributes are not a cluster store** — use a session, a database, or an EJB.

**Init parameters.** `web.xml` `<context-param>` (or equivalent) → `getInitParameter` / `getInitParameterNames`. These are **application** setup (admin mail, a system name), not a servlet’s `<init-param>`. EL `${initParam}` is this map.

**Attributes.** `setAttribute` / `getAttribute` / `removeAttribute`: any servlet in this app can see them. Same concurrency story as other shared maps: the container does not make your **values** thread-safe.

**Static resources.** `getResource` / `getResourceAsStream` take a path starting with `/`, relative to the **document root** or `META-INF/resources` inside `WEB-INF/lib` JARs (root wins). They return **bytes/URL of the file**, not executed JSP. `getRealPath` may be **`null`** if there is no local file. Private work dir: attribute **`jakarta.servlet.context.tempdir`** (`java.io.File`).

**Wiring at startup.** `addServlet` / `addFilter` / `addListener` / `addJspFile` and session/encoding setters run only during **application init** (`ServletContainerInitializer.onStartup` or a **declared** `ServletContextListener.contextInitialized`). A listener that was not declared/`@WebListener` gets **`UnsupportedOperationException`** on those methods.

**Also on the context:** `getRequestDispatcher`, `getNamedDispatcher`, `getContext` (another app), `log`, `getServerInfo` / version / `getVirtualServerName`, `getJspConfigDescriptor`.

```d2
direction: down
app: "web application / WAR" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
ctx: "ServletContext\ncontext path + attributes" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
s1: "servlet A" {
  width: 120
  height: 36
  style.fill: "#e8f5e9"
}
s2: "servlet B" {
  width: 120
  height: 36
  style.fill: "#e8f5e9"
}
app -> ctx
ctx -> s1
ctx -> s2
```

**Fig. 1.** Servlets share one context. They do not share another app’s context.

```java
// Conceptual — jakarta.servlet, Servlet 6.1
ServletContext ctx = getServletContext();
String mail = ctx.getInitParameter("adminEmail");
ctx.setAttribute("bootTime", Instant.now());
try (InputStream in = ctx.getResourceAsStream("/WEB-INF/defaults.properties")) {
    // static resource, not a dispatched JSP
}
```

**Listing 1.** Context params and attributes are **application** scope. Use `RequestDispatcher` when you need **dynamic** output.

> [!warning] Not `ServletConfig`, not a session
> `getInitParameter` on the **servlet** is `<init-param>`. On the **context** it is `<context-param>`. Context attributes survive across requests and users; **`HttpSession`** does not. In a cluster, do not put “the” cache on `ServletContext` and expect every node to see it.

> [!warning] `getResource("/index.jsp")` is the source
> You get the **JSP text**, not HTML. `WEB-INF` is visible to these methods and **not** to the client. Reloading must keep the app on **one class loader**; the temp directory is **per context** and **not** shared.

> [!tip] Interview answer
> ServletContext is the web application object: one per deployed app on this JVM, keyed by the context path. I use it for context-param, application attributes, static resources, logging, and dispatchers. It is not ServletConfig and it is not a distributed cache; sessions and databases are how you share across JVMs.
