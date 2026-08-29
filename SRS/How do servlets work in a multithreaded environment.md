<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/Concurrency/Threads #SRS

# How do servlets work in a multithreaded environment?

> [!abstract] Short answer
> The container keeps **one servlet instance per declaration** (per JVM if the app is distributable) and may run **`service` on many threads at once** — typically `HttpServlet.service` dispatching to `doGet` / `doPost`. `init` happens-before those calls. **Instance and class fields are shared.** Do **not** synchronize `service` (or `doGet`/`doPost`) to paper over that; protect shared data, or keep state on the request/session with a defined concurrency story. `SingleThreadModel` is **gone** (removed in Servlet 6).

## One instance, many request threads

Load → construct → `init(ServletConfig)` once → zero or more `service` calls → `destroy` after service threads have left (or a timeout). `init` must succeed before any request. The container makes `init`’s writes visible to later `service` threads (happens-before).

For a non-distributed app the container **must** use only one instance per servlet declaration. Concurrent clients are concurrent `service` invocations on that object. HTTP methods are extra dispatch from `HttpServlet.service`, not extra instances. Lifecycle types: `ServletRequest` / `ServletResponse` (HTTP: `HttpServletRequest` / `HttpServletResponse`) are the per-call arguments.

```java
import java.io.IOException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpServletRequest;

public final class HitServlet extends HttpServlet {
    private int hits; // shared by every request thread — racy

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {
        hits++; // not atomic, not ordered
        resp.getWriter().write(Integer.toString(hits));
    }
}
```

**Listing 1.** Conceptual anti-pattern. Locals and the request/response for **this** call are the usual thread-confined state. Shared mutable fields need atomics, a lock on a **private** mutex — [[Why might you synchronize on a private mutex object in Java]] — or an external store. [[What is the SingleThreadModel interface in servlets]] is the obsolete “one thread per instance” myth.

```d2
direction: down
inst: "one servlet instance\ninit once" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
t1: "thread A service/doGet" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
t2: "thread B service/doGet" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
inst -> t1
inst -> t2
```

**Fig. 1.** Blocking inside `service` holds a container thread. Async (`startAsync`) exists so that thread can return while another thread or dispatch finishes the response — then **you** must handle concurrent access to the request/response if work overlaps the original dispatch.

`destroy` runs only after `service` threads have exited or a timeout; the container will not call `service` again on that instance afterward.

> [!warning] Do not synchronize `service` / `doGet` / `doPost`
> The spec strongly recommends against it: the container must serialize requests through that instance (it cannot use an instance pool for that case in the old STM world), and throughput collapses. Fine-grained locks or no shared mutable servlet fields.

> [!warning] `HttpSession` is not a private heap
> Objects reachable from more than one servlet (sessions, context attributes, files, pools) can be used by several threads at once. STM never made those single-threaded either; it is also **removed** in Servlet 6.

> [!tip] Interview answer
> One servlet object, many container threads in `service`/`doGet`. Treat instance fields as shared. Keep per-request data on the stack and the request object. Do not lock the whole `service` method. `SingleThreadModel` is removed; write the servlet to be reentrant.
