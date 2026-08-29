<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# What advantages does ExecutorService offer over creating raw threads?

> [!abstract] Short answer
> **`ExecutorService`** **queues and reuses** workers, **bounds** thread (and queue) use, returns a **`Future`**, and has a **shutdown** protocol. **`new Thread(r).start()`** per task pays **full thread startup**, does **not** bound OS threads, has **no** `get()`, and leaves you to **join** or leak **non-daemon** workers. Pools also cut **per-task overhead** and expose **reject** / **keep-alive** policy. Interface: [[How would you explain the ExecutorService interface in Java]]. Framework: [[How would you explain thread pools and executor frameworks in Java]]. `submit` vs `execute`: [[What is the difference between submit and execute on an executor service]]. Raw `Thread`: [[How do you create a thread in Java]].

## Reuse, bound, complete, stop

**`ThreadPoolExecutor`** exists to run **many** async tasks with **less** per-task cost and to **limit** threads consumed. Factories (`newFixedThreadPool`, `newCachedThreadPool`, `newVirtualThreadPerTaskExecutor`, …) wire common settings. **`submit(Callable)`** / **`submit(Runnable)`** wrap work in a **`Future`** (`get`, cancel, `ExecutionException`). **`shutdown` / `shutdownNow` / `awaitTermination`** (and try-with-resources) stop intake; a pile of started `Thread`s has no such API. **`invokeAll` / `invokeAny`** wait on a batch. **`execute`** may still run on the **caller** for a custom `Executor` — that is documented, not a raw-`Thread` default.

You still **must not** leak the service. A **cached** pool can **OOM on threads**; a **fixed** pool can **OOM on the queue**. Saturated bounded pools **reject** — [[What happens when a thread pool queue is full and a new task arrives]]. Tuning: [[How would you explain ThreadPoolExecutor]].

```java
new Thread(() -> work()).start();          // one OS thread, no Future, no shutdown

try (ExecutorService pool = Executors.newFixedThreadPool(4)) {
    Future<Integer> f = pool.submit(() -> 42);
    f.get();
}
```

**Listing 1.** Raw `start` vs a bounded pool plus a `Future`. Closing the service shuts it down.

```d2
direction: down
tasks: "many tasks" {
  width: 120
  height: 36
  style.fill: "#fff8e1"
}
raw: "new Thread per task" {
  width: 180
  height: 40
  style.fill: "#ffebee"
}
pool: "ExecutorService workers" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
tasks -> raw: "unbounded threads"
tasks -> pool: "queue + reuse"
```

**Fig. 1.** The service is a **lifecycle** and a **resource cap**, not just `start()`.

> [!warning] A pool is not “threads I can forget”
> Non-daemon workers keep the JVM up until **shutdown**. `submit` failures hide in the **`Future`**, unlike an uncaught `run()` on a raw thread.

> [!warning] Virtual threads change the “too many `Thread`s” argument
> **`newVirtualThreadPerTaskExecutor`** is still an **`ExecutorService`** (Future, shutdown), not a reason to skip the framework if you want those APIs.

> [!tip] Interview answer
> ExecutorService reuses or bounds workers, queues work, gives me a Future, and shuts down cleanly. Raw new Thread start per request does none of that and can exhaust the machine. I still pick the factory so I do not confuse an unbounded queue with unbounded threads.
