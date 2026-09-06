<!--
reps: 0
priority: 0
-->
#Java/Servlet/Lifecycle #SRS

# Should you define a constructor for a servlet and how should you initialize it?

> [!abstract] Short answer
> **Do not initialize a servlet in a constructor.** The container **loads the class, then `new`s it**, then **must** call **`Servlet.init(ServletConfig)`** before any **`service`**. **`ServletConfig`**, **`ServletContext`**, init parameters, and (in a Jakarta EE web container) **injected resources** are not ready in `new`. Leave the **implicit public zero-arg constructor**, or write one that only does work that needs **no** container. Put real setup in **`init`**. Prefer **`GenericServlet`’s no-arg `init()`**. Lifecycle: [[How does a servlet container manage the servlet lifecycle]]. Config object: [[How would you explain ServletConfig in the servlet API]]. Why that overload: [[Why override the no argument init method in a servlet]].

## Instantiation is not initialization

Jakarta Servlet **6.1** life cycle: **load → instantiate → `init` → `service` (0..n) → `destroy`**. Instantiation is ordinary Java construction. **`ServletContext.createServlet(Class)`** requires a **zero-argument constructor**. A servlet that only declares **`MyServlet(String)`** (or a **non-public** no-arg) cannot be built that way.

**`init(ServletConfig)`** is the hook for **persistent configuration**, **costly resources** (the spec’s example is JDBC connections), and other **one-time** work. The config is **unique per servlet declaration** and exposes init parameters plus **`ServletContext`**. Failed `init` (`ServletException` / `UnavailableException`): the instance is **not** placed in service and **`destroy` is not called**.

**`GenericServlet` / `HttpServlet`:** `init(ServletConfig)` **stores** the config, then calls **`init()`**. Override **`init()`** so you **need not** call `super.init(config)`. Override **`init(ServletConfig)`** only if you call **`super.init(config)` first**. Methods: [[What are the three core Servlet lifecycle methods and their roles]].

Jakarta EE resource injection on **`Servlet`**: references are injected **before lifecycle methods**. A constructor still sees **uninjected** fields. **Static** initializers are **not** `init`: the spec tells you **not** to open databases or Jakarta Enterprise Beans from class initialization; wait until **`Servlet.init`**.

```d2
direction: down
load: "load Servlet class" {
  width: 220
  height: 40
}
ctor: "public no-arg constructor\n(no ServletConfig)" {
  width: 240
  height: 48
  style.fill: "#fff8e1"
}
init: "init(ServletConfig) once\nthen GenericServlet.init()" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
svc: "service / doXxx" {
  width: 180
  height: 40
}
load -> ctor -> init -> svc
```

**Fig. 1.** Constructor may run; **container init** is **`init`**, after **`new`**.

```java
// Conceptual — Jakarta Servlet 6.1
public class ReportServlet extends HttpServlet {
    private String reportPath;

    public ReportServlet() { } // optional; implicit no-arg is enough

    @Override
    public void init() throws ServletException {
        reportPath = getInitParameter("reportPath"); // needs stored ServletConfig
        if (reportPath == null) {
            throw new UnavailableException("reportPath init-param required");
        }
    }
}
```

**Listing 1.** Empty (or omitted) constructor; **one-time** work in **`init()`** via **`getInitParameter`**.

> [!warning] Constructor has no `ServletConfig`
> `getServletConfig()`, `getInitParameter`, and `getServletContext()` in a constructor (or in **`init(ServletConfig)` before `super.init(config)`**) do not see the stored config. A **parameterized-only** constructor makes **`createServlet` / container `new` fail**.

> [!warning] Static init is not `init`
> A tool or class loader can run **static** initializers **without** an active servlet runtime. Do **not** treat that as permission to open connections. Wait for **`Servlet.init`**. Failed **`init`** does **not** call **`destroy`**, so do not pair cleanup only there for work that never finished.

> [!tip] Interview answer
> I almost never write a servlet constructor beyond the implicit public no-arg the container needs to instantiate the class. Initialization that needs ServletConfig, the context, or injected resources belongs in init, after construction. On HttpServlet I override the no-arg init so GenericServlet has already stored the config. If init throws, the servlet is not in service and destroy is not called.
