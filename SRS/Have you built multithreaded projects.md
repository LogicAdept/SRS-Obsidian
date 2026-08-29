<!--
reps: 0
priority: 0
-->
#Java/Concurrency #Career/Experience #SRS

# Have you built multithreaded projects?

> [!abstract] Short answer
> A credible **yes** names three things you actually chose: the **thread model** (`ExecutorService` pool of **platform** threads, or **one virtual thread per task** since **21**), the **shared-state protocol** (a **happens-before** edge — `synchronized` / `volatile` / j.u.c, not “it worked in testing”), and the **lifecycle** (`submit` → `Future.get` → **`shutdown` / `close`**). “The JVM had more than one thread” is not that answer. Toolkit: [[How would you explain the java.util.concurrent package]]. Pools vs raw `Thread`: [[What advantages does ExecutorService offer over creating raw threads]]. Principles: [[What principles do you follow in multithreaded Java programming]].

## What “multithreaded work” means in Java

The JVM **allows concurrent threads of execution**. A **`Thread`** is that unit: `start` schedules `run`; the new thread runs **concurrently** with the starter. **Platform** threads map **1:1** to OS threads and are a **limited** resource. **Virtual** threads (same `java.lang.Thread` type) are **runtime-scheduled**, cheap enough that a JVM may host **millions**, and are meant for work that **blocks on I/O**, not long CPU-bound loops. They are **not faster** platform threads: they buy **throughput**, not lower latency. Creating them: [[How would you explain Virtual Threads]].

Production code almost never `new Thread` per request. `Executor` is the hook for **thread pools, async I/O, lightweight tasks**. `ExecutorService` adds **queueing**, **`submit` → `Future`**, **bulk** `invokeAll` / `invokeAny`, and **controlled shutdown**. Unused services **must** be shut down so workers can be reclaimed. `Executors` factories: `newFixedThreadPool` (fixed workers, **unbounded** queue — extra tasks **wait**), `newCachedThreadPool` (grows as needed; idle workers die after **60s**), `newVirtualThreadPerTaskExecutor` (**21**, **unbounded** new virtual thread **per task**, not a pool). Tuning: [[How would you explain ThreadPoolExecutor]].

Shared mutable data needs a **happens-before** story. Conflicting unsynchronized accesses are a **data race**; a **correctly synchronized** program **appears sequentially consistent**. j.u.c **extends** that: submit → task start; task → `Future.get()`; put into a concurrent collection → later take; `unlock` / `release` / `countDown` → matching acquire. Race vs data race: [[What is the difference between a race condition and a data race]].

When **many** threads share a map, **`ConcurrentHashMap`** is the usual choice over a **synchronized `HashMap`**: thread-safe **without one table lock**. It is **not** a transaction around your `get` then `put`. Compound updates use `merge` / `compute*` / `putIfAbsent`. Map details: [[How would you explain ConcurrentHashMap Java 8]].

Walk the interviewer through **your** job in that vocabulary (workload, factory, shared structure, shutdown, one failure you handled). Do **not** invent a project.

```java
ConcurrentHashMap<String, Integer> counts = new ConcurrentHashMap<>();
try (ExecutorService pool = Executors.newFixedThreadPool(4)) {
    List<Future<?>> jobs = new ArrayList<>();
    for (int i = 0; i < 4; i++) {
        jobs.add(pool.submit(() -> counts.merge("ok", 1, Integer::sum)));
    }
    for (Future<?> job : jobs) {
        job.get();
    }
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    throw new IllegalStateException(e);
} catch (ExecutionException e) {
    throw new IllegalStateException(e.getCause());
}
```

**Listing 1.** Bounded **platform** pool, atomic `merge` on a concurrent map, `Future.get` for the happens-before edge, `close()` (since **19**) to shut the service down.

```d2
direction: down
work: "incoming tasks" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
exec: "ExecutorService" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
plat: "fixed platform pool" {
  width: 180
  height: 36
  style.fill: "#e8f5e9"
}
virt: "virtual per task (21+)" {
  width: 200
  height: 36
  style.fill: "#f3e5f5"
}
share: "happens-before on shared state" {
  width: 240
  height: 40
  style.fill: "#ffebee"
}
work -> exec
exec -> plat: "CPU / mixed"
exec -> virt: "blocking I/O scale"
plat -> share
virt -> share
```

**Fig. 1.** Pick a factory for the **workload**, then a documented memory protocol for anything the workers share.

> [!warning] Sitting on container threads is not a concurrency design
> Request threads you did not create still **share** your statics and caches. An unsynchronized `HashMap` there is still a **data race**. Name the **protocol** (`ConcurrentHashMap`, a lock, immutability), not the container.

> [!warning] `newFixedThreadPool` does not bound memory
> Worker count is capped; the **queue is not**. Tasks **wait** on that shared unbounded queue. Cached pools can instead **grow threads**. Virtual-thread executors are **unbounded in threads** — **do not pool** virtual threads; each task is a thread. Saturated **bounded** pools **reject** — [[What happens when a thread pool queue is full and a new task arrives]].

> [!warning] Concurrent is not “atomic for my whole use case”
> `ConcurrentHashMap` retrievals do **not** lock the table. `size()` under concurrent updates is a **transient** estimate. `volatile` is not `i++`. A `Future` from `submit` **hides** the failure until `get`.

> [!tip] Interview answer
> Yes, and I talk about it as workload, executor, shared state, and shutdown. I use ExecutorService instead of raw Thread, ConcurrentHashMap or an explicit happens-before edge instead of a plain HashMap, and I shut the pool down. For I/O-heavy fan-out since 21 I use virtual threads per task, not a pooled platform worker, and I do not pretend the container’s threads made my caches safe.
