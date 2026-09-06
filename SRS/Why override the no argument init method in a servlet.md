<!--
reps: 0
priority: 0
-->
#Java/Servlet/Lifecycle #SRS

# Why override the no argument init method in a servlet?

> [!abstract] Short answer
> Override **`GenericServlet.init()`** (no args) so **`GenericServlet.init(ServletConfig)`** can **store the config first**, then call you. Jakarta Servlet **6.1** JavaDoc: it is a **convenience** so you **need not** **`super.init(config)`**. The container **only** calls **`Servlet.init(ServletConfig)`**. `GenericServlet`’s implementation **saves** that object and then invokes **`init()`**. Override the **one-arg** form, skip **`super`**, and **`getServletConfig()` / `getInitParameter()` are null**. Constructor vs `init`: [[Should you define a constructor for a servlet and how should you initialize it]]. Lifecycle: [[What are the three core Servlet lifecycle methods and their roles]]. Config object: [[How would you explain ServletConfig in the servlet API]]. Generic vs HTTP: [[What is the difference between GenericServlet and HttpServlet]].

## Two `init` methods

| Method | Who calls it | Job |
| --- | --- | --- |
| **`Servlet.init(ServletConfig)`** | **Container**, **once**, before **`service`**. | Place the servlet **into service**. |
| **`GenericServlet.init(ServletConfig)`** | Same (inherited by **`HttpServlet`**). | **Store** `config`, then **`init()`**. JavaDoc: if you override **this**, **`super.init(config)`**. |
| **`GenericServlet.init()`** | **`GenericServlet.init(ServletConfig)`**, not the container. | **Your** one-time setup. Config still via **`getServletConfig()`**. |

The **`Servlet` interface has no no-arg `init`**. That overload exists only on **`GenericServlet`** (and **`GenericFilter`**).

```d2
direction: down
c: "container" {
  width: 120
  height: 32
}
one: "init(ServletConfig) stores config" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
zero: "init() your code" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
c -> one
one -> zero
```

**Fig. 1.** No-arg **`init`** runs **after** the config is installed.

```java
// Conceptual — HttpServlet / GenericServlet
@Override
public void init() throws ServletException {
    String dsn = getInitParameter("dsn");
}

@Override
public void init(ServletConfig config) throws ServletException {
    super.init(config); // required if you override this form
}
```

**Listing 1.** Prefer the **empty** `init()`. If you take **`ServletConfig`**, **`super.init(config)`** is mandatory.

> [!warning] Skip `super.init(config)` and the servlet is half-dead
> **`getServletConfig()`** stays **null**. Later **`getServletContext()` / `getInitParameter()`** NPE. The container **already called** the one-arg method; your no-arg override **does not** replace that call unless you **also** override the one-arg and **forget** to chain.

> [!warning] Do not init in the constructor
> The constructor runs **before** **`ServletConfig` exists**. **`init()`** is the first legal place for **init-params** and **`ServletContext`**. Implementing **`Servlet` yourself** means you **must** write **`init(ServletConfig)`** and **keep** the config — there is **no** convenience overload.

> [!tip] Interview answer
> I override GenericServlet’s no-argument init because GenericServlet already stores ServletConfig and then calls that method. I avoid overriding init(ServletConfig) so I cannot forget super.init(config). Initialization belongs there, not in the constructor.
