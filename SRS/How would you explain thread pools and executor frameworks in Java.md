<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# How would you explain thread pools and executor frameworks in Java?

> [!abstract] Short answer
> The **executor framework** (`java.util.concurrent`, Java 5) is **`Executor.execute(Runnable)`** plus **`ExecutorService`**: queue and schedule work, return **`Future`**, **shut down**. A **thread pool** is the usual implementation: a **bounded (or cached) set of worker threads** pulling tasks, so you do not **`new Thread` per request**. **`Executors`** factories wire common **`ThreadPoolExecutor`** / **`ForkJoinPool`** / **virtual-thread-per-task** setups. Prefer factories unless you are tuning the pool. Interface: [[How would you explain the ExecutorService interface in Java]]. Vs raw threads: [[What advantages does ExecutorService offer over creating raw threads]]. Cached pool: [[How would you explain Executors.newCachedThreadPool()]].

## Execute, pool, then shut down

`execute` may run the task in a **new** thread, a **pool** thread, or the **caller** — that is the `Executor` contract, not “always a new `Thread`”. **`submit`** is `execute` plus a **`Future`**. **`shutdown` / `shutdownNow`** (or try-with-resources on `ExecutorService`) stop accepting work; idle workers exit. Package map: [[How would you explain the java.util.concurrent package]]. `submit` vs `execute`: [[What is the difference between submit and execute on an executor service]].

**`ThreadPoolExecutor`** is the tunable pool: **core / max** size, **work queue**, **keep-alive**, **`RejectedExecutionHandler`**. Core threads are created even if others are idle; extra threads only if the **queue is full** and size is still below max. **Fixed** factory: `n` threads, **unbounded** queue (tasks wait; the pool does not grow). **Cached** factory: **unbounded threads**, **`SynchronousQueue`**, 60s idle reclaim — **not** an unbounded queue. Saturated finite queue + finite max → **reject** (abort, caller-runs, discard, …). Tuning class: [[How would you explain ThreadPoolExecutor]]. Queue full: [[What happens when a thread pool queue is full and a new task arrives]]. Factories: [[How would you explain Executors]].

**`ScheduledExecutorService`** adds delay and periodic runs. **`newWorkStealingPool`** is a **`ForkJoinPool`**: multiple queues, no FIFO guarantee — [[What is the Java ForkJoin framework]]. **`newVirtualThreadPerTaskExecutor`** starts a **new virtual thread per task** (unbounded); it is an executor, **not** a bounded platform-thread pool. Pool sizing: [[How do you choose the size of a thread pool]].

```java
try (ExecutorService pool = Executors.newFixedThreadPool(4)) {
    Future<Integer> f = pool.submit(() -> 42);
    pool.execute(() -> System.out.println(Thread.currentThread().getName()));
    f.get();
}
```

**Listing 1.** Factory pool, `submit` + `execute`, then close (shutdown). Four workers; extra tasks wait on the unbounded queue.

```d2
direction: down
c: "client" {
  width: 100
  height: 36
  style.fill: "#fff8e1"
}
es: "ExecutorService" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
q: "work queue" {
  width: 140
  height: 36
  style.fill: "#f3e5f5"
}
w: "worker threads" {
  width: 160
  height: 36
  style.fill: "#e8f5e9"
}
c -> es: "execute / submit"
es -> q: "enqueue or reject"
q -> w: "idle worker takes task"
```

**Fig. 1.** Framework = submit path + lifecycle. Pool = workers + queue.

> [!warning] Unbounded queue is not unbounded threads
> `newFixedThreadPool` can **OOM** the **queue**. `newCachedThreadPool` can **OOM** on **threads**. Neither is “unlimited but safe.”

> [!warning] A pool is not fire-and-forget
> Without **shutdown** (or try-with-resources), non-daemon workers keep the JVM alive. `execute` on a custom `Executor` might still run on the **caller**.

> [!tip] Interview answer
> The executor framework is execute plus ExecutorService for futures and shutdown; a thread pool is the usual implementation that reuses workers instead of starting a platform thread per task. I take a factory from Executors unless I need to tune ThreadPoolExecutor. I shut the service down, and I do not confuse a fixed pool’s unbounded queue with a cached pool’s unbounded thread count.
