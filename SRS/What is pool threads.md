<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# What is pool threads?

> [!abstract] Short answer
> A **thread pool** is a set of **worker threads** that **run submitted tasks** and are **reused**, instead of `new Thread` per job. In `java.util.concurrent` the usual pool is **`ThreadPoolExecutor`**, used through **`Executor` / `ExecutorService`**. **`Executor` is not a pool** — it is **`execute(Runnable)`**. Size is **core → queue → max → reject**, plus **keep-alive**. There is **no** language formula `N×(1+wait/compute)`. Do **not** pool **virtual threads**. Framework: [[How would you explain thread pools and executor frameworks in Java]]. `ThreadPoolExecutor`: [[How would you explain ThreadPoolExecutor]]. Sizing: [[How do you choose the size of a thread pool]]. Cached: [[How would you explain Executors.newCachedThreadPool()]]. Full queue: [[What happens when a thread pool queue is full and a new task arrives]]. Why `ExecutorService`: [[What advantages does ExecutorService offer over creating raw threads]]. VTs: [[How would you explain Virtual Threads]].

## Reuse workers; the factory is not the pool

**Why:** starting a platform thread is **heavy**; unbounded `new Thread` can **exhaust** the process. A pool **bounds** concurrency (if you configure it) and **reuses** idle workers.

**`execute`:** if **fewer than `corePoolSize`** workers, **start** one (even if others are idle). Else **queue**. If the **queue is full** and **below `maximumPoolSize`**, **start** another. Else **`RejectedExecutionHandler`**. **`newFixedThreadPool(n)`:** `n` workers, **unbounded** queue (`max` never reached). **`newCachedThreadPool()`:** **unbounded threads**, **direct handoff** (`SynchronousQueue`), idle workers die after **60s** — **not** an unbounded queue. **`ForkJoinPool`** is a **work-stealing** pool (`ForkJoinTask`, parallel streams, virtual-thread **carriers**).

**How large:** `ThreadPoolExecutor` itself: **large queues + small pools** cut CPU/OS overhead but can **starve throughput**; **I/O-bound** tasks may need **more** threads than cores because workers **block**. **`Runtime.availableProcessors()`** is a **CPU-bound starting point**, not a law. Measure. **`shutdown` / `shutdownNow`** when you own the pool.

```java
ExecutorService fixed = Executors.newFixedThreadPool(4);          // 4 workers, unbounded queue
ExecutorService cached = Executors.newCachedThreadPool();         // unbounded workers, no queue
fixed.execute(() -> {});
fixed.shutdown();
```

**Listing 1.** Submit work to a pool. `Executor` has only `execute`; lifecycle and `submit` live on `ExecutorService`.

```d2
direction: down
task: "submit task" {
  width: 120
  height: 36
  style.fill: "#fff8e1"
}
core: "core workers" {
  width: 130
  height: 36
  style.fill: "#e8f5e9"
}
q: "queue" {
  width: 80
  height: 36
  style.fill: "#e3f2fd"
}
max: "grow to max / reject" {
  width: 180
  height: 36
  style.fill: "#ffebee"
}
task -> core
core -> q: "core busy"
q -> max: "queue full"
```

**Fig. 1.** Pool policy is workers plus queue, not “`Executor` means pool.”

> [!warning] `Executor` is not a thread pool
> `Executor.execute` runs a `Runnable` **somehow**. The pool type is **`ThreadPoolExecutor`** (or `ForkJoinPool`, `ScheduledThreadPoolExecutor`).

> [!warning] No official `N×(1+WT/ST)` size
> That recipe is **not** in the Java SE API. Wrong size still **OOME**s the queue or **thrash**es the scheduler.

> [!tip] Interview answer
> A thread pool keeps worker threads and runs submitted tasks on them so you do not start a new Thread per request. In Java that is ThreadPoolExecutor behind ExecutorService, with core size, a queue, a max, and a rejection handler. There is no official wait-over-compute formula for the size, and you should not pool virtual threads.
