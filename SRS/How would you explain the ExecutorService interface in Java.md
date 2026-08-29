<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# How would you explain the ExecutorService interface in Java?

> [!abstract] Short answer
> **`ExecutorService`** extends **`Executor`**: you still **`execute(Runnable)`**, and you also get **`submit`** (returns a **`Future`**), **`invokeAll` / `invokeAny`**, and **lifecycle** (`shutdown`, `shutdownNow`, `awaitTermination`, **`close`**). **`Executor.execute`** runs the command **sometime later** — in a **new** thread, a **pooled** thread, or the **caller**. Rejection is **`RejectedExecutionException`**. **`submit` is `execute` plus a `Future`.** Factories: **`Executors.newFixedThreadPool`**, cached pool, etc. — those return **`ExecutorService` implementations**, not the interface itself. `execute` vs `submit`: [[What is the difference between submit and execute on an executor service]]. Task types: [[What task types can you submit to an ExecutorService]]. Vs raw `Thread`: [[What advantages does ExecutorService offer over creating raw threads]].

## Submit work, then shut down

`submit(Callable)` / `submit(Runnable)` / `submit(Runnable, result)` schedule work and give you **cancel / `isDone` / `get`**. Actions before submit **happen-before** the task, which **happen-before** `Future.get()`. Bulk: `invokeAll` waits for every task (or timeout then **cancels** the rest); `invokeAny` returns **one successful** result and **cancels** the others. Do not mutate the task collection while those run.

**Shutdown:** `shutdown()` rejects **new** tasks and lets queued ones finish. `shutdownNow()` tries to **stop** running tasks (typically **`interrupt`**) and returns **waiting** tasks. `isTerminated` is true only after a shutdown **and** all tasks are done. **`close()`** (19+) is orderly shutdown **then wait**. An unused service should be shut down so workers can be **reclaimed**. Pools: [[How would you explain thread pools and executor frameworks in Java]]. Cached pool: [[How would you explain Executors.newCachedThreadPool()]]. Futures: [[How would you explain the Future interface in java.util.concurrent]].

```java
try (ExecutorService pool = Executors.newFixedThreadPool(10)) {
    Future<?> f = pool.submit(() -> {});
    f.get();
}
```

**Listing 1.** Factory returns an `ExecutorService`. `submit` gives a `Future`. `try-with-resources` calls `close()`.

```d2
direction: down
ex: "Executor.execute" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
es: "ExecutorService\nsubmit, invoke*, shutdown" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ex -> es: "extends"
```

**Fig. 1.** The interface is execution **plus** a handle and a termination protocol — not “a queue” by itself.

> [!warning] `execute` is not always a pool thread
> The contract allows the **calling** thread. `CallerRunsPolicy` uses that. `submit` still goes through `execute` after wrapping.

> [!warning] Forgetting `shutdown` keeps workers alive
> Default pool threads are **non-daemon**. The process can sit until those threads die. Shut down (or `close`) when you are done.

> [!tip] Interview answer
> ExecutorService is Executor plus Futures and shutdown. I submit Callables or Runnables, then get or invokeAll, and I always shut the service down. execute alone has no result handle and might even run on the caller.
