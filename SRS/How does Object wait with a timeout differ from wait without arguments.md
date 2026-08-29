<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# How does Object wait with a timeout differ from wait without arguments?

> [!abstract] Short answer
> **`wait()`** is **`wait(0L, 0)`**: park until **notify / notifyAll / interrupt / spurious wakeup**. Real time is **ignored**. **`wait(timeoutMillis)`** is **`wait(timeoutMillis, 0)`**. If millis and nanos are **both zero**, that is the same infinite wait. If the duration is **positive**, the thread may also wake because **that much real time elapsed** (`1000000 * timeoutMillis + nanos` nanoseconds, more or less). Timeout returns **normally** — not `TimeoutException`. Same wait-set rules: [[How do methods wait and notify notifyAll]].

## Zero duration vs a real deadline

All three `wait` methods require the caller to **own this object’s monitor**, put the thread in the **wait-set**, and **release only this object’s locks**. Other monitors stay held. Before return, the thread **reacquires** this monitor (state as before `wait`). `InterruptedException` is thrown only **after** that restore; the interrupt status is cleared.

**No-arg / both-zero:** the clock is not a wake cause. You stay until notify, interrupt, or a spurious wakeup.

**Positive timeout:** those causes **plus** elapsed real time. You still **cannot** tell from the void return whether it was notify, timeout, or spurious. The documented loop is `while (condition does not hold && timeout not exceeded)`, **recomputing** remaining millis/nanos each time. Negative `timeoutMillis` or `nanos` outside `0..999999` → `IllegalArgumentException`.

`Thread.join(0)` is also “wait forever”; a positive `join(millis)` can return while the thread is still alive. Timed `wait` is the same idea for a **condition**, not for thread death — [[How does Thread.join work in Java]], [[How would you explain the Object wait method and waiting on monitors]].

```java
public final class TimedWait {
    private boolean ready;

    public synchronized boolean awaitReady(long timeoutMillis) throws InterruptedException {
        long deadline = System.nanoTime() + timeoutMillis * 1_000_000L;
        while (!ready) {
            long remaining = deadline - System.nanoTime();
            if (remaining <= 0) {
                return false;
            }
            wait(remaining / 1_000_000L, (int) (remaining % 1_000_000L));
        }
        return true;
    }

    public synchronized void signal() {
        ready = true;
        notifyAll();
    }
}
```

**Listing 1.** Timed `wait` inside `while`, remaining time updated. `wait()` would omit the deadline and loop only on `!ready`. `notify` vs `notifyAll`: [[How does notify differ from notifyAll in Java]].

```d2
direction: down
w0: "wait() / wait(0,0)\nno clock" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
wt: "wait(millis>0)\n+ elapsed real time" {
  width: 260
  height: 55
  style.fill: "#fff8e1"
}
same: "notify, interrupt, spurious\nthen reacquire monitor" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
w0 -> same
wt -> same
```

**Fig. 1.** Timeout adds one wake cause. It does not skip the monitor or the `while` check.

> [!warning] `wait(0)` is not “wait zero milliseconds”
> Both-zero means **ignore the clock**, same as `wait()`. Use a positive duration for a real deadline.

> [!warning] Return from timed `wait` does not mean the condition is true
> Timeout and spurious wakeup look the same as notify. Always re-test, and track remaining time yourself.

> [!tip] Interview answer
> No-arg `wait` waits until notify or interrupt, with no timeout. Timed `wait` can also return when the clock runs out, and `wait(0)` is still forever. I loop on the condition and remaining time because the method does not tell me why it woke.
