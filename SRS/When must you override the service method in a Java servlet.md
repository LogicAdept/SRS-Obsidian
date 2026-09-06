<!--
reps: 0
priority: 0
-->
#Java/Servlet/Lifecycle #SRS

# When must you override the service method in a Java servlet?

> [!abstract] Short answer
> **You must implement `service` when `HttpServlet` is not doing HTTP dispatch for you.** **`Servlet.service` has no default.** **`GenericServlet.service` is `abstract`** — a **`GenericServlet` subclass must override it.** **`HttpServlet` already implements `service`** and **routes to `doGet` / `doPost` / …**. Its JavaDoc: **almost no reason to override `service`**. For a web servlet, **override `doXxx`**, not `service`. Generic vs HTTP: [[What is the difference between GenericServlet and HttpServlet]]. `doXxx` list: [[What are the main HttpServlet request handling methods]]. Lifecycle: [[What are the three core Servlet lifecycle methods and their roles]]. Creating the class: [[What steps are required to create a servlet]].

## Abstract on `GenericServlet`, implemented on `HttpServlet`

Jakarta Servlet **6.1**:

| You extend / implement | `service` | What you override |
| --- | --- | --- |
| **`Servlet`** (directly) | You **must** write **`service(ServletRequest, ServletResponse)`** | That method (plus `init`/`destroy`/…) |
| **`GenericServlet`** | **`abstract`** — **must** override | Protocol-neutral `service` |
| **`HttpServlet`** | **Already implemented** (public method casts, protected method **dispatches** on HTTP method) | **`doGet` / `doPost` / `doPut` / `doPatch` / …** |

**`HttpServlet`:** “There’s almost no reason to override the `service` method.” Overriding **protected `service(HttpServletRequest, HttpServletResponse)`** **skips `doXxx` and `getLastModified`**. Overriding **public `service(ServletRequest, ServletResponse)`** also **breaks** that dispatch unless you call **`super.service`**.

Legitimate **`GenericServlet.service`**: a **non-HTTP** request/response protocol the container actually supports. Legitimate **`HttpServlet.service` override** is rare (a method **`HttpServlet` does not dispatch**). Prefer **`doXxx`** or, for OPTIONS extras, **`doOptions`**. Threads: [[How do servlets work in a multithreaded environment]].

```d2
direction: down
gs: "GenericServlet\nservice is abstract" {
  width: 240
  height: 48
  style.fill: "#fff3e0"
}
hs: "HttpServlet\nservice → doXxx" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
you: "YourServlet extends HttpServlet" {
  width: 260
  height: 40
}
gs -> hs -> you: "override doGet, not service"
```

**Fig. 1.** **Must** override **`service`** only before **`HttpServlet`** fills it in.

```java
// Conceptual — Jakarta Servlet 6.1
public class PingServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.getWriter().write("ok");
    }
    // do not override service(...) here
}
```

**Listing 1.** HTTP servlet: **`doGet`**. **`service` is already there.**

> [!warning] `service()` instead of `doGet` is not “required for HttpServlet”
> Interview dumps that say implement work in **`service` or `doGet`** mix **`GenericServlet`** with **`HttpServlet`**. If you override **`service`** and forget **`HEAD`/`OPTIONS`/`TRACE`**, those methods **stop** using **`HttpServlet`’s defaults**.

> [!warning] Concurrent `service`
> The container may run **`service` on many threads**. Synchronizing **`service`** (or **`doXxx`**) as a whole is **strongly discouraged**. Call **`super.service`** if you intercept and still want **`doXxx`**.

> [!tip] Interview answer
> I must implement service if I implement Servlet myself or extend GenericServlet, because that method is abstract there. If I extend HttpServlet I must not override service for normal apps; HttpServlet already dispatches to doGet and doPost. I override those instead so HEAD, OPTIONS, and TRACE keep their defaults.
