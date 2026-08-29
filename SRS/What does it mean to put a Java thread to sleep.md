<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What does it mean to put a Java thread to sleep?

> [!abstract] Short answer
> **`Thread.sleep`** makes the **currently executing** thread **cease execution** for a duration, subject to **timer and scheduler** precision. It is **`static`**: it always sleeps **the caller**, not some other `Thread` reference. The sleeper **does not lose any monitors**. Interrupt during sleep: **clears** the interrupt status and throws **`InterruptedException`**. State is **`TIMED_WAITING`**. Vs `yield`: [[What is the difference between Thread.sleep and Thread.yield]]. Vs `wait`: [[How would you explain wait, sleep]]. Interrupt: [[How would you explain InterruptedException in Java threads]]. States: [[Which states can a Java thread be in]]. Monitor `wait`: [[How would you explain the Object wait method and waiting on monitors]].

## Pause this thread, keep the locks

Overloads: **`sleep(long millis)`**, **`sleep(millis, nanos)`**, **`sleep(Duration)`**. A **negative `Duration` is a no-op**. Time is **not** a real-time guarantee. **`wait`** leaves the monitor and uses a wait set; **`sleep`** does not. **`LockSupport.parkNanos`** is the lower-level park. Virtual threads that sleep can **unmount** from a carrier (blocking pause), unlike a CPU spin. **`onSpinWait`** is for busy-wait, not sleep.

```java
synchronized (lock) {
    Thread.sleep(Duration.ofMillis(50)); // still owns lock
}
try {
    Thread.sleep(100);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt(); // restore status after sleep cleared it
}
```

**Listing 1.** Sleep holds monitors. After `InterruptedException`, the interrupt flag is **clear** unless you set it again.

```d2
direction: down
s: "Thread.sleep" {
  width: 150
  height: 36
  style.fill: "#e3f2fd"
}
t: "current thread TIMED_WAITING" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
m: "monitors still owned" {
  width: 200
  height: 36
  style.fill: "#ffebee"
}
s -> t
s -> m
```

**Fig. 1.** Sleep is a timed pause of **this** thread. It is not `wait` and not “sleep that object.”

> [!warning] `t.sleep(ms)` still sleeps you
> The method is **static**. Passing another `Thread` as the receiver does **not** pause that thread.

> [!warning] Sleeping in `synchronized` stalls everyone on that monitor
> Prefer waiting on a **condition** if you need to **release** the lock until a signal.

> [!tip] Interview answer
> Sleep pauses the calling thread for about the given time and does not release monitors. It is static, so I cannot put another thread to sleep with it. If the thread is interrupted, sleep throws InterruptedException and clears the interrupt status.
