<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How would you explain multithreading fundamentals in Java?

> [!abstract] Short answer
> The JVM runs **many threads of execution at once**. You get a new one by constructing a **`Thread`** (or using an **`Executor`**) and calling **`start()`**, which **schedules `run` concurrently** with the caller. Each thread has a **private JVM stack**; **objects live on a shared heap**. Sharing that heap without **happens-before** (monitors, `volatile`, atomics, j.u.c) is a **data race**. **`run()`** on the `Thread` object is **not** a start. Create/start: [[How do you create a thread in Java]]. `start` vs `run`: [[What is the difference between Thread start and run]]. Threads vs parallel/async: [[How does multithreading differ from parallelism and async work]].

## Threads, memory, then coordination

**Platform** threads map roughly 1:1 to OS threads. **Virtual** threads (21+) are scheduled by the runtime, always **daemon**, cheap when blocked on I/O. `main` is a started **non-daemon** platform thread; shutdown begins when **all started non-daemon** threads finish.

A thread is **`NEW` until `start`**, then **`RUNNABLE` / wait states**, then **`TERMINATED`**. `start` at most once. Interrupt is a **request**; blocking `wait`/`join`/`sleep` throw **`InterruptedException`**. States: [[Which states can a Java thread be in]].

**JMM:** unlock of a monitor hb later lock of the **same** monitor; volatile write hb later read of **that** field. `synchronized` takes the object’s **intrinsic lock**. JMM: [[How would you explain memory Java]]. Monitors: [[How would you explain monitor locks and intrinsic locks in Java]]. Sync tools: [[How do you synchronize access in a multithreaded Java application]]. Stack vs heap: [[How do the stack and heap differ for multithreading in Java]].

Pools **`execute`/`submit`** instead of unbounded `new Thread` — [[How would you explain thread pools and executor frameworks in Java]].

```java
Runnable work = () -> System.out.println(Thread.currentThread().getName());
Thread t = new Thread(work, "worker");
t.start();
t.join();
```

**Listing 1.** Fundamentals in four lines: a `Runnable`, `start` (not `run`), a name, `join` to wait for termination.

```d2
direction: down
t: "Thread.start()" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
run: "run() on that thread" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
heap: "shared heap objects" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
hb: "monitor / volatile / j.u.c" {
  width: 240
  height: 40
  style.fill: "#ffebee"
}
t -> run: "concurrent"
run -> heap: "references"
heap -> hb: "if shared mutably"
```

**Fig. 1.** Concurrency is `start`. Correctness is how you publish heap writes.

> [!warning] Heap sharing is not a memory barrier
> Two threads holding the same object still need a **happens-before** path. `volatile` is not atomic `++`.

> [!warning] `Executor.execute` may run on the caller
> A pool usually uses a worker. The `Executor` contract still allows the **calling** thread (`CallerRunsPolicy`, some custom executors).

> [!tip] Interview answer
> Multithreading in Java means multiple Thread objects whose run methods execute at the same time after start. They share the heap and keep private stacks, so mutable sharing needs synchronized, volatile, or java.util.concurrent. I start threads with start or an executor, never by calling run, and I treat interrupt as cooperative cancellation.
