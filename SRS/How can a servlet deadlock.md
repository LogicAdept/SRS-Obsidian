<!--
reps: 0
priority: 0
-->
#Java/Servlet #Problems/Concurrency #SRS

# How can a servlet deadlock?

> [!abstract] Short answer
> The servlet-shaped deadlock is **two request threads and two instance locks in opposite order**. Each servlet runs a **`synchronized` `service` / `doGet` / `doPost`** (the monitor is **`this`**). Thread 1 holds servlet A and **`include`/`forward`s** to B; thread 2 holds B and dispatches to A. Dispatch stays on the **same thread**, so each still holds its own lock while waiting for the other — a cycle. One nested dispatch on a single request does **not** deadlock: Java monitors are **reentrant**. Threads: [[How do servlets work in a multithreaded environment]]. Dispatch: [[How would you explain the servlet RequestDispatcher for forward and include]]. General deadlock: [[What is deadlock]], [[How do you avoid deadlock in Java]].

## Concurrent `service`, then a second lock

A container **may** run **concurrent** requests through one servlet’s `service` method. The developer must make that safe. Marking `service` (or `doGet` / `doPost`) **`synchronized`** serializes that instance — the spec warns against it for **throughput** — and it also creates a **lock you still hold** if you dispatch.

`RequestDispatcher.include` / `forward` must run the target in the **same thread and JVM** as the original request. The caller’s `synchronized` method therefore **does not drop** its monitor for the duration of the include. The target servlet’s own `synchronized service` then tries to enter **that** instance’s monitor.

```d2
direction: right
t1: "Thread 1\nholds A, include B" {
  width: 210
  height: 56
  style.fill: "#fff8e1"
}
t2: "Thread 2\nholds B, include A" {
  width: 210
  height: 56
  style.fill: "#fff8e1"
}
a: "servlet A monitor" {
  width: 180
  height: 48
  style.fill: "#ffebee"
}
b: "servlet B monitor" {
  width: 180
  height: 48
  style.fill: "#ffebee"
}
t1 -> a: "owns"
t1 -> b: "waits"
t2 -> b: "owns"
t2 -> a: "waits"
```

**Fig. 1.** Two concurrent requests, opposite lock order. Same-thread dispatch keeps the first monitor.

```java
// Conceptual — deadlock needs TWO concurrent requests, opposite directions
public class ServletA extends HttpServlet {
    @Override
    protected synchronized void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        getServletContext().getRequestDispatcher("/b").include(req, resp);
    }
}

public class ServletB extends HttpServlet {
    @Override
    protected synchronized void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        getServletContext().getRequestDispatcher("/a").include(req, resp);
    }
}
```

**Listing 1.** Each `synchronized doGet` locks its servlet instance. One request that A-includes-B-includes-A is **reentrant** on A. Two overlapping requests A→B and B→A can **circular-wait**.

The same cycle works with any pair of monitors, not only two servlet instances. Several request threads may use the **same `HttpSession` at once**; the container keeps the **attribute map** structurally safe, but **attribute objects** are the application’s problem. Lock the session (or an attribute) in one order and the servlet instance in the other, and two session requests deadlock without any dispatcher.

`SingleThreadModel` was a different (failed) serialization knob; it is **gone in Servlet 6** and was never a deadlock story ([[What is the SingleThreadModel interface in servlets]]). Prefer request-local state and a **private mutex** for the few shared fields ([[Why might you synchronize on a private mutex object in Java]], [[How would you explain HTTP sessions in servlet based applications]]).

> [!warning] Same-thread include is reentrant, not a deadlock by itself
> Interview traps say “`include` while `synchronized` always deadlocks.” One thread that A-includes-B (and even B-includes-A) can re-enter A’s monitor. You need **two threads** and a **lock-order cycle**. `wait()` on the servlet monitor **drops** that monitor; that is a different bug class than this cycle.

> [!warning] `synchronized service` is already the wrong default
> Even without a second servlet, synchronizing `service` / `doXxx` turns the instance into a **single-file queue**. The spec’s reason is performance; the deadlock above is the extra cost when that lock is still held across a dispatch. Do not override `service` just to wrap it in `synchronized` ([[When must you override the service method in a Java servlet]]).

> [!warning] Blocking I/O under an instance lock looks like a freeze
> Holding `this` (or the session) while waiting on a **JDBC pool**, remote call, or another servlet’s lock can pin every other request on that monitor. That may be starvation or a pool/lock cycle rather than the two-servlet picture — still treat long waits as **outside** the instance lock.

> [!tip] Interview answer
> A servlet deadlocks when two request threads each hold one monitor and wait for the other. The usual picture is synchronized doGet on servlet A including B while another request’s synchronized doGet on B includes A — dispatch stays on the same thread, so neither lock is released. One nested include is reentrant and will not deadlock by itself. Do not synchronize service; keep locks short, ordered, and off the servlet instance.
