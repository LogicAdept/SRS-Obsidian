<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# Can Java code manually control which thread holds a monitor?

> [!abstract] Short answer
> **No.** There is no API that says “make thread T own object M’s monitor.” Only **one** thread holds a given monitor at a time, and that thread is the one that **successfully locked** it — by running a `synchronized` instance method, a `synchronized (obj)` block, or a `static synchronized` method (the `Class` object). You can **test** the current thread with `Thread.holdsLock`; you cannot assign or transfer ownership.

## Ownership is a side effect of locking

Each object has a monitor. A thread may reenter the same monitor (lock count); each unlock undoes one lock. The body of `synchronized` does not start until that lock action succeeds, and an unlock runs when the body completes, normally or abruptly. Those are the only three Java-language ways `Object.notify` lists for becoming owner. `wait` / `notify` / `notifyAll` require the **caller** to already be that owner (`IllegalMonitorStateException` otherwise). [[Why must wait and notify run inside synchronized blocks]] and [[On which object does a static synchronized method acquire a lock]] are those rules.

```java
public final class MonitorOwner {
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

**Listing 1.** The thread that enters `synchronized (lock)` owns `lock`’s monitor for the body. `holdsLock` (Java 1.4+) is an assertion about **this** thread, not a setter.

```d2
direction: down
q: "Who should own the monitor?" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
sync: "that thread runs synchronized\n(instance / block / static)" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
no: "no hand-off API\nnotify does not pick the winner" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
q -> sync: "only path in Java"
q -> no: "not supported"
```

**Fig. 1.** `notify` wakes some waiter; that thread still **competes** for the lock and has no privilege to be next. `wait` makes **the same** thread T drop the monitor, park, then reacquire to the same lock count before `wait` returns — it does not leave the monitor with a thread you name.

`Thread.sleep` does **not** drop monitors. Historical `Thread.stop` injected `ThreadDeath` so the victim **unlocked** whatever it held as the error unwound; that was not a way to give the monitor to someone else, and `stop()` now always throws `UnsupportedOperationException`. Diagnostic APIs (`ThreadMXBean` locked-monitor snapshots) observe; they do not rebind ownership. `java.util.concurrent` locks are a **different** mechanism from object monitors; `lock()` still acquires for the **calling** thread. Checking ownership: [[How can you check if a thread holds a monitor lock in Java]].

> [!warning] You cannot pick the next owner with `notify`
> The implementation chooses which waiter to wake; after the notifier unlocks, waiters and new `synchronized` entrants compete. There is no “hand this monitor to thread T.”

> [!warning] `holdsLock` is not a query about other threads
> It is true iff **the current thread** owns that object’s monitor. Passing another thread’s identity is not possible; the argument is the object, not a `Thread`.

> [!tip] Interview answer
> No. A monitor is owned only by the thread that entered `synchronized` on that object (or its `Class` for static methods). There is no call to assign the lock to a chosen thread. `wait` releases and the same thread reacquires; `notify` does not elect the next owner. `Thread.holdsLock` only asserts that *this* thread already holds it.
