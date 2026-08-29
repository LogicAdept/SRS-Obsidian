<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS

# What is CompletableFuture?

> [!abstract] Short answer
> **`CompletableFuture<T>`** (Java 8) is a **`Future`** you **can complete** (`complete` / `completeExceptionally` / `cancel`) and a **`CompletionStage`**: you **chain** **`thenApply` / `thenCompose` / `thenCombine`**. **`supplyAsync` / `runAsync`** start work (default **`ForkJoinPool.commonPool()`** unless parallelism &lt; 2). Only **one** completion wins. **`join()`** throws **`CompletionException`**; **`get()`** wraps it in **`ExecutionException`**. Vs `Future`: [[What are Future and CompletableFuture for in Java]]. Longer: [[How would you explain CompletableFuture]]. Compose: [[How would you explain CompletableFuture for composing async work]]. Stages: [[How would you explain CompletableFuture thenApply vs thenCompose vs thenCombine]].

## Completable handle, not “never block”

You **register** dependents instead of sitting on **`get`** — that is the usual “async” story. **`get`/`join` still block.** Non-async dependents may run on the **thread that completes** the stage. **`cancel`** is **`completeExceptionally(new CancellationException())`**; unlike **`FutureTask`**, CF does **not** own the running supplier, so cancel **need not interrupt**. Future handle: [[How would you explain the Future interface in java.util.concurrent]]. Common pool: [[What is the Java ForkJoin framework]]. `submit`: [[How would you explain the ExecutorService interface in Java]].

There is **no** built-in percent-done callback. Completion is **value**, **exception**, or **cancel**. `null` results are allowed; other **null** arguments throw **NPE**.

```java
CompletableFuture<Integer> cf =
        CompletableFuture.supplyAsync(() -> 1)
                .thenApply(n -> n + 1);
int v = cf.join(); // 2; blocks this thread
```

**Listing 1.** Start on the common pool (by default), compose, then **`join`** if you need the value here.

```d2
direction: down
s: "supplyAsync" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
t: "thenApply" {
  width: 120
  height: 36
  style.fill: "#e3f2fd"
}
j: "join / get" {
  width: 120
  height: 36
  style.fill: "#fff8e1"
}
s -> t -> j: "blocks if you wait"
```

**Fig. 1.** The chain can stay off the caller until **`join`/`get`**. Those two are still blocking.

> [!warning] Async programming is not “main never waits”
> If the caller **`join`s**, it waits. Parking **`supplyAsync`** work on the **common pool** can **starve** Fork/Join tasks.

> [!warning] `thenApply` is not `thenApplyAsync`
> The dependent may run on the **completing** thread. Use **`*Async`** (and an **`Executor`**) when you need a given pool.

> [!tip] Interview answer
> CompletableFuture is a Future I can complete and a pipeline of thenApply and thenCompose. supplyAsync runs the supplier, by default on the common pool. I only block when I call get or join, and cancel just completes the stage exceptionally.
