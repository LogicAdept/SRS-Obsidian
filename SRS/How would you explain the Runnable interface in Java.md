<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How would you explain the Runnable interface in Java?

> [!abstract] Short answer
> **`Runnable`** is a **functional** interface: **`void run()`** — an operation that **returns no result**. You pass an instance (or a lambda) to a **`Thread`**, an **`Executor.execute`**, or a **`FutureTask`**. **`Thread` itself implements `Runnable`**. **`run()`** is the **body**; **`Thread.start()`** is what **schedules** a new thread. Calling **`run()`** yourself runs it on the **current** thread. Vs `Thread` subclass: [[What is the difference between Thread and Runnable in Java]]. Vs `Callable`: [[What is the difference between Runnable and Callable in Java]]. Start vs `run`: [[What is the difference between Thread start and run]].

## Task type, not a thread

Prefer **composition**: `new Thread(work).start()` or `pool.execute(work)` over subclassing `Thread` just to override `run`. **`Executor.execute`** may run the `Runnable` in a **new** thread, a **pool** thread, or the **caller**. **`submit(Runnable)`** still wraps a **`Future`** whose **`get()`** is **`null`** on success — [[How would you explain the ExecutorService interface in Java]]. **`Callable.call()`** returns a value and may throw **checked** exceptions — [[How would you explain the Callable interface in Java]]. Creating threads: [[How do you create a thread in Java]]. Virtual-thread `Thread.run()` **does nothing** if invoked directly.

```java
Runnable work = () -> System.out.println(Thread.currentThread().getName());
new Thread(work, "worker").start();
```

**Listing 1.** The lambda is a `Runnable`. `start` runs `work.run` concurrently. `work.run()` would print the **caller**.

```d2
direction: down
r: "Runnable.run()" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
t: "Thread.start()" {
  width: 160
  height: 36
  style.fill: "#e8f5e9"
}
e: "Executor.execute" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
r -> t: "new concurrent thread"
r -> e: "pool / caller / new"
```

**Fig. 1.** `Runnable` is the work. Something else decides **which** thread runs it.

> [!warning] `run()` is not `start()`
> Invoking `run` on a `Thread` (platform + task) executes the `Runnable` **here**. That is not a second thread of execution.

> [!warning] No result, no checked exceptions
> `run` cannot `return` a value or `throws IOException`. Use **`Callable`** + **`submit`** when you need either.

> [!tip] Interview answer
> Runnable is the void task type: one method run, no result. I pass it to a Thread or an executor instead of subclassing Thread. I call start or execute, not run, when I want concurrency, and I use Callable when the work must return a value.
