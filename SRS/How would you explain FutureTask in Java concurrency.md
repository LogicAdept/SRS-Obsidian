<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS

# How would you explain FutureTask in Java concurrency?

> [!abstract] Short answer
> **`FutureTask`** is a **cancellable** computation that implements **`RunnableFuture`**: it is both a **`Runnable`** and a **`Future`**. Wrap a **`Callable`** (or a **`Runnable` plus a result**), **`run()`** it (yourself, on a `Thread`, or via an **`Executor`**), then **`get()`** the value. After completion you **cannot restart** it unless you use **`runAndReset()`**. `ThreadPoolExecutor.submit` typically wraps work in a `FutureTask` via `newTaskFor`. Unlike **`CompletableFuture`**, this object **owns** the run: **`cancel(true)`** may **interrupt** that worker. Interface: [[How would you explain the Future interface in java.util.concurrent]]. Vs CF: [[What are Future and CompletableFuture for in Java]]. `Callable`: [[How would you explain the Callable interface in Java]]. `submit` vs `execute`: [[What is the difference between submit and execute on an executor service]].

## Wrap, run, then get

Because it is a `Runnable`, `executor.execute(task)` and `new Thread(task).start()` both work; `submit` on `AbstractExecutorService` builds a `RunnableFuture` (default **`FutureTask`**) and returns it as a `Future`. Subclasses may override `newTaskFor` to swap the wrapper.

`isDone` is true after **normal finish, exception, or cancel**. `get` then returns the value, or throws **`ExecutionException`** (task threw), **`CancellationException`**, **`InterruptedException`** (waiter interrupted), or **`TimeoutException`** on the timed overload. `cancel(true)` asks to **interrupt** the runner if the implementation knows that thread; `cancel` has **no effect** once the task is already done. `done()` is a hook when the task becomes done (default no-op).

`runAndReset` runs **without** storing a result and returns the task to the **initial** state, for work that is meant to run **more than once**. Failed or cancelled runs do not reset. Style of “hand back a Future”: [[How would you explain the Future interface in java.util.concurrent]].

```java
ExecutorService pool = Executors.newSingleThreadExecutor();
try {
    FutureTask<Integer> task = new FutureTask<>(() -> 1 + 1);
    pool.execute(task);
    int n = task.get();
} finally {
    pool.shutdown();
}
```

**Listing 1.** Wrap a `Callable`, execute the `Runnable`, block on `get`. `pool.submit(callable)` does the wrap for you.

```d2
direction: down
wrap: "FutureTask(callable)" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
run: "run() on a worker" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
get: "get() on the caller" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
wrap -> run: "execute / start"
run -> get: "isDone, then result"
```

**Fig. 1.** One object is the task and the handle. `get` does not start it.

> [!warning] `get()` is still a blocking wait
> The caller parks until completion (or timeout). That is not `thenApply`. A failed `Callable` surfaces as `ExecutionException`, not as the raw cause. Do not `get` from a Fork/Join common-pool worker or you can **starve** the pool.

> [!warning] Done means done
> A finished `FutureTask` will not run again through `run()`. Use `runAndReset` only for the repeat-without-result case. `cancel` after completion does not rewind it.

> [!tip] Interview answer
> FutureTask is the concrete Future that is also Runnable, so you wrap a Callable and execute it on a thread or an executor. get blocks until the computation finishes or fails. Thread pools use it as the default wrapper from submit.
