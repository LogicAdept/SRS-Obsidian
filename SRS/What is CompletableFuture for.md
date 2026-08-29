<!--
reps: 0
priority: 0
-->
#Java/Async #Java/Concurrency/Executors #SRS

# What is CompletableFuture for?

> [!abstract] Short answer
> It is for **composing asynchronous work** and for **completing a `Future` yourself**. You **`supplyAsync`** (or complete from a callback), then **`thenApply` / `thenCompose` / `thenCombine` / `whenComplete`** instead of blocking **`ExecutorService.submit` + `get`** after every step. **`complete` / `completeExceptionally`** let NIO, a listener, or another thread **publish** the result. Definition: [[What is CompletableFuture]]. Vs `Future`: [[What are Future and CompletableFuture for in Java]]. Pipeline: [[How would you explain CompletableFuture for composing async work]]. `thenApply` vs `thenCompose`: [[How would you explain CompletableFuture thenApply vs thenCompose vs thenCombine]].

## Pipeline and a completable handle

A plain **`Future`** is usually **produced** by an executor; you **wait** or **cancel**. A **`CompletableFuture`** is also a **`CompletionStage`**: dependents fire when the stage **completes**, possibly on the **completing** thread unless you use **`*Async`**. Default async executor: **`ForkJoinPool.commonPool()`**. **`join`/`get`** are still for “I need the value **on this thread now**.” Fork/Join: [[What is the Java ForkJoin framework]]. `submit`: [[How would you explain the ExecutorService interface in Java]].

Use it to **flatten** dependent async calls (`thenCompose`), **join** two results (`thenCombine`), and **handle** errors on the stage (`exceptionally` / `handle`). It is **not** a reactive stream (no backpressure API here). **`cancel`** completes exceptionally; it does **not** automatically interrupt a running `supplyAsync` task.

```java
CompletableFuture<String> cf = new CompletableFuture<>();
channel.read(buf, null, new CompletionHandler<>() {
    public void completed(Integer n, Void a) { cf.complete("ok"); }
    public void failed(Throwable ex, Void a) { cf.completeExceptionally(ex); }
});
cf.thenApply(String::toUpperCase);
```

**Listing 1.** Purpose #2: complete from a callback. Purpose #1: `thenApply` without blocking the I/O thread on `get`.

```d2
direction: down
start: "supplyAsync / complete" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
pipe: "thenApply / thenCompose" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
wait: "join only if this thread needs T" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
start -> pipe -> wait
```

**Fig. 1.** For **orchestration**. Blocking is optional and explicit.

> [!warning] It is not “never block the main thread”
> Any caller who **`join`s** waits. Heavy work on the **common pool** can stall **other** Fork/Join tasks.

> [!warning] Not a progress API
> You get **done / value / exception**, not percent-complete notifications.

> [!tip] Interview answer
> CompletableFuture is for chaining async steps and for completing a future from a callback. I use thenCompose when the next step returns a future, and I only join when this thread needs the value. It does not replace a thread pool or make get non-blocking.
