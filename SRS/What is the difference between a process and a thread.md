<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #OperatingSystems #SRS

# What is the difference between a process and a thread?

> [!abstract] Short answer
> A **process** is an OS **isolated execution environment** with its **own memory space**. A **thread** runs **inside a process** and **shares** that process’s memory and open files. Threads are **cheaper to create**. Java work is **almost always threads** in **one JVM process**; extra OS processes take **`ProcessBuilder`**. JVM threads share the **heap**; each has a **private** pc and **JVM stack**. OS vs Java thread: [[What is the difference between an OS process and a Java thread]]. Composition: [[What are Java threads composed of]]. VTs: [[How would you explain Virtual Threads]]. Green vs 1:1: [[What are green threads and does the JVM use them]]. Fundamentals: [[How would you explain multithreading fundamentals in Java]].

## Isolated address space vs shared heap

**Process:** private resources; talk to another process with **IPC** (pipes, sockets). **Most JVMs are one process.** `ProcessBuilder.start()` creates a **new OS process** (new address space), not a `Thread`.

**Thread:** every process has **at least one**. The JVM starts **`main`**, plus **runtime** threads (GC, etc.). **`Thread.start()`** (platform or virtual) stays in **this** process. **Platform** threads are **OS threads** (1:1). **Virtual** threads are still **`Thread`s** in the **same** JVM: they **share the heap**; they are **not** child processes.

**Why interviews care:** two threads can **race** on the same object. Two processes **cannot** see each other’s heap without IPC or shared memory the OS provides.

```java
new Thread(() -> shared.n++).start();          // same heap; needs happens-before
new ProcessBuilder("echo", "hi").start();      // new process; no shared Java objects
```

**Listing 1.** `start()` on `Thread` vs `ProcessBuilder`. The second does not share `shared`.

```d2
direction: down
proc: "OS process / JVM" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
heap: "shared heap" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
t1: "thread: private stack" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
t2: "thread: private stack" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
proc -> heap
proc -> t1
proc -> t2
t1 -> heap
t2 -> heap
```

**Fig. 1.** Threads share the process heap. Stacks (and pc) stay per thread.

> [!warning] Killing the process kills every thread
> A `Thread` is not a sandbox. Isolation between apps is **processes** (or another JVM), not extra threads.

> [!warning] Shared memory is the feature and the bug
> Cheap communication is why you need **`synchronized` / `volatile` / j.u.c.** Processes do not get that for free.

> [!tip] Interview answer
> A process has its own address space; a thread lives inside a process and shares that memory. In Java you almost always start threads in one JVM process, and they share the heap but keep private stacks. A new OS process is ProcessBuilder, not new Thread, and virtual threads are still in the same process.
