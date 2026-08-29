<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS

# How would you explain the Future interface in java.util.concurrent?

> [!abstract] Short answer
> A **`Future<V>`** is a **handle** for the result of an **asynchronous computation**. **`get()`** **blocks** until the value is ready (timed `get` may throw **`TimeoutException`**). **`isDone()`** is true after **success, exception, or cancel**. **`cancel(mayInterruptIfRunning)`** tries to stop unfinished work; if the task **already completed**, cancel has **no effect**. **`true`** means: **interrupt** the runner **if the implementation knows that thread**. Task failure is **`ExecutionException`** from `get`, not a normal return. This style does **not** compose (`thenApply`) — that is **`CompletableFuture`**. Wrapper: [[How would you explain FutureTask in Java concurrency]]. `Callable`: [[How would you explain the Callable interface in Java]].

## Check, wait, cancel

You usually obtain a `Future` from **`ExecutorService.submit`**. That **extends `execute`** by returning this handle — [[What is the difference between submit and execute on an executor service]]. You can also **`execute` a `FutureTask`**. Computation actions **happen-before** actions after the matching **`get()`**.

**`isCancelled()`** is true only if cancelled **before normal completion**. **`cancel`’s boolean return** is **not** a reliable “now cancelled” — use **`isCancelled()`**. **`Future<?>`** plus **`null`** is the documented cancellable-no-value shape. Since 19: **`state()`**, **`resultNow()`**, **`exceptionNow()`** for a future you **already know** is done (`IllegalStateException` otherwise). **`CompletableFuture`** implements `Future` and adds stages — [[How would you explain CompletableFuture for composing async work]]. Both: [[What are Future and CompletableFuture for in Java]]. Interrupt while waiting on `get`: [[How would you explain InterruptedException in Java threads]].

```java
Future<String> f = executor.submit(() -> "ok");
if (!f.isDone()) { /* still running or not started */ }
String s = f.get();
```

**Listing 1.** Interface usage: poll `isDone` if you want, then `get`. `get` is the wait.

```d2
direction: down
f: "Future" {
  width: 120
  height: 36
  style.fill: "#e3f2fd"
}
run: "task running" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
done: "isDone: success / fail / cancel" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
f -> run: "submit"
run -> done
```

**Fig. 1.** The interface does not start work. Completeness includes failure.

> [!warning] `cancel(true)` is an interrupt request
> The runner is interrupted **only if known**. The task must **honor** interrupt. `cancel` after completion does **not** rewind the computation.

> [!warning] `isDone` is not “succeeded”
> Exceptional completion and cancellation still set **`isDone`**. Always `get` (or `state` / `exceptionNow`) if you need **how** it finished.

> [!tip] Interview answer
> Future is the result handle for async work: get blocks, isDone means finished in any way, cancel tries to stop what has not finished. cancel(true) may interrupt the worker if the implementation knows the thread. Composition is CompletableFuture, not this interface.
