<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# How do you choose the size of a thread pool?

> [!abstract] Short answer
> There is no single JDK formula. You pick **core** and **maximum** together with the **queue**. Compute-heavy work starts near `Runtime.availableProcessors()` (ForkJoin’s default parallelism). Tasks that **block** can use more workers than CPUs. `newFixedThreadPool(n)` makes **n** the live size because its queue is **unbounded**, so `maximumPoolSize` never applies. Same question: [[How do you choose the size of a thread pool]].

## Size is pool plus queue

`ThreadPoolExecutor` grows to `corePoolSize` before it queues. Once at core, it **queues** rather than creating more threads. A new worker above core appears only when the queue **cannot** accept the task, and only up to `maximumPoolSize`; otherwise the task is **rejected**. Equal core and max is a **fixed** pool. `setCorePoolSize` / `setMaximumPoolSize` can change bounds later.

Queue policy decides whether “max” is real:

1. **Direct handoff** (`SynchronousQueue`, as in `newCachedThreadPool`): no idle worker → new thread. Needs a large/unbounded max or tasks reject. Arrival faster than processing → **unbounded thread growth**.
2. **Unbounded queue** (`LinkedBlockingQueue` with no capacity, as in `newFixedThreadPool`): waiters sit in the queue; **at most core threads** are created; **maximumPoolSize has no effect**. Bursts smooth; sustained overload → **unbounded queue growth**.
3. **Bounded queue**: finite max threads plus finite queue. Large queue + small pool cuts CPU and context switches but can **starve throughput**. If tasks **block (I/O)**, the OS can run **more threads than you otherwise allow**. Small queues want **larger** pools; too large a pool burns scheduling overhead.

`newWorkStealingPool()` targets **available processors**; `newWorkStealingPool(p)` uses parallelism **p**. `ForkJoinPool()` does the same; the common pool is the usual default. `availableProcessors()` is at least 1 and **may change** while the VM runs — poll if you resize. Blocking I/O in fork/join is **not** guaranteed to add workers (`ManagedBlocker` is the extension).

`newVirtualThreadPerTaskExecutor()` is **not** a sized pool: one virtual thread per task, unbounded. Do not pick an `n` for that executor.

When the pool and queue are both full, the handler runs — default **abort** (`RejectedExecutionException`). **Caller-runs** is a built-in brake. Saturated queue: [[What happens when a thread pool queue is full and a new task arrives]]. Constructor and knobs: [[How would you explain ThreadPoolExecutor]]. Unbounded cached workers: [[Why Executors.newCachedThreadPool()]].

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public final class PoolSizeChoice {
    public static ExecutorService cpuBound() {
        int n = Runtime.getRuntime().availableProcessors();
        return Executors.newFixedThreadPool(n);
    }

    public static ExecutorService boundedIo() {
        int core = Runtime.getRuntime().availableProcessors() * 2;
        return new ThreadPoolExecutor(
                core,
                core,
                0L,
                TimeUnit.MILLISECONDS,
                new ArrayBlockingQueue<>(256),
                new ThreadPoolExecutor.CallerRunsPolicy());
    }
}
```

**Listing 1.** Fixed pool: `n` workers and an unbounded queue, so `n` is the thread cap. Bounded I/O sketch: core equals max, finite queue, caller-runs instead of growing threads without limit. `nThreads <= 0` on `newFixedThreadPool` throws `IllegalArgumentException`.

```d2
direction: down
need: "How many workers?" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
cpu: "near availableProcessors()\nForkJoin / work-stealing default" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
io: "tasks block → more workers\nthan CPUs can still run" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
queue: "unbounded queue → max ignored\nSynchronousQueue → max is the cap" {
  width: 360
  height: 70
  style.fill: "#fce4ec"
}
need -> cpu: "compute"
need -> io: "I/O"
cpu -> queue: "still pick a queue"
io -> queue: "still pick a queue"
```

**Fig. 1.** Processor count is a starting point for compute. The queue decides whether `maximumPoolSize` ever fires. Virtual-thread-per-task executors skip this choice.

> [!warning] `newFixedThreadPool(n)` does not use `maximumPoolSize`
> The factory’s unbounded queue means extra tasks **wait**, they do not spawn workers past **n**. Raising “max” on that executor does nothing unless you change the queue.

> [!warning] Cached / unbounded-max pools are a size of “whatever arrives”
> `newCachedThreadPool` creates a thread when none is idle. That is not a capacity plan. Pair a **bounded** queue with a **finite** max if you need a hard cap, and pick a rejection policy.

> [!tip] Interview answer
> I size a pool with the queue, not a magic constant. Compute work starts at `availableProcessors()`; blocking work can go higher. `newFixedThreadPool(n)` caps threads at n because the queue is unbounded, so I use a bounded queue if I actually want extra workers or rejection.
