<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How would you explain busy spin or busy waiting in concurrent code?

> [!abstract] Short answer
> A **spin-wait** (busy wait) is a **loop that keeps running** until another thread makes a condition true — typically a **`volatile` flag** — **without** `wait`, `sleep`, or parking. Since 9, put **`Thread.onSpinWait()`** in the loop so the runtime can emit a **spin-wait CPU instruction**. The loop is still correct without it. It **does not** drop monitors. Timed pause vs yield: [[What is the difference between Thread.sleep and Thread.yield]]. Parking on a condition: [[How do methods wait and notify notifyAll]].

## Stay on the core, poll, do not park

`onSpinWait` means: this thread **cannot progress until someone else acts**. Call it **each iteration**. The JVM **may** make that pattern cheaper on some CPUs; it **may** do nothing. It is **not** `yield()` (scheduler hint) and **not** `sleep` (timed cease execution).

The documented shape is `while (flag) { Thread.onSpinWait(); }` with **`volatile`** so the writer’s store is visible — [[How does volatile visibility differ from atomicity for compound updates]]. Empty `while (!ready);` is the same idea without the hint.

Busy-wait **burns a processor** while the condition is false. Use it only when the wait is **short** (the other thread is already running and will store soon). For a long wait, `Object.wait` / `Condition.await` / `LockSupport.park` so the thread **leaves the CPU**. Blocking vs spinning: [[How would you explain blocking versus non blocking methods in IO and concurrency]].

`wait` **releases this monitor**; a spin inside `synchronized` **holds** the lock the whole time — other threads cannot enter to set the flag.

```java
public final class SpinUntilReady {
    private volatile boolean ready;

    public void await() {
        while (!ready) {
            Thread.onSpinWait();
        }
    }

    public void signal() {
        ready = true;
    }
}
```

**Listing 1.** Same structure as the `onSpinWait` API note. Without `volatile`, the reader may never see `ready == true`.

```d2
direction: down
spin: "while (!ready) onSpinWait()" {
  width: 280
  height: 45
  style.fill: "#fff8e1"
}
park: "wait / await / park\nleave the CPU" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
spin -> park: "wait may be long"
```

**Fig. 1.** Spin polls. Park blocks. `yield` in a spin is a different, ignorable hint.

> [!warning] Spinning while holding `synchronized (lock)`
> The thread that should set `ready` often needs that same lock. You livelock: spinner never drops the monitor, writer never runs.

> [!warning] Spin is not a cache-pinning API
> The JDK documents **busy-wait** and optional **processor instructions**. It does not promise the thread stays on the same core.

> [!tip] Interview answer
> Busy waiting is a tight loop on a `volatile` flag instead of `wait` or `sleep`. I call `Thread.onSpinWait()` in the loop since Java 9. I only spin when the other thread will finish almost immediately; otherwise I park.
