<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Patterns/Architecture/UI/MVC #Java/Servlet #SRS

# What is the Front Controller pattern in Spring MVC?

> [!abstract] Short answer
> **One servlet owns the HTTP entry algorithm; handlers do the work.** Spring MVC’s front controller is **`DispatcherServlet`**: it maps, intercepts, invokes, and then renders a view or writes the body via **delegate beans**. `@Controller` methods are **not** front controllers. You still **map** that servlet to a URL pattern — it is not magically every request on the server.

## One dispatch algorithm, many handlers

Spring Framework *DispatcherServlet*: MVC is built around the **front controller pattern**. A central servlet provides a **shared request-processing algorithm**; **configurable delegates** (`HandlerMapping`, `HandlerAdapter`, `ViewResolver`, `HandlerExceptionResolver`, …) do the actual work. That is the opposite of a WAR full of `HttpServlet` subclasses, each mapped to its own path.

`DispatcherServlet` javadoc: **any number** of these servlets may exist. Each has its **own namespace** and child `WebApplicationContext`. Only the **root** context from `ContextLoaderListener` (if any) is shared. Child contexts see the root; the root does **not** see servlet-local beans.

```java
DispatcherServlet servlet = new DispatcherServlet(context);
ServletRegistration.Dynamic registration = servletContext.addServlet("app", servlet);
registration.setLoadOnStartup(1);
registration.addMapping("/app/*");
```

**Listing 1.** Conceptual Framework registration. Official examples often use **`/app/*`**, not `/`. The servlet: [[What is Spring MVC DispatcherServlet]]. Pattern vs container bootstrap: [[What is WebApplicationInitializer in Spring MVC]]. Hierarchy: [[What is the difference between DispatcherServlet and ContextLoaderListener]].

```d2
direction: down
http: "HTTP" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
filters: "Servlet filters\n(Security, …)" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
fc: "DispatcherServlet\nfront controller" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
h: "@Controller methods\nHandlerMapping / Adapter" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

http -> filters -> fc -> h
```

**Fig. 1.** Filters wrap the servlet. The front controller is inside the mapped servlet, not in front of the filter chain. Interceptors sit on the MVC chain: [[What is a HandlerInterceptor in Spring MVC]].

Annotated controllers may **write the response in the adapter** (`@ResponseBody`) instead of returning a view name. The pattern still holds: one servlet, many handlers.

> [!warning] Mapping is not “the whole host”
> Only URLs in **this servlet’s** `url-pattern` enter it. A second `DispatcherServlet` on `/api/*` is a **second** front controller with its own child context. Static files may go to the **default servlet** if you enable default-servlet handling — those never hit MVC handlers.

> [!warning] Filters are not the front controller
> Servlet filters (including Spring Security) run **around** `DispatcherServlet`. They are the Servlet API chain, not `HandlerMapping`.

> [!warning] `@Controller` is a handler, not the pattern
> The front controller is the **servlet**. Controllers are beans the servlet **dispatches to**.

> [!tip] Interview answer
> **Front controller means one servlet runs a shared dispatch loop and delegates to handlers, mappings, and views.** In Spring that servlet is `DispatcherServlet`. You can have several, each with its own web context; they share only the optional root context. Filters still run first, and the URL mapping decides which requests even enter the servlet.
