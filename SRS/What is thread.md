<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What is thread?

> [!abstract] Short answer
> A **Java thread** is a **`java.lang.Thread`**: a **thread of execution** with a **private** pc and **JVM stack**, sharing the **heap**. **`start()`** (or an **executor**) **schedules** `run` **concurrently**. **Platform** threads wrap **OS** threads; **virtual** threads are still **`Thread`s**, **M:N** on **carriers**. **Thread-safety** is a **different** question: shared mutable state needs **happens-before**. **Daemon** threads do **not** delay JVM **shutdown** (all **started non-daemon** threads have **terminated**). Fundamentals: [[How would you explain multithreading fundamentals in Java]]. Stacks: [[What are Java threads composed of]]. Process: [[What is the difference between a process and a thread]]. `start` vs `run`: [[What is the difference between Thread start and run]]. VTs: [[How would you explain Virtual Threads]]. Daemons: [[How would you explain daemon threads in Java]]. Safety: [[How would you explain thread safety for shared mutable state]].

## Execution, not a process

**`Thread` implements `Runnable`.** Prefer **`new Thread(task).start()`**. **`run()`** on the caller is **not** a start. Shared objects **race** without **`synchronized` / `volatile` / atomics / j.u.c.**

**Daemon:** **`setDaemon(true)` before `start`**. After the thread is **alive**, **`IllegalThreadStateException`**. **Virtual** threads are **always** daemon (`setDaemon(false)` → **`IllegalArgumentException`**). Shutdown starts when **every started non-daemon** thread has **ended** — **not** “when `main` returns” if other non-daemon workers still run. Unstarted non-daemon threads do **not** hold the VM open.

```java
Thread t = new Thread(() -> work(), "worker");
t.setDaemon(true); // before start; VT is already daemon
t.start();
```

**Listing 1.** A thread is the worker. Daemon is a **JVM-lifetime** flag, not “background = safe.”

```d2
direction: down
t: "Thread of execution" {
 width: 180
 height: 36
 style.fill: "#e8f5e9"
}
st: "private stack" {
 width: 140
 height: 36
 style.fill: "#e3f2fd"
}
h: "shared heap" {
 width: 120
 height: 36
 style.fill: "#fff8e1"
}
t -> st
t -> h
```

**Fig. 1.** One thread, private stack, shared objects.

> [!warning] Thread-safety is not the definition of a thread
> A **thread-safe counter** is an object that stays correct under concurrent use. A **`Thread`** is the **runner**.

> [!warning] `main` returning does not kill user workers
> Other **non-daemon** threads **keep the JVM**. Daemons **do not** delay the shutdown sequence.

> [!tip] Interview answer
> A thread is a Thread object: sequential code the JVM can run at the same time as other threads, with its own stack and a shared heap. I start it with start or an executor, not by calling run. Daemon threads do not keep the JVM alive, and virtual threads are always daemon.
