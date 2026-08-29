<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #OperatingSystems #SRS

# Where do operating system threads come from in an application?

> [!abstract] Short answer
> From the **OS**, when something in **this process** creates a **kernel thread**. In **Java**, that is each **platform** `Thread` (**1:1 wrapper**) plus **JVM runtime** threads (GC, signals, …). **`Thread.start()`** on a **platform** thread **captures** an OS thread for life. **Virtual** threads do **not** each own one: the JDK mounts them on **carrier** platform threads (a **`ForkJoinPool`**). **`ProcessBuilder.start()`** is a **new process**, not another OS thread in **this** JVM. OS vs Java thread: [[What is the difference between an OS process and a Java thread]]. VTs: [[How would you explain Virtual Threads]]. Green vs 1:1: [[What are green threads and does the JVM use them]]. Unit of scheduling: [[What is the smallest schedulable unit of work in Java threads]]. Pools: [[What is pool threads]]. Process: [[What is the difference between a process and a thread]].

## Platform start, carriers, not `new Thread` of a process

The **kernel** does not spawn threads because you wrote a **`Runnable`**. It spawns them when the **runtime** (or **native** code) calls the **thread syscall**. **`Executors.newFixedThreadPool(n)`** holds **n** platform workers → about **n** OS threads (plus JVM internals). **`newCachedThreadPool()`** can grow **unbounded** OS threads. **10,000 virtual** tasks still share **few** carriers.

**Native** libraries may create OS threads of their own; they are **not** `java.lang.Thread` until attached. The OS **does not see** virtual `Thread` objects — only **busy carriers**.

```java
Thread.ofPlatform().start(() -> work());  // one OS thread, captured
Thread.ofVirtual().start(() -> work());   // OS sees a carrier, not this Thread
new ProcessBuilder("echo", "hi").start(); // other process
```

**Listing 1.** Only the first line is “give me a dedicated OS thread for this Java thread.”

```d2
direction: down
app: "Java application / JVM process" {
  width: 260
  height: 36
  style.fill: "#fff8e1"
}
pt: "platform Thread.start" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
rt: "JVM runtime threads" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
os: "OS threads" {
  width: 120
  height: 36
  style.fill: "#ffebee"
}
app -> pt
app -> rt
pt -> os
rt -> os
```

**Fig. 1.** OS threads are created **in this process** by the JVM (and native code), not by `ProcessBuilder`.

> [!warning] Virtual threads are not OS threads
> Counting **`Thread` objects** (or tasks) **overcounts** kernel threads.

> [!warning] The JVM already has OS threads before `main`
> You do not start from zero. GC and other **runtime** threads exist beside **`main`**.

> [!tip] Interview answer
> Operating system threads come from the kernel when the process creates them. In Java that is platform threads from Thread.start or a pool, plus JVM internal threads. Virtual threads reuse a small set of carrier OS threads, and a new process is ProcessBuilder, not another thread in this JVM.
