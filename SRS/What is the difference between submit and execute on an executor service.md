<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# What is the difference between submit and execute on an executor service?

> [!abstract] Short answer
> **`execute(Runnable)`** lives on **`Executor`**: run this **later**, return **`void`**. **`submit`** lives on **`ExecutorService`**: same scheduling, plus a **`Future`**. **`submit(Callable)`** → **`get()`** is the value. **`submit(Runnable)`** → **`get()` is `null`** (or a supplied result). Default wrap is **`FutureTask`**, then **`execute`**. **Exceptions:** `execute` can hit the **uncaught handler**; **`submit` swallows them into the `Future`** (`ExecutionException` on **`get()`**). Task types: [[What task types can you submit to an ExecutorService]]. Wrapper: [[How would you explain FutureTask in Java concurrency]]. `Runnable` vs `Callable`: [[What is the difference between Runnable and Callable in Java]]. Pool: [[How would you explain ThreadPoolExecutor]]. Uncaught `run`: [[What happens when an uncaught exception escapes a thread run method]].

## Void fire vs a handle

`AbstractExecutorService.submit` is **`newTaskFor` + `execute`**. Both throw **`RejectedExecutionException`** (and **NPE** on null). Work **before** submit **happens-before** the task, which **happens-before** a successful **`get()`**.

You do **not** `submit` just to “use the pool.” **`execute` already does.** Use **`submit`** for a **result**, **cancel**, or **`isDone`**. On **`ThreadPoolExecutor`**, **`afterExecute`** sees throws from **`execute`**. Tasks from **`submit`** **catch** inside **`FutureTask`**, so **`afterExecute`’s `Throwable` is null** unless you unwrap the `Future`.

```java
ExecutorService pool = Executors.newSingleThreadExecutor();
pool.execute(() -> { throw new RuntimeException(); }); // worker / handler
Future<?> f = pool.submit(() -> { throw new RuntimeException(); });
f.get(); // ExecutionException; worker stays up
pool.shutdown();
```

**Listing 1.** Same boom, different delivery. `execute` has no `get()`.

```d2
direction: down
ex: "execute: void" {
 width: 160
 height: 36
 style.fill: "#fff8e1"
}
sub: "submit: Future" {
 width: 160
 height: 36
 style.fill: "#e8f5e9"
}
ex -> sub: "newTaskFor then execute"
```

**Fig. 1.** `submit` is `execute` plus a `Future`. The wrapper is why throws stay off the uncaught path.

> [!warning] `execute` is not on `ExecutorService` only
> It is the **`Executor`** method. `ExecutorService` **adds** `submit` / shutdown / `invokeAll`.

> [!warning] A thrown `submit` task looks “fine” until `get`
> If you never **`get()`**, you **lose** the exception. `execute` failures are **visible** sooner (handler / `afterExecute`).

> [!tip] Interview answer
> execute runs a Runnable and returns void. submit wraps the work in a Future so I can get a result, cancel, or wait. Failures from submit show up as ExecutionException on get, not as an uncaught exception on the worker.
