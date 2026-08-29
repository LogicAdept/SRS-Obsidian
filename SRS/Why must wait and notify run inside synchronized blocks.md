<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# Why must wait and notify run inside synchronized blocks?

> [!abstract] Short answer
> `wait` / `notify` / `notifyAll` run on an object’s **wait set**, which is tied to that object’s **monitor**. The caller **must already own** that monitor — via a `synchronized` **method** on it, a `synchronized (`*that object*`)` block, or (for a `Class`) a **`static synchronized`** method. Otherwise **`IllegalMonitorStateException`**. `wait` **drops** this object’s nested lock count, sleeps in the wait set, then **re-locks** the same count before returning. `notify` picks **one** waiter (unspecified which); `notifyAll` clears the set. Neither waiter **runs** until the notifier **unlocks**. Use **`while`**, not `if`, around `wait`. Wait: [[How would you explain the Object wait method and waiting on monitors]]. `notify` vs `notifyAll`: [[How does notify differ from notifyAll in Java]]. Monitor: [[What is monitor in Java]].

## Own the monitor, then drop it only inside `wait`

Wait-set operations exist **only** as `Object.wait`, `notify`, and `notifyAll`. If the caller’s unmatched lock count on that object is **zero**, both wait and notify throw **`IllegalMonitorStateException`** — “attempted to wait or notify **without owning** the monitor.” That is the language rule, not a style tip. Timed `wait(0, 0)` is the same as `wait()`.

**What `wait` does** (once you own the lock): enqueue this thread in the wait set, perform **n** unlocks on **this** object, go dormant. Other monitors you hold **stay** locked. Wake paths: `notify` that **selects you**, `notifyAll`, **interrupt**, timed expiry, or an implementation **spurious** removal (allowed, not encouraged). Then the thread does **n** lock actions again. Until those succeed, it does not return from `wait`. An `InterruptedException` is thrown **after** that re-lock; the interrupt status is **cleared**. Interrupt: [[How would you explain InterruptedException in Java threads]]. Timed overloads: [[How does Object wait with a timeout differ from wait without arguments]].

**What `notify` does:** if the wait set is non-empty, **one** member is removed — **no** specified choice. That thread’s re-lock **cannot** succeed until the notifier **fully unlocks** this monitor. `notifyAll` removes **everyone**; they still serialize on the same lock. `Thread.sleep` does **not** drop monitors and is **not** a wait/notify substitute.

**Why `while`.** Spurious wake, a `notify` for a **different** condition, and “I woke but lost the race after re-lock” all mean: the predicate may be **false** when `wait` returns. Loop until it is true. Checking the predicate and calling `wait` must happen **while still holding** the same monitor the notifier uses to publish the predicate — that is the same `synchronized` that makes `wait` legal.

Private mutex: wait on **that** object, not `this`. [[Why might you synchronize on a private mutex object in Java]].

```java
final class Mailbox {
    private final Object lock = new Object();
    private String message; // null = empty

    void put(String m) throws InterruptedException {
        synchronized (lock) {
            while (message != null) {
                lock.wait();
            }
            message = m;
            lock.notifyAll();
        }
    }

    String take() throws InterruptedException {
        synchronized (lock) {
            while (message == null) {
                lock.wait();
            }
            String m = message;
            message = null;
            lock.notifyAll();
            return m;
        }
    }
}
```

**Listing 1.** Same monitor for condition, `wait`, and `notifyAll`. `while` re-checks after every wake. `notifyAll` because empty and full waiters share one wait set.

```d2
direction: down
own: "own monitor (synchronized)" {
  width: 240
  height: 36
  style.fill: "#e8f5e9"
}
wait: "wait: unlock n, join wait set" {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
note: "notify / notifyAll" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
relock: "waiter re-locks n, then returns" {
  width: 260
  height: 40
  style.fill: "#ffebee"
}
own -> wait
note -> relock: "after notifier unlocks"
wait -> relock: "wake"
```

**Fig. 1.** `wait` is **release-and-sleep** on **this** monitor, not “sleep while holding it.” `notify` only moves a thread out of the wait set.

> [!warning] The matching object is the rule, not “some synchronized nearby”
> `synchronized (a) { b.wait(); }` throws **`IllegalMonitorStateException`** unless you already own **`b`**. Nested `synchronized (b)` inside `synchronized (a)` still waits on **`b`** and drops **`b`**, not `a`. `a` stays locked for the whole wait — a deadlock gift.

> [!warning] `if (!ready) wait()` is not enough
> Implementations **may** remove you from the wait set with **no** notify. `notify` does **not** pick a fair or condition-specific waiter. After re-lock, another thread may have consumed the event. **`while`**. Swallowing `InterruptedException` without restoring the flag loses cancel.

> [!tip] Interview answer
> wait and notify require the calling thread to own that object's monitor, which is what synchronized on that same object does; otherwise you get IllegalMonitorStateException. wait drops that monitor, parks in the wait set, and reacquires it before returning, so the notifier must unlock before the waiter can run. I always wait in a while loop on the real condition because of spurious wakeups and shared wait sets.
