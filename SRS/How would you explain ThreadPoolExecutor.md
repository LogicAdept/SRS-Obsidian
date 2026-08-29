<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# How would you explain ThreadPoolExecutor?

> [!abstract] Short answer
> **`ThreadPoolExecutor`** is the tunable **`ExecutorService`**: workers, a **`BlockingQueue`**, **keep-alive**, a **`ThreadFactory`**, and a **`RejectedExecutionHandler`**. On **`execute`**: if fewer than **core** threads are running, **create a worker even if others are idle**; else **queue**; else if below **max** and the queue **refused** the task, **create**; else **reject**. Prefer **`Executors`** factories unless you are tuning. Framework: [[How would you explain thread pools and executor frameworks in Java]]. Cached factory: [[How would you explain Executors.newCachedThreadPool()]]. Saturated queue: [[What happens when a thread pool queue is full and a new task arrives]].

## Core, queue, then max — not max first

**Core = max** → fixed-size pool. **Max = `Integer.MAX_VALUE`** → can grow without a thread cap. Core threads start **on demand** unless you **`prestart*`**. Keep-alive applies to **excess** threads by default; **`allowCoreThreadTimeOut(true)`** also times out core workers (keep-alive must be non-zero). Default factory: same group, **`NORM_PRIORITY`**, **non-daemon**. Factories: [[How would you explain Executors]]. Sizing: [[How do you choose the size of a thread pool]]. Interface: [[How would you explain the ExecutorService interface in Java]].

**Queue strategies:** **`SynchronousQueue`** (direct handoff — cached pool; needs a large max or tasks reject); **unbounded `LinkedBlockingQueue`** (fixed factory — **max is ignored**, queue can grow until memory fails); **bounded `ArrayBlockingQueue`** (finite max + finite queue → backpressure via reject). Default reject: **`AbortPolicy`** → **`RejectedExecutionException`**. **`CallerRunsPolicy`** runs on the caller. **`DiscardPolicy`** drops the new task. **`DiscardOldestPolicy`** drops the queue head and retries (rarely acceptable). Hooks: **`beforeExecute` / `afterExecute`** (e.g. reset `ThreadLocal`). Subclass for delay: **`ScheduledThreadPoolExecutor`**.

```java
new ThreadPoolExecutor(
    4, 8,                          // core, maximum
    60L, TimeUnit.SECONDS,         // keep-alive for excess threads
    new ArrayBlockingQueue<>(128),
    Executors.defaultThreadFactory(),
    new ThreadPoolExecutor.AbortPolicy());
```

**Listing 1.** Bounded queue and finite max: after 4 workers, tasks queue; after 128 queued, grow toward 8; then abort.

```d2
direction: down
ex: "execute(task)" {
  width: 150
  height: 36
  style.fill: "#fff8e1"
}
core: "workers < core?" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
q: "offer to queue" {
  width: 150
  height: 36
  style.fill: "#f3e5f5"
}
max: "workers < max?" {
  width: 160
  height: 36
  style.fill: "#e8f5e9"
}
rej: "RejectedExecutionHandler" {
  width: 200
  height: 36
  style.fill: "#ffebee"
}
ex -> core
core -> q: "no: queue"
core -> max: "yes: new worker"
q -> max: "queue full"
max -> rej: "at max"
```

**Fig. 1.** Create-to-core, then queue, then create-to-max, then reject. Not “grow to max before queuing.”

> [!warning] Unbounded queue makes maximumPoolSize a no-op
> `newFixedThreadPool` never creates past core because `LinkedBlockingQueue` always accepts. The OOM risk is the **queue**, not extra threads.

> [!warning] Cached pool OOM is threads, not the queue
> `SynchronousQueue` does not hold tasks. Arrival faster than workers → threads toward **`Integer.MAX_VALUE`**. Default abort still fires only after that bound, which is not a practical cap.

> [!tip] Interview answer
> ThreadPoolExecutor is the real pool: core size, a work queue, max size, keep-alive, factory, and a reject handler. Execute creates up to core first, then queues, and only creates extra threads if the queue will not take the task and we are still below max. I use an Executors factory unless I need that tuning, and I never treat an unbounded queue as a free max-thread setting.
