<!--
reps: 0
priority: 0
-->
#Java/Concurrency #Paradigms/Parallelism #SRS

# Why do we need concurrency?

> [!abstract] Short answer
> Independent units of work must **make progress at the same time**: overlapping **I/O waits** and **independent requests**, not only “use every core.” The JVM **can** run many threads at once — on **several processors**, or by **time-slicing** one. A server’s **throughput** rises with how many requests are **in flight** for a given latency; that **concurrency** is the reason for threads, pools, and (since **21**) **virtual threads**. Extra threads past the **core count** do **not** speed **CPU-bound** work. Virtual threads: [[How would you explain Virtual Threads]]. Async vs concurrent: [[What is the difference between being async and being concurrent]]. Compute split: [[What is the Java ForkJoin framework]].

## Overlap wait, then (maybe) use cores

A **thread** is Java’s unit of concurrency: sequential code that runs **concurrently with**, and largely **independently of**, other such units. The JVM supports **many** threads; they operate on **shared** main memory. That is possible with **many hardware processors**, **time-slicing one** processor, or both. Process vs thread: [[What is the difference between a process and a thread]].

**Servers.** Independent requests are a natural **thread-per-request** mapping. For fixed latency, **concurrency** (requests in flight) must grow with **arrival rate** (throughput). Platform threads wrap **OS** threads, which are **scarce**; pooling **avoids start cost** but does **not** raise that cap, so OS threads often limit throughput **before** CPU or network does. **Virtual threads** keep thread-per-request while overlapping **blocking I/O** on few carriers — **scale** (throughput), **not** faster code. The async/callback style can also overlap I/O, at the cost of splitting the request off the platform’s unit of concurrency.

**CPU-bound work.** If the task is **calculation** for a second, more threads than **processor cores** does **not** help, virtual or platform. That is **parallelism**: `ForkJoinPool`’s default target is **`Runtime.availableProcessors()`**; the **Stream** API stays the usual way to process large data sets **in parallel**. j.u.c toolbox: [[How would you explain the java.util.concurrent package]].

Shared memory is the cost: no **happens-before** between conflicting accesses is a **data race**. Concurrency without a protocol is not a speedup. Race vs data race: [[What is the difference between a race condition and a data race]]. What “yes, I used threads” must mean: [[Have you built multithreaded projects]].

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i -> executor.submit(() -> {
        Thread.sleep(Duration.ofSeconds(1));
        return i;
    }));
}
```

**Listing 1.** Ten thousand **one-second sleeps** can run **concurrently** on virtual threads because they **wait**, not because they need 10,000 cores. The same count of **one-second sorts** would not get faster past the core count.

```d2
direction: down
need: "independent work in flight" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
io: "overlap blocking I/O" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
cpu: "split CPU across cores" {
  width: 210
  height: 36
  style.fill: "#fff8e1"
}
need -> io: "throughput / latency"
need -> cpu: "only if CPU-bound"
```

**Fig. 1.** Concurrency is **in-flight work**. Parallel hardware is **one** way to run it, and it only helps when the work is actually using the CPU.

> [!warning] More threads is not more speed
> Virtual threads are **not** faster platform threads. A pool of **200** platform workers for **10,000** blocking tasks **serializes** most of them; it does not create 10 000 concurrent requests. Past **core count**, extra threads do **not** shorten a **CPU-bound** second of work.

> [!warning] Overlap is not a free data-race waiver
> Time-slicing and shared memory mean another thread **can** see your fields. `start` / `join`, `volatile`, monitors, and j.u.c are why that does not become a **data race**. “We needed concurrency” is not “we skipped happens-before.”

> [!tip] Interview answer
> We need concurrency so independent work can be in flight at once — requests and I/O waits, even on one core via time-slicing. Throughput tracks how many requests you can handle together for a given latency, which is why servers outgrow scarce OS threads. Extra threads do not speed CPU-bound work past the core count; that is parallelism, and it is a different knob from overlapping waits.
