<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS

# How would you explain the Callable interface in Java?

> [!abstract] Short answer
> **`Callable<V>`** is a **one-method** task: **`V call()`** may **return a value** and may **throw a checked `Exception`**. It is meant to run **on another thread**, like **`Runnable`**, but **`Runnable.run()`** returns **`void`** and **cannot** throw checked exceptions. Submit it with **`ExecutorService.submit(Callable)`** (or wrap in a **`FutureTask`**). **`Thread` constructors do not take `Callable`.** Vs `Runnable`: [[What is the difference between Runnable and Callable in Java]]. Handle: [[How would you explain the Future interface in java.util.concurrent]]. Wrapper: [[How would you explain FutureTask in Java concurrency]].

## `call`, then `get`

`Executors` can turn a `Runnable` (plus an optional result), `PrivilegedAction`, etc. into a `Callable`. `AbstractExecutorService.submit` wraps the `Callable` in a **`RunnableFuture`** (default **`FutureTask`**) and **`execute`s** it. **`Future.get()`** returns **`call()`’s value**, or **`ExecutionException`** if `call` threw (cause is that throwable), or **`CancellationException`**, or **`InterruptedException`** if the **waiter** was interrupted. `execute(Runnable)` cannot express a result — [[What is the difference between submit and execute on an executor service]]. Same idea, other title: [[What is the difference between Runnable and Callable in Java]]. Creating threads: [[How do you create a thread in Java]].

```java
ExecutorService pool = Executors.newSingleThreadExecutor();
try {
    Future<Integer> f = pool.submit(() -> 1 + 1);
    int n = f.get();
} finally {
    pool.shutdown();
}
```

**Listing 1.** A lambda is a `Callable<Integer>` because `call` returns `int` and the lambda can throw. `get` waits for that result.

```d2
direction: down
c: "Callable.call()" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
p: "pool thread" {
  width: 140
  height: 36
  style.fill: "#fff8e1"
}
g: "Future.get()" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
c -> p: "submit"
p -> g: "value or ExecutionException"
```

**Fig. 1.** `Callable` is the task type. `Future` is the result slot. `Thread.start` is not in this picture.

> [!warning] Not a `Thread` constructor argument
> `new Thread(callable)` does not compile. Wrap with `FutureTask` and `start` that, or `submit` to an executor.

> [!warning] Checked exceptions are boxed on `get`
> `call()` may throw `Exception`. The pool thread does not have to declare it. The **caller of `get`** sees **`ExecutionException`**. If you never `get`, you can miss the failure.

> [!tip] Interview answer
> Callable is like Runnable but call returns a value and may throw a checked exception. I submit it to an ExecutorService and use Future.get for the result. I do not pass a Callable to a Thread constructor.
