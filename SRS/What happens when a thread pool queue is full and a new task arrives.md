<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# What happens when a thread pool queue is full and a new task arrives?

> [!abstract] Short answer
> **`ThreadPoolExecutor.execute`** still tries to **start another worker** if the pool is below **`maximumPoolSize`**. Rejection happens only when the **queue will not accept** the task **and** no extra thread can be created — or the executor is **shut down**. Then **`RejectedExecutionHandler.rejectedExecution`** runs. Default **`AbortPolicy`** throws **`RejectedExecutionException`**. Execute order: [[How would you explain ThreadPoolExecutor]]. Cached vs fixed: [[How would you explain Executors.newCachedThreadPool()]]. Framework: [[How would you explain thread pools and executor frameworks in Java]].

## Queue full is not the last step

After **core** workers exist, new work is **offered** to the queue. A **failed offer** (bounded queue full, or **`SynchronousQueue`** with no idle worker) is the cue to **grow** toward max. **Unbounded `LinkedBlockingQueue`** (fixed factory) **never fills**; **`maximumPoolSize` is ignored**; reject is for **shutdown** (or memory exhaustion). **`submit`** still ends in **`execute`**. The handler **is** the rejection — it is not invoked **after** a separate throw. **`CallerRunsPolicy`**: caller runs it. **`DiscardPolicy`**: drop the new task. **`DiscardOldestPolicy`**: drop the queue head and retry.

```java
var pool = new ThreadPoolExecutor(
 1, 2, 0L, TimeUnit.MILLISECONDS,
 new ArrayBlockingQueue<>(1),
 new ThreadPoolExecutor.AbortPolicy());
pool.execute(slow); // core worker
pool.execute(slow); // queued
pool.execute(slow); // second worker (queue full, below max)
pool.execute(slow); // AbortPolicy → RejectedExecutionException
```

**Listing 1.** Core 1, max 2, queue 1: the **fourth** task is the first that rejects.

```d2
direction: down
full: "queue full" {
 width: 120
 height: 36
 style.fill: "#fff8e1"
}
max: "workers < max?" {
 width: 160
 height: 36
 style.fill: "#e8f5e9"
}
w: "new worker" {
 width: 120
 height: 36
 style.fill: "#e3f2fd"
}
h: "RejectedExecutionHandler" {
 width: 220
 height: 40
 style.fill: "#ffebee"
}
full -> max
max -> w: "yes"
max -> h: "no or shut down"
```

**Fig. 1.** Saturation = cannot queue **and** cannot add a thread.

> [!warning] Unbounded queue is never “full”
> `newFixedThreadPool` can **OOM the queue**. It will not reject because the queue filled.

> [!warning] Discard policies can fail silently
> Only **abort** (the default) throws. Caller-runs slows the producer instead.

> [!tip] Interview answer
> If the work queue will not take the task, the pool tries to create another thread up to maximum size. Only then, or after shutdown, does the reject handler run. The default handler throws RejectedExecutionException; an unbounded queue never reaches the full-queue case.
