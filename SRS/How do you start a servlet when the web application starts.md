<!--
reps: 0
priority: 0
-->
#Java/Servlet/Lifecycle #SRS

# How do you start a servlet when the web application starts?

> [!abstract] Short answer
> Give it a **non-negative `load-on-startup`**. In `web.xml` that is `<load-on-startup>` with **0 or a positive integer**. On the class, **`@WebServlet(loadOnStartup = n)`** with the same rule. Programmatically, `ServletContext.addServlet(…)` then **`ServletRegistration.Dynamic.setLoadOnStartup(n)`** with `n >= 0`. The container **instantiates** the servlet and calls **`init`** while the `ServletContext` is starting — **after** every `ServletContextListener.contextInitialized`. **`-1`**, a **negative** value, or **omitting** the element means the container **may wait until the first request**. Lifecycle: [[How does a servlet container manage the servlet lifecycle]]. Listeners are earlier, not servlet `init`: [[Why do servlets use listeners]]. JSP: [[How do you configure initialization parameters for a JSP]].

## Load at deploy, not on the first hit

“Start” here is **load + instantiate + `Servlet.init`**, not `service` and not a background thread. Without a startup priority the container is free to delay that work until a request needs the servlet.

**Descriptor.** Inside the servlet’s `<servlet>` element, `<load-on-startup>` takes an integer. **≥ 0**: must initialize during application startup. **Negative or absent**: lazy. Lower integers run **before** higher ones. Equal integers: the container chooses the order.

**Annotation.** `@WebServlet`’s `loadOnStartup` is that same integer. The annotation **default is `-1`**, so a mapped `@WebServlet` is **not** started at deploy unless you set a non-negative value.

**Programmatic.** `setLoadOnStartup` on the `Dynamic` registration: **≥ 0** → instantiate and `init` in the **ServletContext initialization phase**, after all configured **`ServletContextListener`s** have returned from `contextInitialized`. **Negative** (default **`-1`**) → lazy. A later call replaces the previous value. You may register from a `ServletContainerInitializer` or from `contextInitialized` (the usual “add servlet during startup” window).

`ServletContextListener` **notifies that the application is starting**. It does **not** initialize servlets: listeners run **before** any servlet or filter `init`. Use a listener for context attributes and resources; use `load-on-startup` when you need **that servlet instance** ready (warm caches, scheduled work kicked from `init`, fail fast if `init` throws).

```d2
direction: down
app: "ServletContext starting" {
  width: 240
  height: 36
  style.fill: "#fff8e1"
}
sci: "SCI / addServlet + setLoadOnStartup" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
lis: "ServletContextListener.contextInitialized" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
eager: "load-on-startup ≥ 0\ninstantiate + init" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
lazy: "negative / omitted / default -1\ninit on first request" {
  width: 280
  height: 48
  style.fill: "#ffebee"
}
app -> sci
sci -> lis
lis -> eager
lis -> lazy
```

**Fig. 1.** Eager servlets `init` after listeners, still during context startup. Lazy servlets wait.

```xml
<!-- Conceptual — jakartaee web-app servlet -->
<servlet>
  <servlet-name>warmup</servlet-name>
  <servlet-class>com.example.WarmupServlet</servlet-class>
  <load-on-startup>1</load-on-startup>
</servlet>
```

**Listing 1.** `1` is an order, not “on/off.” `0` also means start during deployment.

```java
// Conceptual — jakarta.servlet.annotation, Servlet 6.1
@WebServlet(urlPatterns = "/warmup", loadOnStartup = 1)
public class WarmupServlet extends HttpServlet {
    @Override
    public void init() { /* container already called init(ServletConfig) */ }
}
```

**Listing 2.** Omit `loadOnStartup` and the default is **`-1`** (lazy). Same integer rules as `setLoadOnStartup`.

> [!warning] `@WebServlet` does not start the servlet by itself
> Mapping only publishes URL patterns. **`loadOnStartup` defaults to `-1`**. Negative `<load-on-startup>` and a missing element are also lazy. Calling `new WarmupServlet()` and `init` yourself is not container startup and skips how the container owns the instance.

> [!warning] Listeners run first; `init` failure keeps the servlet out of service
> `contextInitialized` fires **before** any servlet `init`. You cannot rely on a load-on-startup servlet already existing there. If `init` throws `ServletException` or `UnavailableException`, that servlet is **not** placed into service. Startup **order** among equal integers is **not** specified.

> [!tip] Interview answer
> I set a non-negative load-on-startup so the container instantiates the servlet and calls init while the application starts, after ServletContextListeners. I use the web.xml element, @WebServlet loadOnStartup, or ServletRegistration.Dynamic setLoadOnStartup, and I remember the annotation default is minus one, which is lazy. A listener is not a substitute: it runs before any servlet init.
