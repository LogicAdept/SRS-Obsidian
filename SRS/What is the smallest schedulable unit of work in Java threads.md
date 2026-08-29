<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What is the smallest schedulable unit of work in Java threads?

> [!abstract] Short answer
> The **thread** — a **`java.lang.Thread`**. Java’s **unit of concurrency** is sequential code that runs **on a thread**, **concurrently** with other threads. A **`Runnable`/`Callable` is work**, not a scheduler entity: it runs **when some thread executes `run`/`call`**. **Platform** threads are **OS-scheduled**. **Virtual** threads are **JDK-scheduled** onto **carrier** platform threads; the **OS** still schedules those **OS threads**, not each VT. Task vs thread vs process: [[What is the difference between a thread a task and a process]]. OS process vs Java thread: [[What is the difference between an OS process and a Java thread]]. VTs: [[How would you explain Virtual Threads]]. Composition: [[What are Java threads composed of]]. Pools: [[What is pool threads]]. Fundamentals: [[How would you explain multithreading fundamentals in Java]].

## The scheduler sees threads, not methods

**`start()`** (or an executor worker) is what becomes **eligible** to run. The JVM/OS pick **which thread** gets a core; they do **not** schedule a **method**, a **line**, or a **task object** by itself. **`Thread.yield`** is only a **hint**. There is **no** Java API for a **CPU quantum** among virtual threads (no VT time-sharing).

A **process** is a larger isolation boundary (own address space). **Many tasks** on a **fixed pool** still share **few** schedulable workers. **`ForkJoinTask`** is still run by **pool threads**.

```java
Runnable task = () -> work();          // not scheduled by itself
new Thread(task).start();              // now a Thread is schedulable
exec.submit(task);                     // a worker Thread runs it later
```

**Listing 1.** The task is data. The **thread** is what the scheduler multiplexes onto CPUs (directly or via a carrier).

```d2
direction: down
task: "Runnable / Callable" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
th: "Thread (schedulable)" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
cpu: "core / OS thread" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
task -> th: "run on"
th -> cpu: "platform 1:1 or VT via carrier"
```

**Fig. 1.** Work items sit on threads. Threads are what get scheduled.

> [!warning] A task is not a unit of scheduling
> Submitting 10,000 tasks to four workers schedules **four** (or so) threads, not 10,000.

> [!warning] Virtual threads are still threads
> They are **not** processes and **not** cooperative `yield` tasks. The JDK mounts them on **platform** threads the **OS** already knows.

> [!tip] Interview answer
> The smallest schedulable unit in Java is the thread, a Thread object the JVM or OS can run. A Runnable is just work that some thread will execute. Virtual threads are still threads: the JDK schedules them onto carrier OS threads.
