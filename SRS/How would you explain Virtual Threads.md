<!--
reps: 0
priority: 0
-->
#Java/Concurrency/VirtualThreads #SRS

# How would you explain Virtual Threads?

> [!abstract] Short answer
> A **virtual thread** is a **`Thread`** scheduled by the **Java runtime** (user mode), not 1:1 by the OS. It needs **few resources**; a JVM may run **millions**. A small pool of **platform carrier** threads actually runs them; on **blocking I/O or locking** the runtime can **move the carrier** to another virtual thread. **`Thread.currentThread()`** is always the virtual thread, never the carrier. Use them for **mostly-blocked** work, not long **CPU-heavy** loops. Always **daemon**; priority is **fixed**. Create with **`Thread.ofVirtual()`** or **`Executors.newVirtualThreadPerTaskExecutor()`**. Pinning / `synchronized`: [[How would you explain Virtual Threads synchronized]]. Daemons: [[How would you explain daemon threads in Java]]. Spring Boot: [[How do you enable virtual threads in Spring Boot]].

## Carriers, not a second `Thread` type you subclass

Platform threads map **1:1 to kernel threads**, with a **large OS stack**, priority, and a thread group — a **limited** resource, fine for **any** work. Virtual threads **reuse** a few of those as **carriers**. You still write ordinary blocking `Runnable` / `Callable` code; the scheduler unmounts while the task waits. That is the “blocking code that scales like async” story — not a new I/O API. `run()` invoked **directly** on a virtual `Thread` **does nothing**; you still **`start`**. Start vs `run`: [[What is the difference between Thread start and run]]. Per-task executor (unbounded VTs, not a platform pool): [[How would you explain thread pools and executor frameworks in Java]].

Virtual threads have **no default name** (`getName()` is `""`). They **do not** capture the creator’s access-control context. JDK scheduler knobs (reference implementation): carrier **parallelism** defaults to **available processors**; **max pool** of carriers defaults to **256**.

```java
Runnable task = () -> System.out.println(Thread.currentThread().isVirtual());
Thread vt = Thread.ofVirtual().name("io-1").start(task);
vt.join();
try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
    exec.submit(task);
}
```

**Listing 1.** Builder start, then an unbounded virtual-thread-per-task executor. `isVirtual()` is true; `currentThread()` is the VT.

```d2
direction: down
v: "many virtual threads" {
  width: 190
  height: 40
  style.fill: "#e3f2fd"
}
c: "few platform carriers" {
  width: 190
  height: 40
  style.fill: "#e8f5e9"
}
os: "OS kernel threads" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
v -> c: "mount / unmount on block"
c -> os: "1:1"
```

**Fig. 1.** Runtime multiplexes VTs onto carriers. Code sees the virtual `Thread`, not the carrier.

> [!warning] Always daemon, not a CPU pool
> Virtual threads **cannot** be made non-daemon; they do **not** keep the JVM alive. They are **not** meant for long-running CPU-bound work (they would occupy carriers).

> [!warning] `run()` on an unstarted virtual thread is a no-op
> Scheduling still requires **`start`** (or an executor that starts them). Subclassing `Thread` is the platform-thread constructors; use **`ofVirtual()`**.

> [!tip] Interview answer
> Virtual threads are lightweight Thread objects the JVM schedules on a few platform carrier threads, so I can keep writing blocking I/O instead of an async stack. They are always daemons and they are a bad fit for long CPU-bound work. I start them with Thread.ofVirtual or a virtual-thread-per-task executor, and I remember currentThread is the virtual thread, not the carrier.
