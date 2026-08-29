<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# Why Executors.newCachedThreadPool()?

> [!abstract] Short answer
> Use it for **many short-lived async** tasks: **reuse** an idle worker if one exists, else **start a new** platform thread, and **drop** workers idle for **60 seconds** so a quiet pool holds **no** threads. It is an **unbounded thread pool** (`core = 0`, `maximumPoolSize = Integer.MAX_VALUE`) with a **`SynchronousQueue`** (capacity **0**, a **handoff**, not a backlog). That is **not** `newFixedThreadPool`’s **unbounded `LinkedBlockingQueue`**. If tasks **arrive faster than they finish**, the pool can **grow without bound** and the process can **die** creating OS threads. Tuning: [[How would you explain ThreadPoolExecutor]]. Queue full / reject: [[What happens when a thread pool queue is full and a new task arrives]]. Why a pool at all: [[What advantages does ExecutorService offer over creating raw threads]].

## Reuse, then grow, then shrink

`Executors.newCachedThreadPool()` is the convenience factory `ThreadPoolExecutor` documents as **unbounded threads with automatic reclamation**. It is:

```java
public static ExecutorService newCachedThreadPool() {
    return new ThreadPoolExecutor(
            0, Integer.MAX_VALUE,
            60L, TimeUnit.SECONDS,
            new SynchronousQueue<Runnable>());
}
```

**Listing 1.** `corePoolSize` **0**, max **`Integer.MAX_VALUE`**, keep-alive **60s**, work queue a **`SynchronousQueue`**. Same idea with a custom `ThreadFactory` on the overload.

**Execute rule.** If fewer than **core** workers exist, prefer a **new thread** over queuing. Once at core, prefer **queuing**. If the queue **refuses** the task, create another thread unless that would pass **max**, else **reject** (default **`AbortPolicy`** → `RejectedExecutionException`). With **core 0**, the first step is “queue it”; a `SynchronousQueue` **cannot** hold a task unless a worker is **already taking**. Insert **fails**, so a **new thread** is built — **direct handoff**. That is why max is essentially unbounded: otherwise handoff would **reject**. Keep-alive applies to threads **above** core; core is **0**, so **every** idle worker can die after **60s**. Idle long enough, the pool consumes **no** worker resources. Still **`shutdown` / `close`**: the default factory makes **non-daemon** workers.

**Contrast.** `newFixedThreadPool(n)` is `n, n, 0ms, new LinkedBlockingQueue<>()`: **n** workers, **unbounded queue**, **max unused**. Burst **waits** in memory, not in extra OS threads. Cached pool: burst **becomes threads**. Interface: [[How would you explain the ExecutorService interface in Java]]. Pools: [[How would you explain thread pools and executor frameworks in Java]].

```d2
direction: down
task: "execute / submit" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
hand: "SynchronousQueue handoff" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
idle: "reuse idle worker" {
  width: 180
  height: 36
  style.fill: "#e8f5e9"
}
grow: "new platform thread (max MAX_VALUE)" {
  width: 260
  height: 40
  style.fill: "#ffebee"
}
task -> hand
hand -> idle: "taker waiting"
hand -> grow: "no taker"
```

**Fig. 1.** Nothing sits in the queue. Either a worker takes **now**, or the pool **grows**.

> [!warning] Unbounded **threads**, not an unbounded **queue**
> Interview dumps often say “unbounded queue → OOM.” That is **`newFixedThreadPool`**. Cached pool: **`SynchronousQueue` has no internal capacity** (`size()` is **0**). The production failure is **too many platform / OS threads** when arrival stays ahead of completion — tens of thousands of tasks can mean tens of thousands of OS threads and a **crash**. Thread creation can throw **`OutOfMemoryError`**. Do not treat “it went idle and shrank” as a cap during the spike.

> [!warning] Short-lived is a precondition
> The factory is for **many short-lived** async tasks. Long **blocking** work plus a request flood is unbounded **growth**, not reuse. Bounded `max` + bounded queue **rejects**; this factory almost **never** rejects until **shutdown**, because max is `Integer.MAX_VALUE`. Virtual-thread-per-task is a different unbounded model — [[How would you explain Virtual Threads]].

> [!tip] Interview answer
> newCachedThreadPool exists to run lots of short async work: reuse a worker, else start another, and drop idle threads after sixty seconds. It is not an unbounded queue; it is a zero-capacity handoff and an unbounded platform-thread cap. I do not put bursty or blocking production load on it unless I am willing to grow an OS thread per in-flight task.
