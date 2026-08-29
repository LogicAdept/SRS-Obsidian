<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #OperatingSystems #SRS

# What is cooperative multitasking and which model does Java use?

> [!abstract] Short answer
> **Cooperative** (non-preemptive) multitasking: a task **runs until it yields** or blocks; the runtime/OS does **not** forcibly take the CPU away. **Java platform threads** are **OS threads**: the **OS scheduler** assigns them to cores (typically **preemptive** time-sharing). **Virtual threads** are **M:N** on **carriers**; the JDK scheduler **does not** ask your code to **yield**, so they are **not cooperative**. They **unmount** on many **blocking** JDK calls. The JDK **does not time-share** virtual threads (no CPU quantum preemption among VTs). Green threads: [[What are green threads and does the JVM use them]]. VTs: [[How would you explain Virtual Threads]]. `yield`: [[What is the difference between Thread.sleep and Thread.yield]]. Priority: [[Can thread priority reliably control execution order in Java]].

## Preempt the carrier, unmount the virtual thread

**Cooperative** systems starve if one task never yields. **`Thread.yield()`** is only a **heuristic** for platform threads, not a cooperative kernel.

**Platform `Thread`:** 1:1 kernel thread; **preemption is the OS’s job**. Java **priority** is a hint.

**Virtual `Thread`:** the JDK mounts it on a **carrier** (`ForkJoinPool` FIFO scheduler). App code **must not** assume when it moves carriers. **CPU-bound** virtual threads can **occupy a carrier** until they block, because there is **no** VT time-sharing. That is why VTs are for **mostly-blocked** work, not long tight loops.

```java
Thread.ofPlatform().start(() -> spin());  // OS can preempt this kernel thread
Thread.ofVirtual().start(() -> spin());   // may hold a carrier until it blocks
Thread.yield();                           // hint, not cooperative scheduling
```

**Listing 1.** Java does not require `yield()` for correctness. A CPU loop on a virtual thread is a poor fit.

```d2
direction: down
coop: "cooperative: run until yield" {
  width: 240
  height: 40
  style.fill: "#ffebee"
}
pt: "platform: OS preempts" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
vt: "virtual: unmount on block" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
coop -> pt: "not Java platform threads"
coop -> vt: "JEP: VTs are not cooperative"
```

**Fig. 1.** Cooperative = explicit hand-back. Java’s `Thread` models are **not** that contract.

> [!warning] Virtual threads are not “green cooperative threads”
> Early Java **M:1** green threads shared **one** OS thread. VTs are **M:N** and **do not** expect you to yield.

> [!warning] No time-sharing among virtual threads (Java 21 model)
> A long CPU burst on a VT **does not** get a quantum that switches to another VT. Block or don’t use VTs for that work.

> [!tip] Interview answer
> Cooperative multitasking means a task keeps the CPU until it yields. Java platform threads are scheduled by the OS, which is preemptive. Virtual threads are not cooperative either: you do not yield, they unmount when they block, and they are not time-sliced among themselves.
