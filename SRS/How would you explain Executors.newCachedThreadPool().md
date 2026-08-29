<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# How would you explain Executors.newCachedThreadPool()?

> [!abstract] Short answer
> A **cached** pool **creates a thread when none is idle**, and **reuses** idle workers. It is a `ThreadPoolExecutor` with **core 0**, **max `Integer.MAX_VALUE`**, **60-second** keep-alive, and a **`SynchronousQueue`** (direct handoff, **no** task buffer). Idle workers **die after a minute**, so a quiet pool holds **no** threads. Intended for **many short** tasks. If submit rate stays above completion rate, the thread count can **grow without a pool cap** — [[How do you choose the size of a thread pool]]. Why this factory is risky in production: [[Why Executors.newCachedThreadPool()]]. Queue-full policy in general: [[What happens when a thread pool queue is full and a new task arrives]].

## Reuse, else grow; never queue

`execute` tries an idle worker first. If none is waiting, the handoff **fails** (the queue does not hold the `Runnable`), so the executor **starts another thread** up to `Integer.MAX_VALUE`. That is **unbounded workers**, not an unbounded **queue** — unlike `newFixedThreadPool`, which uses a shared unbounded queue and a **fixed** thread count.

`ThreadPoolExecutor` documents this as **direct handoff**: a `SynchronousQueue` avoids deadlock when tasks wait on each other, but it **needs** a huge max pool so submissions are not rejected. The cost is **unbounded thread growth** when work arrives faster than it finishes. Threads unused for **sixty seconds** are removed; after a long idle the cache is empty.

Do not use it as a default production server pool for unbounded request bursts. Size core/max **and** the queue yourself, or use a bounded factory. Virtual-thread “one thread per task” is a different factory (`newVirtualThreadPerTaskExecutor`). Framework overview: [[How would you explain thread pools and executor frameworks in Java]].

```java
ExecutorService cached = Executors.newCachedThreadPool();
// same configuration:
ExecutorService equivalent = new ThreadPoolExecutor(
        0, Integer.MAX_VALUE,
        60L, TimeUnit.SECONDS,
        new SynchronousQueue<>());
```

**Listing 1.** Factory versus the `ThreadPoolExecutor` it returns. There is no `LinkedBlockingQueue` here.

```d2
direction: down
submit: "execute(task)" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
idle: "idle worker waiting?" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
reuse: "handoff, reuse thread" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
grow: "start another thread\n(max Integer.MAX_VALUE)" {
  width: 280
  height: 55
  style.fill: "#ffebee"
}
submit -> idle
idle -> reuse: "yes"
idle -> grow: "no (SynchronousQueue)"
```

**Fig. 1.** Cached pool grows threads instead of queuing work.

> [!warning] Not an unbounded queue
> `newFixedThreadPool` queues; `newCachedThreadPool` does **not**. Mixing those two stories is a common wrong answer.

> [!warning] Unbounded threads under load
> If tasks keep arriving faster than they complete, the pool can keep creating platform threads until the OS or JVM fails to allocate another. Idle reclaim (60s) does not cap a **sustained** burst.

> [!tip] Interview answer
> newCachedThreadPool is a ThreadPoolExecutor with core zero, max Integer.MAX_VALUE, a sixty-second timeout, and a SynchronousQueue. It reuses idle threads and otherwise starts a new one, which is good for many short tasks. It is dangerous as a default under a flood of work because the thread count is not bounded.
