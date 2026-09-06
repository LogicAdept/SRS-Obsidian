<!--
reps: 0
priority: 0
-->
#Java/Servlet/Context #SRS

# What is the difference between ServletContext and ServletConfig?

> [!abstract] Short answer
> **`ServletConfig` is per servlet declaration.** The container passes **one** into **`Servlet.init`**. From it you get **this servlet’s** **`<init-param>` / `@WebInitParam`**, the **servlet name**, and a handle to the context. **`ServletContext` is per web application** (one object **per JVM** in a distributed deploy). From it you get **`<context-param>`**, **application attributes**, **static resources**, **logging**, and (at startup) **programmatic registration**. **`getInitParameter` exists on both and reads different maps.** Config API: [[How would you explain ServletConfig in the servlet API]]. Context API: [[How would you explain ServletContext in Java web applications]]. Attributes: [[What are servlet attributes for and how do they work]]. `init` vs constructor: [[Should you define a constructor for a servlet and how should you initialize it]].

## One servlet vs the whole app

Jakarta Servlet **6.1**: **`init(ServletConfig)`** receives a config **unique per servlet declaration**. That object also **`getServletContext()`**. **Chapter 4:** there is **one `ServletContext` instance per web application** in this container (per JVM if distributed).

| | **`ServletConfig`** | **`ServletContext`** |
| --- | --- | --- |
| **How many** | One per **`<servlet>` / `@WebServlet`** | One per **web app** (per JVM) |
| **When** | Handed to **`init`**, then **`getServletConfig()`** | **`config.getServletContext()`**, **`getServletContext()`**, request **`getServletContext()`** (3.0+) |
| **String params** | Servlet **init-param** | App **context-param** |
| **Attributes** | No attribute map | **`setAttribute` / `getAttribute`** — all servlets in the app |
| **Also** | **`getServletName()`** | Resources, **`log`**, session timeout, encoding, **`addServlet`** at startup |
| **JSP** | Implicit **`config`** | Implicit **`application`**; EL **`initParam`** is **context-param**, not servlet init-param |

**`GenericServlet` / `HttpServlet` implement `ServletConfig`** by **delegating** to the object stored in **`init(ServletConfig)`**. Filters have a parallel **`FilterConfig`**. EL: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]].

```d2
direction: down
app: "web application / WAR" {
  width: 220
  height: 36
}
ctx: "one ServletContext\ncontext-param + attributes" {
  width: 280
  height: 48
  style.fill: "#e3f2fd"
}
c1: "ServletConfig A\ninit-param" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
c2: "ServletConfig B\ninit-param" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
app -> ctx
ctx -> c1
ctx -> c2
```

**Fig. 1.** Many **configs**, **one** context. **`getInitParameter("x")`** on the wrong object is **`null`**, not a type error.

```java
// Conceptual — Jakarta Servlet 6.1
@Override
public void init() throws ServletException {
    String perServlet = getInitParameter("driver");           // ServletConfig
    String perApp = getServletContext().getInitParameter("dsn"); // ServletContext
    getServletContext().setAttribute("ready", Boolean.TRUE);  // visible to other servlets
}
```

**Listing 1.** Same method name, **two namespaces**. **`init()`** (no-arg) runs after GenericServlet has **stored** the config.

> [!warning] `getInitParameter` is not interchangeable
> A **context-param** is invisible to **`ServletConfig.getInitParameter`**. A servlet **init-param** is invisible to **`ServletContext.getInitParameter`**. Putting a **mutable** object in **context attributes** shares it across **concurrent `service`** threads and **does not replicate** across JVMs.

> [!warning] No config in the constructor
> **`getServletConfig()` / `getServletContext()`** before **`super.init(config)`** (or the no-arg **`init()`**) do not see the stored config. **`addServlet`** is **startup-only**, not from **`service`**.

> [!tip] Interview answer
> ServletConfig is this servlet’s setup: name and init-params, passed into init. ServletContext is the web application: context-params, attributes, and resources, one per app per JVM. I never mix getInitParameter on those two types. HttpServlet implements ServletConfig after it stores the object from init.
