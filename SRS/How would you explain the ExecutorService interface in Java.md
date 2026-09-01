<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# How would you explain the ExecutorService interface in Java?

> [!abstract] Short answer
> **`ExecutorService`** is an **`Executor` that you can shut down and that can hand back a `Future`**. `Executor` only **`execute(Runnable)`** — submit work, hide how it runs. This interface adds **asynchronous results** (`submit`, bulk `invokeAll` / `invokeAny`) and a **termination protocol** so workers can be reclaimed. It is a **contract**, not a pool: factories such as **`Executors.newFixedThreadPool`** return **implementations** (`ThreadPoolExecutor`, and so on). Vs `new Thread`: [[What advantages does ExecutorService offer over creating raw threads]]. The usual implementation: [[How would you explain ThreadPoolExecutor]].

## Decouple submission from threads, then own the lifecycle

Program to **`ExecutorService`**, not to a concrete pool class, unless you need tunables. Callers **submit tasks**; the service **queues, schedules, and runs** them. `execute` may still run in a **new** thread, a **pooled** thread, or the **caller** — that is the `Executor` contract, not “always a worker”. **`submit` is `execute` plus a `Future`** — [[What is the difference between submit and execute on an executor service]]. The handle: [[How would you explain the Future interface in java.util.concurrent]].

**Shutdown is part of the type.** `shutdown()` rejects **new** work and lets queued tasks finish. `shutdownNow()` tries to **stop** running tasks (typically **interrupt**) and returns **waiting** ones. `isTerminated` is true only **after** a shutdown **and** every task is done. **`close()`** (19+, `AutoCloseable`) is orderly shutdown **then wait**. An unused service should be shut down so non-daemon workers can die.

```java
try (ExecutorService pool = Executors.newFixedThreadPool(4)) {
    Future<Integer> f = pool.submit(() -> 42);
    int n = f.get();
}
```

**Listing 1.** Code against the interface. The factory chooses the implementation. `try-with-resources` calls `close()`.

```d2
direction: down
e: "Executor\nexecute(Runnable)" {
  width: 220
  height: 44
  style.fill: "#e3f2fd"
}
es: "ExecutorService\nFuture + shutdown" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
impl: "ThreadPoolExecutor\n(and other impls)" {
  width: 240
  height: 44
  style.fill: "#fff8e1"
}
e -> es: "extends"
es -> impl: "implemented by"
```

**Fig. 1.** The interface is the extra contract on top of `Executor`. A pool is one implementation.

> [!warning] Forgetting shutdown keeps the JVM alive
> Default pool threads are **non-daemon**. If you never `shutdown` / `close`, those workers outlive your last task and the process may not exit.

> [!warning] `execute` is not “always a pool thread”
> The interface allows the **calling** thread. `ThreadPoolExecutor.CallerRunsPolicy` uses that. Do not assume `execute` started a worker.

> [!tip] Interview answer
> ExecutorService is Executor plus two things: a Future when I submit work, and a shutdown protocol so I can stop accepting tasks and reclaim threads. I code to the interface; newFixedThreadPool and friends return implementations. I always shut it down when I am done, because pool threads are not daemon by default.
