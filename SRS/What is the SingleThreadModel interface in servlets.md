<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/Concurrency/Threads #SRS

# What is the SingleThreadModel interface in servlets?

> [!abstract] Short answer
> **`SingleThreadModel`** was a **marker** (no methods) meaning: the container must **not** run **`service` on two threads at once** for that servlet — by **synchronizing one instance** or a **pool of instances**. It **never** made **session attributes** or **statics** safe. **Deprecated in Servlet 2.4** (no replacement). **Removed in Servlet 6.** Today: **one instance, many request threads**. Do **not** implement it; keep request state **local** and protect **shared** fields. Concurrent servlets: [[How do servlets work in a multithreaded environment]]. Lifecycle: [[How does a servlet container manage the servlet lifecycle]], [[What are the three core Servlet lifecycle methods and their roles]]. Session: [[How would you explain HTTP sessions in servlet based applications]]. Deadlock: [[How can a servlet deadlock]]. What is a servlet: [[What is a servlet]].

## A failed “make it single-threaded” flag

The interface **guaranteed** only **`service`**. The container could still **share** **`HttpSession`** and **class** state across requests. Pooling instances **multiplied** fields, it did **not** isolate the JVM. **Synchronizing `service`/`doGet`** to fake the old model **serializes the whole app** — same anti-pattern.

**Servlet 6+:** the type **does not exist**. Write servlets as **thread-safe** for concurrent **`doGet`/`doPost`**.

```java
// Historical only — gone from Servlet 6
public class OldServlet extends HttpServlet implements SingleThreadModel {
  private int hits; // still racy vs other instances / statics / session
  protected void doGet(HttpServletRequest req, HttpServletResponse resp) {
    hits++; // not a reason to resurrect this interface
  }
}
```

**Listing 1.** Marker promised nothing about **session** or **static** data. Do not copy this.

```d2
direction: down
m: "implements SingleThreadModel" {
  width: 260
  height: 36
  style.fill: "#fff8e1"
}
a: "sync one instance" {
  width: 180
  height: 36
  style.fill: "#ffebee"
}
b: "pool of instances" {
  width: 180
  height: 36
  style.fill: "#ffebee"
}
m -> a
m -> b
```

**Fig. 1.** Two container strategies. Neither fixes shared session or statics.

> [!warning] Deprecated, then deleted
> Servlet **2.4** deprecated it. Servlet **6** **removed** it. New code cannot implement it.

> [!warning] Not a concurrency design
> Use **request/response locals**, a **private mutex** for servlet fields you must share, or an **external store**. Do not lock **`service`**.

> [!tip] Interview answer
> SingleThreadModel was a marker so the container would not run service on two threads at once, by locking one instance or pooling instances. It did not protect session attributes or statics, so it was deprecated in 2.4 and removed in Servlet 6. Today one servlet instance serves many threads, and I keep mutable state off the instance or lock a private field.
