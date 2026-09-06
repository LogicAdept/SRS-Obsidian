<!--
reps: 0
priority: 0
-->
#Java/Servlet/Lifecycle #SRS

# What are the three core Servlet lifecycle methods and their roles?

> [!abstract] Short answer
> On **`jakarta.servlet.Servlet`** they are **`init`**, **`service`**, and **`destroy`**. The container **`new`s** the class, then **`init(ServletConfig)` once** (config, costly setup). After that it may call **`service`** **zero or more** times, **often concurrently**. When it **takes the instance out of service**, it **`destroy`s once** so you can **release resources and persist state**. **`init` is not a constructor**; failed **`init` does not call `destroy`**. Container timing: [[How does a servlet container manage the servlet lifecycle]]. Constructor vs `init`: [[Should you define a constructor for a servlet and how should you initialize it]]. Config: [[How would you explain ServletConfig in the servlet API]]. HTTP `service` → `doXxx`: [[What are the main HttpServlet request handling methods]].

## `init`, `service`, `destroy`

Jakarta Servlet **6.1 §2.3** names these three as the life cycle on **`Servlet`** (`GenericServlet` / `HttpServlet`).

| Method | When | Role |
| --- | --- | --- |
| **`init(ServletConfig)`** | Once, **after** `new`, **before** any **`service`** | Read **init parameters**, **`ServletContext`**, open **JDBC** / other one-time resources. **`GenericServlet`** stores the config then calls **`init()`**. Prefer overriding **`init()`**: [[Why override the no argument init method in a servlet]]. |
| **`service(req, res)`** | **0..n** times after successful **`init`** | Handle **this** request. HTTP: container passes **`HttpServletRequest` / `HttpServletResponse`**; **`HttpServlet.service`** dispatches to **`doGet` / `doPost` / …**. An instance **may never** see a request. |
| **`destroy()`** | Once, when the container **removes** this instance | Release resources, **save persistent state**. Runs after **in-flight `service` threads finish** or a **server time limit**. After **`destroy`**, **that instance is dead**; a later need is a **new object**. |

**Load** and **`new`** are container steps, **not** `Servlet` methods. **`load-on-startup`** only chooses **when** load/`init` happen (deploy vs first request): [[How does a servlet container manage the servlet lifecycle]].

**Concurrency:** many threads may run **`service`** on the **same** instance. Do **not** synchronize **`service`** (or **`doXxx`**) as a blanket lock. Threads: [[How do servlets work in a multithreaded environment]].

```d2
direction: down
init: "init(ServletConfig) once" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
svc: "service 0..n times\n(concurrent threads OK)" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
des: "destroy once\nthen GC-eligible" {
  width: 200
  height: 48
  style.fill: "#fff3e0"
}
init -> svc -> des
```

**Fig. 1.** The **API** life cycle is **three methods**. **`new` is not `init`**.

```java
// Conceptual — Jakarta Servlet 6.1
public class ReportServlet extends HttpServlet {
    @Override
    public void init() throws ServletException {
        // once: config already stored by GenericServlet.init(ServletConfig)
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        // service dispatch for GET; 0..n, maybe concurrent
    }

    @Override
    public void destroy() {
        // once: close what init opened; instance will not serve again
    }
}
```

**Listing 1.** **`init` / `service` (here `doGet`) / `destroy`**. Skip **`super.init(config)`** only because this overrides the **no-arg** `init()`.

> [!warning] Failed `init` skips `destroy`
> **`ServletException` / `UnavailableException` in `init`**: the instance is **not** in service and **`destroy` is not called**. Do not open a resource in **`init`** and assume **`destroy`** will close it if **`init` threw** later. Static initializers are **not** `init`.

> [!warning] After `destroy`, that object is finished
> The container **must not** route more requests to **that** instance. It **may** `destroy` to **save memory**, not only at shutdown. **`destroy` can run while a `service` thread is still winding down** if the time limit expired — do not assume exclusive access to fields without your own coordination.

> [!tip] Interview answer
> The three Servlet lifecycle methods are init, service, and destroy. Init runs once with ServletConfig for one-time setup; service handles each request and must be thread-safe; destroy runs once so I can release what init acquired. If init fails, destroy is not called, and a constructor is not a substitute for init.
