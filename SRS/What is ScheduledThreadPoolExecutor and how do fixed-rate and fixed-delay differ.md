<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# What is ScheduledThreadPoolExecutor and how do fixed-rate and fixed-delay differ?

> [!abstract] Short answer
> **`ScheduledThreadPoolExecutor` (Java 5) is a `ThreadPoolExecutor` for time-triggered work: tasks wait in a `DelayedWorkQueue` until their trigger time, then run on a fixed-size pool.** The two periodic modes differ in when the clock restarts: `scheduleAtFixedRate` keeps a fixed grid of start times (a late run starts immediately and missed slots collapse — never a burst, never overlap), while `scheduleWithFixedDelay` counts the pause from the *end* of the previous run.

## How scheduling works internally

Periodic tasks are not `Timer`-style callbacks: each run is a queue entry carrying a nanoTime-based trigger, so the schedule is immune to wall-clock changes and DST. Workers pop the entry whose trigger is due soonest (a heap ordered by time, with a leader-follower dance so exactly one thread waits on the head); after the run, a periodic task is re-enqueued with the next trigger — computed from the fixed grid in rate mode, from `finishTime + delay` in delay mode. Two structural quirks follow from inheriting `ThreadPoolExecutor` semantics: `maximumPoolSize` has no effect (the internal queue is unbounded, so the pool never needs a spare thread beyond `corePoolSize`), and idle-timeout tuning is moot. Cancellation is a first-class concern: canceled periodic entries linger in the heap unless `setRemoveOnCancelPolicy(true)` is set, which matters for apps that reschedule tasks every few seconds.

## Fixed-rate versus fixed-delay, measured

The same task — 200 ms of work — scheduled every 100 ms in both modes tells the whole story:

```java
var stpe = new ScheduledThreadPoolExecutor(1);
stpe.scheduleAtFixedRate(task200ms, 0, 100, MILLISECONDS);   // starts: 2, 202, 402, 603, 803
stpe.scheduleWithFixedDelay(task200ms, 0, 100, MILLISECONDS);// starts: 0, 301, 601, 901
```

**Listing 1.** Start times in milliseconds, measured on JDK 21. Fixed-rate attempted starts at 100/300/500 — each landed only after the previous run finished, so the effective period degraded to the task duration (~200 ms) and the missed slots never fired retroactively: no overlap, no catch-up burst. Fixed-delay simply paused 100 ms *after* each 200 ms run, giving a stable ~300 ms cycle.

The choice is semantic. Fixed-rate means "on a wall grid" — metrics flushing every 10 s, heartbeats — and you accept that a slow run shifts the grid late without ever executing two runs at once. Fixed-delay means "rest between runs" — polling a slow backend, rate-limited sweeps — and the cycle self-stretches under load instead of accumulating debt. Neither mode queues missed executions: a run that cannot start on time starts as soon as a worker is free, and its skipped siblings are gone ([[What task types can you submit to an ExecutorService]] covers what the resulting futures expose).

## Failure model and the practical wraps

Two failure facts decide production behavior. First, a thrown exception *silently cancels the periodic run*: the task is removed and the schedule stops with no error anywhere but the swallowed future — periodic bodies get a top-level try/catch, or a wrapper that logs. Second, one blocking run stalls all work on its worker while the rest of the pool carries the schedule — size `corePoolSize` for the concurrent schedules you actually hold, not for "one is enough". Compared to the pre-Java-5 `java.util.Timer`, the executor wins on both: per-task isolation (a timer's single thread dies with its first uncaught exception) and a real thread pool behind the schedule. Framework schedulers are built on this class — Spring's task scheduler ([[How do you use schedulers in Spring Boot]]) wraps it with cron support, and the same delayed-queue mechanics reappear in [[What is a DelayQueue]] used by hand.

> [!warning] Two popular misreadings
> "Fixed-rate catches up by running missed executions back to back" — no: missed start times are dropped; the measured 100 ms grid with a 200 ms task became a 200 ms cycle, not a double burst — count on degradation, never on catch-up. "One exception in one run is one lost run" — no: the whole schedule terminates silently; the returned `ScheduledFuture` completes exceptionally and nobody reads it. Wrap periodic bodies defensively and monitor the future ([[How would you explain ThreadPoolExecutor]] for the base-class cancellation rules).

The base machinery: [[How would you explain ThreadPoolExecutor]]; the factory view: [[How would you explain Executors]]; the queue type that backs the triggers: [[What is a DelayQueue]]; periodic work at the framework layer: [[How do you use schedulers in Spring Boot]].

> [!tip] Interview answer
> `ScheduledThreadPoolExecutor` = pool + `DelayedWorkQueue` of nanoTime-triggered entries; periodic tasks re-enqueue after each run. Fixed-rate keeps a start-time grid: measured 100 ms period with a 200 ms task degraded to ~200 ms starts (2, 202, 402...) — late runs start immediately, missed slots collapse, never overlap. Fixed-delay measures from completion: same task gave 0, 301, 601 — a stable task+delay cycle. Structural facts worth naming: `maximumPoolSize` is inert (unbounded queue), canceled periodic tasks need `setRemoveOnCancelPolicy(true)` to leave the heap, and one uncaught exception silently kills the whole schedule — wrap the body. Rate = wall-grid semantics, delay = rest-between-runs semantics.
