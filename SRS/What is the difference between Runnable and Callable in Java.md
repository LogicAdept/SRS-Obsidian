<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS

# What is the difference between Runnable and Callable in Java?

> [!abstract] Short answer
> **`Runnable`:** **`void run()`** — no result, **no checked exceptions**. Pass it to **`Thread`**, **`Executor.execute`**, or **`submit`**. **`Callable<V>`:** **`V call()`** — a result, and **`call` may throw `Exception`**. There is **no `Thread(Callable)`** constructor. Submit with **`ExecutorService.submit(Callable)`** (or wrap in **`FutureTask`**, which **is** a `Runnable`). **`Future.get()`** returns the value or **`ExecutionException`** (cause = what `call` threw). `Runnable`: [[How would you explain the Runnable interface in Java]]. `Callable`: [[How would you explain the Callable interface in Java]]. Same pair: [[What is the difference between Runnable and Callable in Java]]. `submit` vs `execute`: [[What is the difference between submit and execute on an executor service]]. Tasks: [[What task types can you submit to an ExecutorService]]. `FutureTask`: [[How would you explain FutureTask in Java concurrency]]. `Future`: [[How would you explain the Future interface in java.util.concurrent]].

## `run` vs `call`

Both are **functional** task types, not threads. **`execute(runnable)`** fires and forgets. **`submit(runnable)`** still gives a **`Future<?>`** whose successful **`get()` is `null`**. **`submit(callable)`** is how you get **`V`**. **`Executors.callable(runnable, result)`** adapts a `Runnable`. An uncaught throw from **`run()`** on a raw **`Thread`** hits the **uncaught handler** and **ends that thread**. A throw from **`call()`** is **stored** until **`get()`**.

```java
ExecutorService pool = Executors.newSingleThreadExecutor();
pool.execute(() -> {});                          // Runnable
Future<?> f1 = pool.submit(() -> {});            // Runnable; get() -> null
Future<Integer> f2 = pool.submit(() -> 1 + 1);   // Callable
new Thread(() -> {}).start();                    // Runnable only
new Thread(new FutureTask<>(() -> 1)).start();   // Callable via FutureTask
pool.shutdown();
```

**Listing 1.** Lambdas: no result → `Runnable`; result (or `throws`) → `Callable`. `Thread` still wants a `Runnable`.

```d2
direction: down
r: "Runnable.run(): void" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
c: "Callable.call(): V" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
t: "Thread / execute" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
f: "submit -> Future" {
  width: 160
  height: 36
  style.fill: "#ffebee"
}
r -> t
r -> f
c -> f
```

**Fig. 1.** `Callable` needs a `Future` (or a `FutureTask` on a `Thread`). `Runnable` can go either way.

> [!warning] `Thread` does not accept `Callable`
> Wrap with **`FutureTask`** or use an **executor**. `new Thread(callable)` does not compile.

> [!warning] Checked exceptions
> `run()` cannot declare them. `call()` can. Do not catch-and-ignore inside `call` if the caller will **`get()`**.

> [!tip] Interview answer
> Runnable is void run with no checked exceptions, so Thread and execute can take it. Callable is call that returns a value and may throw Exception, so I submit it and get a Future. There is no Thread constructor for Callable; I wrap it in FutureTask if I must start a raw Thread.
