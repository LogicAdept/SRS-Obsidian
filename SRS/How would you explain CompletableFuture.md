<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS

# How would you explain `CompletableFuture`?

> [!abstract] Short answer
> **`CompletableFuture<T>`** (Java 8) is a **`Future`** whose result can be set **manually** and a **`CompletionStage`** that chains dependent steps. Internally it holds one **`result`** slot and a **stack of dependent callbacks**; the **first** completion — value, exception, or cancel — wins, and every registered dependent is then **posted**. A **non-async** dependent may run **inline on the thread that completed** the stage; `*Async` variants without an explicit executor use **`ForkJoinPool.commonPool()`** (or a fresh thread per task if its parallelism is below two). Definition: [[What is CompletableFuture]]. Purpose: [[What is CompletableFuture for]].

## Completion and dependents

A fresh `CompletableFuture` is **incomplete**. **`complete(value)`**, **`completeExceptionally(ex)`**, and **`cancel(...)`** all try to fill the single result slot: exactly **one** of them wins, the others return **`false`**. Dependents registered earlier (by `thenApply`, `thenCompose`, `whenComplete`, …) sit in an internal **stack of `Completion` nodes**; when the result lands, each dependent is **posted** — a **non-async** one may execute **on the thread that called the completion method** or on **any other caller of a completion method**. That is why an innocent-looking `thenApply` can suddenly run on your network thread. With **`thenApplyAsync(fn, executor)`** you pin the step to the executor you chose.

Blocking readers still work: **`get()`** waits and throws checked exceptions; **`join()`** throws the unchecked **`CompletionException`** instead. On exceptional completion, `get` wraps the cause in **`ExecutionException`**, while `join`/`getNow` throw the **`CompletionException`** directly. **`cancel`** is documented as **`completeExceptionally(new CancellationException())`** — it does **not** interrupt a running supplier, because the future does not own that thread.

```java
var cf = new CompletableFuture<String>();
// another thread publishes the result:
executor.execute(() -> cf.complete(client.call()));
cf.thenApply(String::trim)
  .thenAccept(System.out::println); // runs when completion lands
```

**Listing 1.** One producer completes the stage; the registered dependent fires when the result arrives — or immediately if it already has.

```d2
direction: down
incomplete: "Incomplete\nresult slot empty" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
try: "complete / completeExceptionally / cancel" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
winner: "First call wins\nothers return false" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
post: "Post dependents\n(thenApply, thenCompose, ...)" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
inline: "non-async:\ncompleting thread" {
  width: 220
  height: 70
  style.fill: "#fff8e1"
}
pool: "Async variant:\ncommonPool or given executor" {
  width: 280
  height: 80
  style.fill: "#fff8e1"
}
blocked: "get / join\nwaiters released" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
incomplete -> try
try -> winner
winner -> post
winner -> blocked
post -> inline
post -> pool
```

**Fig. 1.** Single completion, then the dependent stack is drained; where a non-async dependent runs is deliberately unspecified — pin it with `*Async`.

## Chaining and error flow

Dependent stages also fire only on the matching outcome: `thenApply` runs **only on normal completion**; when the stage completes exceptionally, the exception **propagates** to dependent stages and they complete exceptionally too, until a recovery method — **`exceptionally`**, **`handle`**, or **`whenComplete`** — absorbs it. The three composition tools are compared in [[How would you explain CompletableFuture thenApply vs thenCompose vs thenCombine]]; larger pipelines live in [[How would you explain CompletableFuture for composing async work]].

> [!warning] Cancel does not stop the work
> The popular lie is "`cancel(true)` interrupts the task." For a `CompletableFuture`, cancel is just **exceptional completion**; the running lambda keeps burning its thread. Interruption belongs to the executor that owns the thread — see [[How would you explain the Future interface in java.util.concurrent]] for the `FutureTask` contrast.

> [!example] Default executor nuance
> Every `*Async` method without an explicit executor uses **`ForkJoinPool.commonPool()`** — but if the common pool's parallelism is **below two** (e.g. a 1-CPU machine), the Javadoc promises a **new thread per task** instead. Subclasses can also override **`defaultExecutor()`**. See [[What is the Java ForkJoin framework]].

> [!tip] Interview answer
> **`CompletableFuture` pairs a `Future` you can complete by hand with a `CompletionStage` for chaining. One result slot, one winner; dependents are kept in a stack and posted on completion — non-async ones may run right on the completing thread, while `Async` variants default to the common ForkJoin pool. `join` throws `CompletionException`, `get` wraps the cause in `ExecutionException`, and cancel merely completes exceptionally — it never interrupts the running task.**
