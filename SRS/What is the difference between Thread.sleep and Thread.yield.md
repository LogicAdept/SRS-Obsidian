<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What is the difference between Thread.sleep and Thread.yield?

> [!abstract] Short answer
> **`Thread.sleep`** makes the **caller** **cease execution** for a duration (`TIMED_WAITING`; timer/scheduler precision). It **keeps every monitor**. Interrupt → **`InterruptedException`**, status **cleared**. **`Thread.yield`** is only a **hint** the scheduler **may ignore**; the thread stays **`RUNNABLE`**. Both are **`static`**. Timed pause: [[What does it mean to put a Java thread to sleep]]. Vs `wait`: [[What is the difference between wait and sleep]]. Not cooperative: [[What is cooperative multitasking and which model does Java use]]. Interrupt: [[How would you explain InterruptedException in Java threads]].

## Timed pause vs optional courtesy

`Thread.sleep(millis)` / `sleep(millis, nanos)` / `sleep(Duration)` (19+): the current thread sleeps. Negative millis → `IllegalArgumentException`; `nanos` must be `0..999999`. **`sleep(Duration)` is a no-op if the duration is negative.** Interrupt during sleep: `InterruptedException`, status **cleared**. Ownership of monitors is **unchanged** — unlike `Object.wait`, which **releases this object’s** monitor — [[How do methods wait and notify notifyAll]].

`Thread.yield()`: heuristic to help other threads that would otherwise over-use a CPU. Combine with **profiling**; it may not do what you think. Uses: debugging races; some lock implementations. **Not** a substitute for `sleep`, `wait`, or `join`. Priority is also not a reliable order knob — [[Can thread priority reliably control execution order in Java]].

A spin loop that waits for a flag should consider **`Thread.onSpinWait()`**, not `yield`, when the JDK documents busy-wait.

```java
public final class SleepVsYield {
    public static void pause() throws InterruptedException {
        Thread.sleep(100);
    }

    public static void maybeReschedule() {
        Thread.yield();
    }
}
```

**Listing 1.** `sleep` waits ~100 ms and can throw. `yield` returns immediately as far as the API is concerned; the OS may or may not switch threads.

```d2
direction: down
cur: "current thread" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
sl: "sleep(d)\npark ~d, keep monitors" {
  width: 260
  height: 55
  style.fill: "#fff8e1"
}
y: "yield()\nhint, may no-op" {
  width: 220
  height: 55
  style.fill: "#fce4ec"
}
cur -> sl
cur -> y
```

**Fig. 1.** Sleep is a timed wait without dropping locks. Yield is optional advice to the scheduler.

> [!warning] `sleep` inside `synchronized` still holds the lock
> Other threads blocking on that monitor stay blocked for the whole sleep. That is a common deadlock/latency bug. `wait` is the API that drops **this** monitor.

> [!warning] `yield` is not “sleep(0)” with a guarantee
> The scheduler is free to run you again immediately. Do not use it for timing or fairness in application code.

> [!warning] `someThread.sleep(n)` still sleeps **you**
> Both methods are **`static`**. They always affect **the current** thread. There is **no** separate `RUNNING` vs `RUNNABLE` in `Thread.State`.

> [!tip] Interview answer
> `sleep` pauses this thread for a time and does not release monitors; it can be interrupted. `yield` only suggests giving up the CPU and may be ignored. I almost never call `yield` in production.
