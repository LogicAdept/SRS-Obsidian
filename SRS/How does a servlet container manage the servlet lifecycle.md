<!--
reps: 0
priority: 0
-->
#Java/Servlet/Lifecycle #SRS

# How does a servlet container manage the servlet lifecycle?

> [!abstract] Short answer
> The container owns **load → instantiate → `init` → `service` (many times, often concurrent) → `destroy` → GC**. Those three methods are on **`Servlet`**; the **constructor is not** one of them. Load may happen at deploy (`load-on-startup ≥ 0`) or **lazily** on first need (annotation / API **default `-1`**). **`init(ServletConfig)` runs once** and must finish before any request. **`destroy` runs once** on that instance after in-flight `service` calls finish (or a container timeout); the container **never** reuses that instance. HTTP: `HttpServlet.service` dispatches to **`doGet` / `doPost` / …**. Methods: [[What are the three core Servlet lifecycle methods and their roles]]. Eager init: [[How do you start a servlet when the web application starts]]. No-arg `init`: [[Why override the no argument init method in a servlet]]. Threads: [[How do servlets work in a multithreaded environment]]. HTTP type: [[Why is HttpServlet declared as an abstract class]].

## The container drives `init`, `service`, and `destroy`

You do **not** construct the servlet for traffic and you do **not** call `init` / `destroy` yourself. For a **non-distributed** app the container keeps **one instance per servlet declaration**. A **distributable** app: **at most one instance per declaration per JVM**. Two names for the **same class** → **two instances**, **two lifecycles**.

**Load and instantiate.** The container finds the class with ordinary Java class loading and **`new`s it**. That can be when the application starts, or later when a request needs the servlet.

**Initialize.** `init(ServletConfig)` runs **once**. Here you read init parameters, touch `ServletContext`, and open costly resources. Until `init` returns successfully, the instance **must not** handle requests. If `init` throws `ServletException` or `UnavailableException`, the instance is **dropped** and **`destroy` is not called** (initialization failed). The container **may** construct a **new** instance later (it must wait if `UnavailableException` gave a minimum downtime).

**Service.** After a successful `init`, the container may call `service(request, response)` on **several threads at once**. An instance **might handle zero requests** in its lifetime. Do **not** synchronize `service` (or the `doXxx` methods it calls) as a default — it serializes the servlet. `HttpServlet.service` picks `doGet`, `doPost`, and the rest from the HTTP method. `ServletException` means this request failed; **permanent** `UnavailableException` → container **`destroy`s** the instance and later requests get **404**; **temporary** → **503** + `Retry-After` (a container **may** treat every unavailability as permanent).

**End of service.** The container may unload whenever it wants (memory, shutdown). It waits for current `service` threads (or a server time limit), calls **`destroy` once**, then **must not** route more requests to **that** object. To use the servlet again it **instantiates a new one**. After `destroy` returns, the instance is eligible for GC.

Application **listeners** run around this. On deploy, in order: **listeners constructed** → **`ServletContextListener.contextInitialized`** → **filters `init`** → servlets with **`load-on-startup` ≥ 0** (`lower integers first`). On shutdown, servlets are **destroyed before** `contextDestroyed`. A JVM crash **skips `destroy`**.

```d2
direction: down
load: "load class + instantiate" {
  width: 240
  height: 36
  style.fill: "#fff8e1"
}
ini: "init(ServletConfig) once" {
  width: 240
  height: 36
  style.fill: "#e3f2fd"
}
svc: "service on N threads" {
  width: 240
  height: 36
  style.fill: "#e8f5e9"
}
end: "wait in-flight service\ndestroy once → GC" {
  width: 240
  height: 48
  style.fill: "#ffebee"
}
fail: "init throws\nno destroy, drop instance" {
  width: 240
  height: 48
  style.fill: "#ffebee"
}
load -> ini
ini -> svc
ini -> fail
svc -> end
```

**Fig. 1.** Failed `init` skips `destroy`. Successful instances leave only through `destroy`.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
public class LifecycleServlet extends HttpServlet {
    @Override
    public void init() { /* once, after GenericServlet stored ServletConfig */ }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {
        resp.getWriter().write("ok");
    }

    @Override
    public void destroy() { /* once; then this instance is dead */ }
}
```

**Listing 1.** `init()` is the no-arg hook `GenericServlet` calls from `init(ServletConfig)`. The container still owns the sequence.

> [!warning] Static initializers are not `init`
> Class loading can run `<clinit>` when a tool inspects the WAR. Treat the servlet as **in the container** only after `Servlet.init`. Failed `init` **must not** expect `destroy` for cleanup — clean up in the `init` method that threw, or use a listener for app-wide resources.

> [!warning] One instance, many threads
> Shared fields need their own concurrency story. Request and response objects are **not** thread-safe (aside from `startAsync` / `complete`). After `destroy`, that instance is finished — a later mapping hit is a **new** object.

> [!tip] Interview answer
> The container loads and instantiates the servlet, calls init once with ServletConfig, then may call service concurrently for each request, and later calls destroy once after in-flight service calls finish. I do not construct that instance or invoke init and destroy myself. If init fails, destroy is skipped and the container may try a new instance later; HTTP work still enters through service, which HttpServlet turns into doGet or doPost.
