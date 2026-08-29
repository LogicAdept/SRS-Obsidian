<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS

# What task types can you submit to an ExecutorService?

> [!abstract] Short answer
> **`Executor.execute`:** **`Runnable`** only, **no** `Future`. **`submit`:** **`Runnable`** (`get()` → **`null`**), **`Runnable` plus a result `T`**, or **`Callable<T>`** (`get()` → **`call()`’s value**). **`invokeAll` / `invokeAny`:** a **collection of `Callable`s**. Wrap other work in **`FutureTask`** (it **is** a `Runnable`) or **`Executors.callable`**. `submit` vs `execute`: [[What is the difference between submit and execute on an executor service]]. `Runnable` vs `Callable`: [[What is the difference between Runnable and Callable in Java]]. Wrapper: [[How would you explain FutureTask in Java concurrency]]. `Callable`: [[How would you explain the Callable interface in Java]]. Factories: [[How would you explain Executors]]. Pool: [[How would you explain ThreadPoolExecutor]].

## `Runnable`, `Callable`, and bulk `Callable`s

A **lambda** is a **`Callable`** when it **returns a value** (or is typed that way); **`void`** is a **`Runnable`**. **`execute`** cannot take a **`Callable`**. Default **`submit`** wrapping is **`FutureTask`**, then **`execute`**. Both reject **`null`** and throw **`RejectedExecutionException`** if the executor will not take the task.

**`ForkJoinPool`** is an **`ExecutorService`** and also accepts **`ForkJoinTask`**. **`ScheduledExecutorService`** adds **delayed / periodic** `Runnable`/`Callable` — still those two task types.

```java
ExecutorService pool = Executors.newSingleThreadExecutor();
pool.execute(() -> {});
Future<?> f0 = pool.submit(() -> {});
Future<String> f1 = pool.submit(() -> {}, "ok");
Future<Integer> f2 = pool.submit(() -> 1);
List<Future<Integer>> all = pool.invokeAll(List.of(() -> 1, () -> 2));
pool.shutdown();
```

**Listing 1.** `execute` plus the three `submit` shapes, then bulk `Callable`s.

```d2
direction: down
r: "Runnable" {
  width: 120
  height: 36
  style.fill: "#fff8e1"
}
c: "Callable<V>" {
  width: 130
  height: 36
  style.fill: "#e8f5e9"
}
ex: "execute" {
  width: 100
  height: 36
  style.fill: "#e3f2fd"
}
sub: "submit / invokeAll" {
  width: 180
  height: 36
  style.fill: "#ffebee"
}
r -> ex
r -> sub
c -> sub
```

**Fig. 1.** `Callable` needs `submit` (or a `FutureTask` passed to `execute`).

> [!warning] No `Thread` as a task type
> You submit **work**, not a **`Thread` subclass** you then `start`. The **pool** owns the workers.

> [!warning] `submit(Runnable)` still returns a `Future`
> Success is **`null`**, not “no handle.” Failures wait in **`get()`** as **`ExecutionException`**.

> [!tip] Interview answer
> ExecutorService takes Runnable on execute and submit, and Callable on submit. There is also submit of a Runnable with a result value, and invokeAll of a collection of Callables. I wrap other APIs with FutureTask or Executors.callable if I need a Future.
