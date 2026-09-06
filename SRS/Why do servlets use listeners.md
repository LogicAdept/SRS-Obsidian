<!--
reps: 0
priority: 0
-->
#Java/Servlet/Listeners #SRS

# Why do servlets use listeners?

> [!abstract] Short answer
> Servlets use **listeners** so the **container** can **notify application code** when **`ServletContext`**, **`HttpSession`**, or **`ServletRequest`** **lifecycle or attributes** change — **without** putting that work in **`service` / `doGet`**. Jakarta Servlet **6.1 §11.1**: **control**, **factorization**, and **efficient resource management**. Typical **why**: open a **pool / log / scheduler** in **`contextInitialized`**, close it in **`contextDestroyed`**; count or clean **sessions**; observe **request start/end**. They **do not intercept** the request the way a **filter** does. Vs filters: [[When should you use servlet filters versus listeners]]. Filter chain: [[How would you explain servlet filters and request interception]]. Startup order: [[How does a servlet container manage the servlet lifecycle]]. `@WebListener`: [[What features were added in the Servlet 3 specification]].

## What the events are for

Listeners are **WAR classes** with a **public no-arg constructor**. The container **instantiates and registers** them at **deploy**, **before** the first request (**§11.3.3**). **`AsyncListener`** is the exception: **only** via **`AsyncContext.addListener`**.

| Scope | Why you listen | Interfaces |
| --- | --- | --- |
| **Context** | **JVM-level** app resources: start/stop, context attributes. Spec example: **DB login** into **`ServletContext`**, **close** on undeploy. | **`ServletContextListener`**, **`ServletContextAttributeListener`** |
| **Session** | Resources for **one client**: create, **invalidate / timeout**, attributes, **id change**, **activation**. | **`HttpSessionListener`**, **`HttpSessionAttributeListener`**, **`HttpSessionIdListener`**, **`HttpSessionActivationListener`**; **`HttpSessionBindingListener`** on the **bound object** |
| **Request** | State for **this** request’s life. | **`ServletRequestListener`**, **`ServletRequestAttributeListener`** |
| **Async** | Timeout, error, **complete**. | **`AsyncListener`** |

Declare with **`<listener>`** (order = invoke order; **destroy** often **reverse**) or **`@WebListener`**. Several classes may share one event type.

```d2
direction: down
d: "deploy" {
  width: 90
  height: 32
}
l: "listener contextInitialized" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
s: "servlet service" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
x: "listener contextDestroyed" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
d -> l
l -> s: "first request"
s -> x: "undeploy"
```

**Fig. 1.** Listeners wrap the **app lifetime**. Servlets still handle **HTTP**.

```java
// Conceptual
@WebListener
public class PoolListener implements ServletContextListener {
    @Override
    public void contextInitialized(ServletContextEvent e) {
        e.getServletContext().setAttribute("pool", openPool());
    }
    @Override
    public void contextDestroyed(ServletContextEvent e) {
        closePool(e.getServletContext().getAttribute("pool"));
    }
}
```

**Listing 1.** **Why** a listener exists: **acquire and release** shared state **outside** every servlet.

> [!warning] A listener is not a filter and not a servlet
> **`ServletRequestListener.requestInitialized`** is **not** **`doFilter`**. You **cannot** wrap the response or **stop** the chain. Putting **per-request business logic** in a listener **hides** it from the mapping. **Unhandled** exceptions in **`contextInitialized`** / session timeout callbacks can make the app answer **500** for later requests.

> [!warning] Binding vs attribute listeners
> **`HttpSessionBindingListener`** is implemented by the **value** (`valueBound` / `valueUnbound`). It is **not** listed next to **`HttpSessionAttributeListener`** as an app-wide observer. **TLD-discovered** context listeners **cannot** call **3.0+ `addServlet`**. **`addListener` after startup** is too late.

> [!tip] Interview answer
> We use listeners to react to container lifecycle, not to handle GET and POST. ServletContextListener is the usual place to start and stop application-wide resources. Session and request listeners manage shorter-lived state. I pick a filter when I need to wrap or block the request; I pick a listener when I need a callback that no URL mapping should own.
