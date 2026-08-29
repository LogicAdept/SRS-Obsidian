<!--
reps: 0
priority: 0
-->
#OperatingSystems/Concurrency #Java/Concurrency/Threads #SystemDesign/Performance #SRS

# Why run a program on multiple threads instead of one?

> [!abstract] Short answer
> One thread is **one sequential execution**. Several threads let **independent work stay in flight**: overlapping **waits** (I/O, `sleep`) even on **one** core via **time-slicing**, and **using several processors** when the work is actually **on the CPU**. A server’s **throughput** for a given latency tracks how many requests are **concurrent**; one worker that holds the whole request **serializes** arrivals. Extra threads past the **core count** do **not** shorten a **CPU-bound** second of work. Why concurrency: [[Why do we need concurrency]]. Process vs thread: [[What is the difference between a process and a thread]]. Virtual threads: [[How would you explain Virtual Threads]].

## Overlap waits; parallelize only if it is CPU

The JVM runs **many** threads at once. They share **heap** memory. The machine may use **several hardware processors**, **time-slice one** processor, or both. A **platform** thread is typically a **1:1** wrapper around an **OS** thread (limited, large stack). A **virtual** thread is still a `Thread`, scheduled by the runtime, meant for work that **blocks on I/O**, not long CPU loops. They are **not faster** cores: they buy **throughput**, not lower latency.

**I/O / wait.** While one task is blocked, another thread can run. Thread-per-request keeps that mapping honest: **concurrency** (requests in flight) must grow with **arrival rate** if latency stays put. One platform thread wrapping one OS thread **caps** that in-flight count. Pooling **cuts start cost**; it does **not** raise the OS-thread cap. Virtual threads overlap blocking `java.*` I/O on few carriers.

**CPU.** `ForkJoinPool`’s default **parallelism** is **`Runtime.availableProcessors()`**. If each task **computes** for a second, more threads than **cores** does not help — virtual or platform. That is **parallel hardware**, a different knob from overlapping waits. Fork/join: [[What is the Java ForkJoin framework]].

Shared fields still need a **happens-before** story. Multiple threads without a protocol is a **data race**, not a speedup. JMM: [[Why does the Java Memory Model matter for concurrency]].

```java
void twoWaitsOneThread() throws InterruptedException {
    Thread.sleep(Duration.ofSeconds(1));
    Thread.sleep(Duration.ofSeconds(1)); // ~2s elapsed
}

void twoWaitsTwoThreads() throws Exception {
    try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
        exec.submit(() -> { Thread.sleep(Duration.ofSeconds(1)); return null; });
        exec.submit(() -> { Thread.sleep(Duration.ofSeconds(1)); return null; });
    } // close waits for both → ~1s elapsed
}
```

**Listing 1.** Two **one-second waits**: sequential on one thread, **overlapped** on two. Replace `sleep` with a **one-second sort** and the two-thread version does **not** finish in half the time once you already have one worker per core.

```d2
direction: down
one: "one thread" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
seq: "wait then wait (sum)" {
  width: 200
  height: 36
  style.fill: "#ffebee"
}
many: "several threads" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
overlap: "overlap waits / extra cores" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
one -> seq
many -> overlap
```

**Fig. 1.** Multiple threads are for **in-flight** work. They are not a “make this loop twice as fast” switch.

> [!warning] More threads is not more CPU speed
> Ten thousand **sleeps** can run together on virtual threads. Ten thousand **sorts** cannot outrun the **core count**. A **cached** platform pool for a request flood can **grow OS threads** until the process dies. Default pool workers are **non-daemon**: skip `shutdown` / `close` and the JVM **stays up**.

> [!warning] A second thread sees your fields
> Time-slicing and shared heap mean another thread **can** read what you wrote — or **not**, with no happens-before. “We went multithreaded for performance” is not a waiver for an unsynchronized `HashMap`.

> [!tip] Interview answer
> I use more than one thread so independent work can be in flight — overlapping I/O waits even on one core, and extra cores only when the work is actually computing. Throughput follows how many requests I can have running at once, which a single thread cannot do. I do not add threads past the core count to speed CPU-bound code, and I still need a happens-before story for anything they share.
