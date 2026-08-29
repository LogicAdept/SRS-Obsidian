<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# How do methods `wait`, `notify`, and `notifyAll` work?

> [!abstract] Short answer
> They are `Object` methods on **that object’s monitor and wait set**. `wait` parks the **current** thread and **drops this object’s lock count**; `notify` wakes **one** waiter; `notifyAll` wakes **all**. Waiters do not run until they **reacquire** the same monitor. The caller must **already own** the monitor (`IllegalMonitorStateException` otherwise). Which waiter `notify` picks is **arbitrary**.

## Wait set, then compete for the lock again

Every object has a monitor and a wait set. `wait` / `notify` / `notifyAll` are the only Java-language operations on that set. A thread becomes owner via `synchronized` on that instance, a synchronized instance method, or `static synchronized` on a `Class` — [[Can Java code manually control which thread holds a monitor]]. Why that ownership is required: [[Why must wait and notify run inside synchronized blocks]]. `notify` vs `notifyAll`: [[How does notify differ from notifyAll in Java]].

`wait()` is `wait(0L, 0)`. Thread **T** (the caller) must own the monitor. T is put in the wait set and performs **n unlocks** of **this** object (the full reentrant count). Other monitors T holds stay locked. T stays out of the wait set until notify (and T is chosen), `notifyAll`, interrupt, timeout (timed wait), or a **spurious** wakeup. Then T **competes** for the monitor like any other locker. When `wait` returns, T’s lock count on this object is restored. Interrupt throws `InterruptedException` **after** that restore.

`notify`: if any threads are waiting, **one** is chosen at the implementation’s discretion — no specified winner, no extra privilege to be next to lock. `notifyAll`: **all** waiters leave the wait set; still **one** owner at a time. If the wait set is empty, both are no-ops.

```java
public final class Mailbox {
    private final Object lock = new Object();
    private String message;

    public void put(String m) {
        synchronized (lock) {
            message = m;
            lock.notifyAll();
        }
    }

    public String take() throws InterruptedException {
        synchronized (lock) {
            while (message == null) {
                lock.wait();
            }
            String m = message;
            message = null;
            return m;
        }
    }
}
```

**Listing 1.** Wait **in a `while`** on the condition (spurious wakeups and extra `notify`s). `notifyAll` here because a single `notify` might wake the wrong waiter if more than one kind of wait existed.

```d2
direction: down
w: "wait: unlock this monitor\npark in wait set" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
n: "notify / notifyAll\nremove from wait set" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
r: "reacquire same monitor\nthen wait returns" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
w -> n
n -> r
```

**Fig. 1.** Waking is not “Runnable and running.” The notifier still holds the lock until it leaves `synchronized`. Timed wait: [[How does Object wait with a timeout differ from wait without arguments]]. `Thread.sleep` does **not** drop monitors.

The dump’s “`wait`/`notify` are not `synchronized` so you must lock explicitly” is the wrong causal story. They **check** ownership; they do not acquire it for you. Calling them without `synchronized` (or an equivalent hold) is `IllegalMonitorStateException`, not a silent wait. `Thread.holdsLock` can assert the hold — [[How can you check if a thread holds a monitor lock in Java]].

> [!warning] `notify` does not mean “that thread runs now”
> It only moves one waiter out of the wait set. That thread still waits to **enter** the monitor. You cannot name which waiter. Prefer `notifyAll` unless you can prove a single waiter kind and that lost wakeups cannot happen.

> [!warning] One `wait` without a loop is a bug
> Implementations may remove a thread from the wait set with **no** notify (spurious wakeup). Re-test the condition. Also re-test because `notifyAll` can wake you before the state you want is true.

> [!tip] Interview answer
> `wait` releases this object’s monitor and parks in its wait set; `notify` wakes one waiter, `notifyAll` wakes all. They must be called while you own that monitor. After a wake the thread reacquires the lock before `wait` returns. Always wait in a loop on the condition; `notify` does not pick a specific thread and does not run it until you unlock.
