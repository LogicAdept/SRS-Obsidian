<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# How would you explain `Executors`?

> [!abstract] Short answer
> **`Executors`** (Java 5+) is a **static factory utility** for executors, not an interface. The six names to know: **`newFixedThreadPool`** — fixed workers on a **shared unbounded queue**; **`newCachedThreadPool`** — grows on demand, reuses idle workers, threads die after idling; **`newSingleThreadExecutor`** — one worker, sequential order, guaranteed **not reconfigurable**; **`newScheduledThreadPool`** — delays and periodic runs; **`newWorkStealingPool`** — a **`ForkJoinPool`** with multiple queues; **`newVirtualThreadPerTaskExecutor`** (Java 21) — a new virtual thread per task. Tuned internals: [[How would you explain ThreadPoolExecutor]]. Pool mechanics: [[How would you explain thread pools and executor frameworks in Java]].

## The factories and what they actually build

* **`newFixedThreadPool(n)`** — exactly `n` workers on an **unbounded `LinkedBlockingQueue`**. Because the queue never fills, `maximumPoolSize` tuning is irrelevant here: extra tasks **queue**, they are not rejected.
* **`newCachedThreadPool()`** — core 0, huge max, **60-second** keep-alive, **`SynchronousQueue`** handoff: no buffer, so every submission either takes an idle worker or **spawns** a new thread. Details and risks: [[How would you explain Executors.newCachedThreadPool()]], [[What is a SynchronousQueue]].
* **`newSingleThreadExecutor()`** — one worker; tasks run **sequentially**, no more than one active; if the thread dies, a replacement is created. Unlike `newFixedThreadPool(1)`, the Javadoc guarantees the result is **not reconfigurable** to add threads.
* **`newScheduledThreadPool(n)`** — a **`ScheduledThreadPoolExecutor`**: `schedule`, `scheduleAtFixedRate`, `scheduleWithFixedDelay`.
* **`newWorkStealingPool(parallelism)`** — a **`ForkJoinPool`** targeting the given parallelism (defaults to CPU count); workers **steal** from other queues. Background: [[What is the Java ForkJoin framework]].
* **`newVirtualThreadPerTaskExecutor()`** and **`newThreadPerTaskExecutor(factory)`** — Java 21: a **fresh thread per task** instead of pooling; unbounded task count by design.

```d2
direction: down
need: "What do the tasks look like?" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
fixed: "Few, steady, CPU-bound\nnewFixedThreadPool(n)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
burst: "Many short-lived\nnewCachedThreadPool\n(watch growth)" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
seq: "Must run in order\nnewSingleThreadExecutor" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
sched: "Delayed or periodic\nnewScheduledThreadPool" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
steal: "Recursive divide-and-conquer\nnewWorkStealingPool" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
virtual: "Huge count, mostly blocking I/O\nnewVirtualThreadPerTaskExecutor (Java 21)" {
  width: 360
  height: 90
  style.fill: "#e8f5e9"
}
need -> fixed
need -> burst
need -> seq
need -> sched
need -> steal
need -> virtual
```

**Fig. 1.** Each factory encodes a workload assumption; the choice is a sizing decision — see [[How do you choose the size of a thread pool]].

## Why production code often skips the factories

The classic factories **fix the queue and the rejection policy for you**: fixed gives an unbounded queue (memory is the safety valve), cached gives unbounded threads. A saturated server usually wants a **bounded** queue plus a deliberate **`RejectedExecutionHandler`**, and that means constructing **`ThreadPoolExecutor`** directly with the parameters you chose. What happens when that queue fills: [[What happens when a thread pool queue is full and a new task arrives]].

```java
ExecutorService pool = new ThreadPoolExecutor(
        4, 8, 60, TimeUnit.SECONDS,
        new ArrayBlockingQueue<>(100),
        new ThreadPoolExecutor.CallerRunsPolicy());
```

**Listing 1.** The shape production code reaches for: bounded queue, explicit overflow policy — configuration the `Executors` factories do not expose.

> [!warning] newSingleThreadExecutor is not castable into a pool
> The claim "I can downcast the result and call `setCorePoolSize`" is false: the factory returns a **non-reconfigurable wrapper**, unlike `newFixedThreadPool(1)`, which returns a plain `ThreadPoolExecutor`. And "`newFixedThreadPool` can grow past `n`" is false too — its unbounded queue, not extra threads, absorbs the load.

> [!tip] Interview answer
> **`Executors` is the factory facade over executor implementations. Fixed pools give a thread count and an unbounded queue; cached gives unbounded threads with a handoff queue and one-minute idle eviction; single-thread guarantees ordering; scheduled adds delay and periodic execution; work-stealing wraps a ForkJoinPool; Java 21 adds one-virtual-thread-per-task. For servers I usually construct `ThreadPoolExecutor` directly, because I want a bounded queue and an explicit rejection policy.**
