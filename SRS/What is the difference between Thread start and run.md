<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What is the difference between Thread start and run?

> [!abstract] Short answer
> **`start()`** **schedules this `Thread`** to run **independently** of the caller. The JVM then executes **`run()`** on that thread. **`start` at most once**; a second call → **`IllegalThreadStateException`**. **`run()`** is **`Runnable`’s** body — **not** a start API. On a **platform** thread with a task, a direct `run()` runs that task on the **caller**. On a **virtual** thread, a direct `run()` **does nothing**. Create: [[How do you create a thread in Java]]. You cannot force-start: [[How do you forcibly start a Java thread]]. `Thread` vs `Runnable`: [[What is the difference between Thread and Runnable in Java]]. VTs: [[How would you explain Virtual Threads]]. Uncaught `run`: [[What happens when an uncaught exception escapes a thread run method]].

## Schedule versus invoke

Until **`start`**, the thread is **`NEW`**. After **`start`**, it is **`RUNNABLE`** (or a wait state) **on its own**. **`run()`** does **not** change that: no second execution, **`isAlive`** stays false if you never **`start`**. Subclass **`run`**, or pass a **`Runnable`**. Concurrency begins only at **`start()`** (or **`ofVirtual().start` / `startVirtualThread`**). When a core is assigned is the **scheduler’s** job.

```java
Runnable work = () -> System.out.println(Thread.currentThread().getName());
Thread t = new Thread(work, "worker");
t.run();    // caller, often "main"
t.start();  // "worker"
t.start();  // IllegalThreadStateException
```

**Listing 1.** `run` is a method call. `start` is the only start. Twice is illegal.

```d2
direction: down
st: "start(): new execution" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
rn: "run(): this thread" {
  width: 180
  height: 36
  style.fill: "#ffebee"
}
st -> rn: "JVM calls run on the new thread"
```

**Fig. 1.** You call `start`. The new thread calls `run`. You calling `run` skips the first step.

> [!warning] `start` does not mean “new OS thread” for every `Thread`
> **Platform** threads wrap OS threads. **Virtual** threads are still started with **`start`**, not by you calling **`run`**.

> [!warning] Virtual `run()` is a no-op if you invoke it
> Do not “test” a virtual thread by **`t.run()`**. Use **`start`**.

> [!tip] Interview answer
> start schedules a new thread of execution and the JVM runs run on that thread. run is just the task body; if I call it myself it runs on the current thread, or does nothing on a virtual thread. I can start a Thread only once.
