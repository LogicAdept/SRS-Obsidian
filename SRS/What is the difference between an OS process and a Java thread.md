<!--
reps: 0
priority: 0
-->
#OperatingSystems #Java/Concurrency/Threads #SRS

# What is the difference between an OS process and a Java thread?

> [!abstract] Short answer
> An **OS process** is an **isolated address space** (own memory, files, identity). A **Java thread** is a **`java.lang.Thread`** that runs **inside a JVM process** and **shares that process’s heap**. It is **not** a process. **Platform** threads are **thin wrappers around OS threads** (1:1, capture the OS thread for life). **Virtual** threads are still **`Thread`s**, but **not tied** to one OS thread; the **OS does not see them** — only **carriers**. Generic trio: [[What is the difference between a process and a thread]], [[What is the difference between a thread a task and a process]]. Stacks/heap: [[What are Java threads composed of]]. VTs: [[How would you explain Virtual Threads]]. Green vs 1:1: [[What are green threads and does the JVM use them]].

## Process isolation vs in-JVM execution

**Most JVMs are one OS process.** `ProcessBuilder.start()` starts **another** process: **no shared Java objects**. Threads in **this** JVM still share the **heap** and method area; each has a **private** pc and **JVM stack**.

**`java.lang.Thread` ≠ OS thread, always:**
- **Platform:** JDK **wrapper**; **one** Java thread **owns one** OS thread until it ends. Count is capped by what the **OS** will give you.
- **Virtual:** JDK **user-mode** `Thread`; **M:N** onto **platform carriers**. Cheap and plentiful; **native** code may see a **different** OS thread id after remount. **Not** a child process.

```java
Thread.ofPlatform().start(() -> work());  // one OS thread, captured
Thread.ofVirtual().start(() -> work());   // Java thread; OS sees carriers
new ProcessBuilder("echo", "hi").start(); // new address space
```

**Listing 1.** Two kinds of Java thread, plus a real OS process. Only the last is isolated.

```d2
direction: down
osp: "OS process (JVM)" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
ost: "OS threads" {
  width: 130
  height: 36
  style.fill: "#ffebee"
}
pt: "platform Thread" {
  width: 150
  height: 36
  style.fill: "#e3f2fd"
}
vt: "virtual Thread" {
  width: 150
  height: 36
  style.fill: "#e8f5e9"
}
osp -> ost
pt -> ost: "1:1 wrapper"
vt -> ost: "M:N via carriers"
```

**Fig. 1.** An OS process contains OS threads. A Java `Thread` may wrap one or **share** them.

> [!warning] A Java thread is not a sandbox
> Crash or `System.exit` is **process-wide**. Isolation between apps is **another process** (or another JVM), not `new Thread`.

> [!warning] `jstack`-style OS views miss virtual threads
> The kernel counts **OS** threads (platform + busy carriers), **not** millions of `Thread` objects.

> [!tip] Interview answer
> An OS process has its own address space; a Java thread lives in the JVM process and shares the heap. A platform thread is a wrapper that holds one OS thread for life. A virtual thread is still a Thread, but the OS does not see it — many virtual threads share a few carrier OS threads.
