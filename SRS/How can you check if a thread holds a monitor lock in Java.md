<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# How can you check if a thread holds a monitor lock in Java?

> [!abstract] Short answer
> For **this** thread: `Thread.holdsLock(obj)` — `true` iff the **current** thread owns `obj`’s monitor. It is meant for **`assert Thread.holdsLock(obj)`**. There is no `holdsLock(thread, obj)` for another thread. Management snapshots (`ThreadMXBean` / `ThreadInfo.getLockedMonitors()`) can **observe** who owns what; they do not assign ownership.

## `holdsLock` is current-thread only

`Thread.holdsLock(Object obj)` (Java 1.4+) returns whether **the calling thread** holds that object’s monitor. `obj == null` throws `NullPointerException`. A thread owns a monitor by executing a `synchronized` instance method of that object, a `synchronized (obj)` block, or a `static synchronized` method of a `Class` — [[On which object does a static synchronized method acquire a lock]], [[Can Java code manually control which thread holds a monitor]]. `wait` / `notify` require that ownership — [[Why must wait and notify run inside synchronized blocks]].

```java
public final class HoldsLockCheck {
    private final Object lock = new Object();

    public void critical() {
        synchronized (lock) {
            assert Thread.holdsLock(lock);
            work();
        }
    }

    private static void work() {}
}
```

**Listing 1.** The documented use is an assertion inside code that is supposed to run under that monitor. It is not a way to wait for the lock or to query a `Thread` you name.

```d2
direction: down
q: "Does some thread own obj?" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
cur: "Thread.holdsLock(obj)\ncurrent thread only" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
jmx: "ThreadMXBean / ThreadInfo\nsnapshot of locked monitors" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
q -> cur: "in application code"
q -> jmx: "diagnostics"
```

**Fig. 1.** `holdsLock` cannot take a `Thread` argument — the argument is the **object**. To see monitors held by **other** platform threads, dump thread info with locked-monitor flags set (`dumpAllThreads` / `getThreadInfo(..., lockedMonitors, ...)`). If the VM does not support monitor usage monitoring, those calls throw `UnsupportedOperationException`. If you pass `lockedMonitors == false` or the thread holds none, the `MonitorInfo` array is empty. `findMonitorDeadlockedThreads` does not report cycles that include virtual threads.

> [!warning] `holdsLock` is not a substitute for `synchronized`
> A `true` result is a snapshot for **this** call. It does not acquire the monitor, does not create happens-before for other threads, and is useless as a lock protocol. Use it in `assert`, then still enter `synchronized` (or already be inside it).

> [!warning] Do not invent `thread.holdsLock(obj)` on a victim thread
> You cannot ask “does `t` hold `lock`?” with the `Thread` API. Passing `t` as the object tests whether **you** own **`t`’s** monitor (the `Thread` instance), which is a different, usually wrong, question.

> [!tip] Interview answer
> `Thread.holdsLock(obj)` tells you if the **current** thread owns that object’s monitor — typically `assert Thread.holdsLock(obj)` inside a critical section. It does not test other threads. For dumps, `ThreadMXBean` can list locked monitors per platform thread; that is observation, not control.
