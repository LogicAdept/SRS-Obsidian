<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS

# What are Future and CompletableFuture for in Java?

> [!abstract] Short answer
> **`Future<V>`** is a **handle** for a result that **may not be ready**: **`isDone`**, **`get`** (blocks, wraps failure in **`ExecutionException`**), **`cancel`**. You usually **receive** one from **`ExecutorService.submit`**, not complete it yourself. **`CompletableFuture<V>`** **is a `Future`** you **can complete**, plus **`CompletionStage`**: **`thenApply` / `thenCompose` / `thenCombine`**, **`supplyAsync`**, **`complete` / `completeExceptionally`**. **`join()`** throws **`CompletionException`** instead of `ExecutionException`. Future API: [[How would you explain the Future interface in java.util.concurrent]]. Style: [[How would you explain the Future interface in java.util.concurrent]]. CF: [[How would you explain CompletableFuture]]. Compose: [[How would you explain CompletableFuture for composing async work]]. `FutureTask`: [[How would you explain FutureTask in Java concurrency]].

## Handle vs completable stage

A **`Future`** does not run the work; an **executor** (or **`FutureTask`**) does. **`get`** waits. **`cancel(true)`** on a **`FutureTask`/`ThreadPoolExecutor` task** may **interrupt** the worker; on a **`CompletableFuture`**, **`cancel` is `completeExceptionally(new CancellationException())`** — it does **not** own the computation, so it need **not** interrupt a `supplyAsync` thread.

**`CompletableFuture`**: only **one** of `complete` / `completeExceptionally` / `cancel` wins. Dependent **non-async** actions may run on the **completing** thread. **`*Async`** without an `Executor` uses **`ForkJoinPool.commonPool()`** (or a new thread if parallelism &lt; 2). Stages: [[How would you explain CompletableFuture thenApply vs thenCompose vs thenCombine]]. Executor submit: [[How would you explain the ExecutorService interface in Java]].

```java
ExecutorService pool = Executors.newCachedThreadPool();
Future<Integer> f = pool.submit(() -> 1);     // handle only
int a = f.get();

CompletableFuture<Integer> cf =
        CompletableFuture.supplyAsync(() -> 1)
                .thenApply(n -> n + 1);       // compose, then join/get
int b = cf.join();
```

**Listing 1.** `submit` → `Future`. `supplyAsync` + `thenApply` → a **`CompletableFuture`** you can still `get`/`join`.

```d2
direction: down
fut: "Future" {
  width: 140
  height: 36
  style.fill: "#fff8e1"
}
cf: "CompletableFuture" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
fut -> cf: "implements Future +\nCompletionStage +\ncomplete()"
```

**Fig. 1.** `Future` = wait/cancel. `CompletableFuture` = that plus **pipeline** and **manual complete**.

> [!warning] `get()` is still blocking
> A chain of `thenApply` does not make `get`/`join` non-blocking. Blocking inside `supplyAsync` on the **common pool** can **starve** Fork/Join work.

> [!warning] Cancellation is not the same type
> `FutureTask.cancel(true)` can interrupt. `CompletableFuture.cancel` only completes the stage exceptionally unless you built interruption yourself.

> [!tip] Interview answer
> Future is the result handle from submit: I block on get or cancel. CompletableFuture is a Future I can complete and chain with thenApply and thenCompose. I use Future when the executor owns the task, and CompletableFuture when I need composition or to complete from a callback.
