<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What is the difference between Thread and Runnable in Java?

> [!abstract] Short answer
> **`Thread`** is a **thread of execution** (and a class that **`implements Runnable`**). **`Runnable`** is the **task**: **`void run()`**. The JDK shows **two** starts: **subclass `Thread` and override `run`**, or **`new Thread(runnable).start()`**. Prefer the **`Runnable`**: one class, **composition**, works with **`Executor.execute`**, **lambdas**, **virtual threads**. **`start()`** schedules; **`run()`** on the caller is **not** a start. `Runnable`: [[How would you explain the Runnable interface in Java]]. Create: [[How do you create a thread in Java]]. `start` vs `run`: [[What is the difference between Thread start and run]]. Vs `Callable`: [[What is the difference between Runnable and Callable in Java]]. VTs: [[How would you explain Virtual Threads]]. OS thread: [[What is the difference between an OS process and a Java thread]].

## Worker object vs work item

**`Thread`:** lifecycle (`start`, `join`, interrupt, name, daemon, platform vs virtual). **Platform** threads wrap **OS** threads; **virtual** threads are still **`Thread`**, not a second type of `Runnable`. Subclassing `Thread` spends your **one** superclass on the worker.

**`Runnable`:** only **`run`**. Pass the **same** task to a **pool**, a **platform** thread, or **`Thread.ofVirtual().start(task)`**. **`Thread` already is a `Runnable`** — do **not** `new Thread(existingThread)` expecting two workers; you would **`run` the `Thread` object’s `run`**, which is easy to get wrong.

```java
class Worker extends Thread {
  public void run() { work(); }
}
new Worker().start();

Runnable task = () -> work();
new Thread(task).start();
pool.execute(task);
```

**Listing 1.** Official two styles, then reuse the **same** `Runnable` on a pool. `task.run()` would run on the **caller**.

```d2
direction: down
r: "Runnable.run(): the work" {
  width: 220
  height: 36
  style.fill: "#e8f5e9"
}
t: "Thread.start(): the worker" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
r -> t: "pass task into Thread or Executor"
```

**Fig. 1.** Separate **what to run** from **which thread runs it**.

> [!warning] `run()` is not `start()`
> `thread.run()` executes **`run` on this thread**. No second thread of execution.

> [!warning] Extending `Thread` is optional
> Override **`run`** if you subclass. You do not get a thread by implementing `Runnable` until **something calls `start`/`execute`**.

> [!tip] Interview answer
> Thread is the worker; Runnable is the task with void run. I pass a Runnable into a Thread or an executor instead of subclassing Thread, so I can reuse the task and keep my superclass free. start schedules that run on another thread; calling run myself does not.
