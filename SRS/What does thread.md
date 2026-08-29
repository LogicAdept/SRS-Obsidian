<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What does thread priority mean, and what does it mean to sleep a thread?

> [!abstract] Short answer
> Garbled cue: two `Thread` questions — **priority** and **sleep**. **Priority** is a **hint** to the **scheduler** (`setPriority` / `getPriority`, **`MIN_PRIORITY`…`MAX_PRIORITY`**, default **`NORM_PRIORITY`**). It does **not** reliably order threads. **Virtual threads** have a **fixed** priority you **cannot** change. **Sleep** means **`Thread.sleep`**: the **caller** **ceases execution** for a duration, **keeps monitors**, may be **interrupted** (`InterruptedException`, status **cleared**). Priority: [[Can thread priority reliably control execution order in Java]]. Sleep: [[What does it mean to put a Java thread to sleep]]. Vs `yield`: [[What is the difference between Thread.sleep and Thread.yield]]. Survey: [[How would you explain multithreading fundamentals in Java]]. VTs: [[How would you explain Virtual Threads]].

## Hint vs timed pause

Platform threads **inherit** priority; the OS may ignore or collapse Java’s ten levels. Do not use priority for mutual exclusion or sequencing — use **locks**, **`join`**, **`Executor`**, **`CompletableFuture`**.

**`sleep` is static.** `t.sleep(ms)` still pauses **you**. Time is **timer/scheduler** precision, not a deadline. State **`TIMED_WAITING`**. That is not `Object.wait` (wait set, **releases** the monitor). Interrupt: [[How would you explain InterruptedException in Java threads]].

```java
Thread t = Thread.currentThread();
t.setPriority(Thread.NORM_PRIORITY); // virtual: always NORM; extra values ignored
Thread.sleep(100);                   // this thread pauses; still owns any monitors
```

**Listing 1.** Two different APIs. Neither “starts” work, and sleep is not a way to sleep `t` unless `t` is the caller.

```d2
direction: down
p: "setPriority" {
  width: 140
  height: 36
  style.fill: "#fff8e1"
}
s: "Thread.sleep" {
  width: 140
  height: 36
  style.fill: "#e3f2fd"
}
p -> s: "not substitutes"
```

**Fig. 1.** Priority is scheduling advice. Sleep is a timed cease-execution of the **current** thread.

> [!warning] Priority is not a contract
> High priority does **not** mean “always runs first” or “gets more CPU.” Production code that depends on it is wrong.

> [!warning] Sleeping while holding a monitor
> Other threads that need that lock **wait**. Sleep does **not** drop ownership.

> [!tip] Interview answer
> Thread priority is only a scheduler hint between MIN and MAX, default NORM, and it is not a way to order work. Sleep pauses the calling thread for a while without releasing locks, and interrupt makes it throw InterruptedException. Virtual threads cannot change priority.
