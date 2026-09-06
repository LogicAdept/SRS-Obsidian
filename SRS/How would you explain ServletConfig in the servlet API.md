<!--
reps: 0
priority: 0
-->
#Java/Servlet/Context #SRS

# How would you explain ServletConfig in the servlet API?

> [!abstract] Short answer
> **`ServletConfig` is the per-servlet-declaration setup object** the container passes into **`Servlet.init`**. From it you read **this servlet’s** name-value **init parameters**, the **servlet name**, and the shared **`ServletContext`**. It is **not** application-wide config: that is **`ServletContext`** (`<context-param>`). Contrast: [[What is the difference between ServletContext and ServletConfig]]. Context API: [[How would you explain ServletContext in Java web applications]]. When `init` runs: [[How does a servlet container manage the servlet lifecycle]].

## One config object per servlet declaration

After the container **instantiates** the servlet, it **must** call **`Servlet.init(ServletConfig)`** **exactly once** and **successfully** before any **`service`**. That `ServletConfig` is **unique per servlet declaration**. Two `<servlet>` (or `@WebServlet` / `addServlet`) names for the same class → **two instances**, **two configs**. `init` **happens-before** later `service` calls.

The interface is four methods:

| Method | Meaning |
| --- | --- |
| `getInitParameter(name)` | This servlet’s init param, or **`null`** if absent |
| `getInitParameterNames()` | Names, or an **empty** enumeration |
| `getServletName()` | Logical name from the descriptor / admin; for an **unregistered** instance, the **class name** |
| `getServletContext()` | The **one** web-app context on this JVM |

Sources of those params: `<servlet><init-param>` in `web.xml`, **`@WebInitParam`** on **`@WebServlet`**, or **`ServletRegistration.setInitParameter`** after **`ServletContext.addServlet`** during application init. They are **not** `<context-param>` and **not** request parameters.

**`GenericServlet` / `HttpServlet` implement `ServletConfig`.** `init(ServletConfig)` **stores** the object; `getInitParameter`, `getServletContext`, `getServletName`, and `getServletConfig()` delegate to it. Override the **no-arg `init()`** so you **need not** call `super.init(config)`: GenericServlet’s `init(config)` stores the config, then calls `init()`. Why that overload: [[Why override the no argument init method in a servlet]]. A constructor is **not** `init`: the config does not exist yet. [[Should you define a constructor for a servlet and how should you initialize it]].

```d2
direction: down
decl: "servlet declaration\n(name + class + init-param)" {
  width: 280
  height: 48
  style.fill: "#fff8e1"
}
cfg: "ServletConfig\n(one per declaration)" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
ctx: "ServletContext\n(one per web app / JVM)" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
s: "servlet instance\ninit(config) then service" {
  width: 260
  height: 48
  style.fill: "#fff3e0"
}
decl -> cfg
cfg -> s
cfg -> ctx
```

**Fig. 1.** `ServletConfig` is per declaration. `ServletContext` is per web application. `getInitParameter` on each object reads a **different** map.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
@WebServlet(
    name = "ReportServlet",
    urlPatterns = "/report",
    initParams = @WebInitParam(name = "format", value = "csv"))
public class ReportServlet extends HttpServlet {
    private String format;

    @Override
    public void init() {
        format = getInitParameter("format"); // this servlet only
        String admin = getServletContext().getInitParameter("adminEmail");
    }
}
```

**Listing 1.** `getInitParameter()` with no receiver is **`ServletConfig`**. `getServletContext().getInitParameter(...)` is **`<context-param>`**. Missing names return **`null`**, not an exception.

> [!warning] `super.init(config)` or the no-arg `init()`
> If you override **`init(ServletConfig)`** on `HttpServlet` / `GenericServlet` and **skip `super.init(config)`**, the stored config is **never set**, so `getInitParameter` / `getServletContext` after that do not work. Prefer **`init()`**. Failed `init` (`ServletException` / `UnavailableException`) means the servlet is **not** put in service and **`destroy` is not called**.

> [!warning] Same method name, two maps
> `servlet.getInitParameter("x")` is **`<init-param>`**. `getServletContext().getInitParameter("x")` is **`<context-param>`**. They do not fall through to each other. Config is **not** request-scoped: it outlives every `service` call for that instance.

> [!tip] Interview answer
> ServletConfig is the object the container passes to init for this servlet declaration: init-param, servlet name, and a handle to ServletContext. I read servlet-specific setup from it, and I get application-wide context-param from the context instead. On HttpServlet I override the no-arg init so GenericServlet can store the config first.
