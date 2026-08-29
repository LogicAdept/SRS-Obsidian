<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #OperatingSystems #SRS

# What is the difference between a thread a task and a process?

> [!abstract] Short answer
> A **process** is an OS **isolated address space**. A **thread** is an **execution** inside that process (**shared heap**, private stack). A **task** is **work** (`Runnable` / `Callable` / `ForkJoinTask`) you **submit** — it is **not** a thread. A pool **runs many tasks on fewer workers**. Extra OS processes: **`ProcessBuilder`**, not `new Thread`. Process vs thread: [[What is the difference between a process and a thread]]. OS vs Java thread: [[What is the difference between an OS process and a Java thread]]. Submit what: [[What task types can you submit to an ExecutorService]]. `Runnable`: [[How would you explain the Runnable interface in Java]]. Pools: [[What is pool threads]], [[How would you explain thread pools and executor frameworks in Java]]. `FutureTask`: [[How would you explain FutureTask in Java concurrency]]. VTs: [[How would you explain Virtual Threads]].

## Isolation, execution, work item

**Process:** own memory; IPC to talk; **most JVMs are one process**. Killing it kills every Java thread.

**Thread:** `Thread.start()` (platform ≈ **OS thread**; **virtual** still a `Thread` in **this** JVM). Many threads share objects — that is why you synchronize.

**Task:** `execute` / `submit` a `Runnable` or `Callable`. The **`Executor` may run it** on a **new** thread, a **pooled** thread, or even the **caller**. **`FutureTask`** is a **task object** (`RunnableFuture`), not a process. **`ForkJoinTask`** is a **subdividable** task on a **`ForkJoinPool`**. Virtual-thread executors often use **one thread per task**; that still does **not** make a task a process.

```java
Runnable task = () -> work();
new Thread(task).start();                 // dedicate a thread to this task
exec.submit(task);                        // same work; worker may be reused
new ProcessBuilder("echo", "hi").start(); // new OS process
```

**Listing 1.** Same `Runnable`, three lifetimes. Only `ProcessBuilder` leaves the JVM’s address space.

```d2
direction: down
proc: "process / JVM" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
th: "threads (workers)" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
task: "tasks: Runnable / Callable" {
  width: 220
  height: 36
  style.fill: "#e8f5e9"
}
proc -> th
th -> task: "run submitted work"
```

**Fig. 1.** Tasks queue onto threads. Threads live in one process.

> [!warning] A task is not a `Thread`
> Submitting 10,000 tasks to a **fixed** pool does **not** start 10,000 OS threads. It **queues** work.

> [!warning] `new Thread(task)` is not a process
> You still share the **heap**. Isolation is a **new process** (or a **new JVM**).

> [!tip] Interview answer
> A process has its own address space, a thread runs inside a process and shares memory, and a task is just a unit of work you submit. In Java I start threads with Thread or an executor, and I start a new OS process with ProcessBuilder. A thread pool runs many tasks on fewer workers; the task is not the worker.
