<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How do you stop a Java thread safely and what does safely mean?

> [!abstract] Short answer
> **Cooperatively.** The worker watches a **flag** (`volatile boolean` or the **interrupt status**) and **returns from `run`** with objects left consistent. **`Thread.stop()` is not safe** and does not stop anyone anymore: it **always** throws `UnsupportedOperationException`. “Safe” means you do **not** inject an asynchronous `ThreadDeath` that **unlocks every monitor** mid-update. History: [[What is ThreadDeath]]. `InterruptedException`: [[How would you explain InterruptedException in Java threads]].

## Cooperative cancel, not kill

`Thread.stop()` used to throw `ThreadDeath` in the **victim**. Unwinding released **all** monitors that thread owned. Any object those monitors protected could be **half-written** and then visible to others — “inherently unsafe.” That API is deprecated for removal; **`stop()` always throws `UnsupportedOperationException`** on the caller.

The documented replacement: **modify a variable** the worker samples, and **return from `run` in an orderly fashion**. If it is blocked in `wait` / `join` / `sleep`, call **`interrupt()`** so the wait throws `InterruptedException` (status cleared). Blocked in interruptible NIO: channel closed, `ClosedByInterruptException`. Otherwise `interrupt()` only **sets the status**; a tight CPU loop that never checks **never stops**.

`Thread.interrupted()` reads **and clears** the current thread’s status. `isInterrupted()` does not clear — [[What is the difference between interrupted and isInterrupted in Java]]. Catching `InterruptedException` and continuing without restoring `interrupt()` hides cancellation from callers.

A `volatile boolean cancelled` (or `AtomicBoolean`) is the “variable” in the `stop` javadoc. Combine with `interrupt()` when the thread may be in `wait`. Do not `stop()`, `suspend()`, or `resume()`.

```java
public final class StopSafely implements Runnable {
    private volatile boolean cancelled;

    public void cancel(Thread worker) {
        cancelled = true;
        worker.interrupt();
    }

    @Override
    public void run() {
        while (!cancelled && !Thread.currentThread().isInterrupted()) {
            try {
                work();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }

    private static void work() throws InterruptedException {
        Thread.sleep(100);
    }
}
```

**Listing 1.** Flag plus interrupt. The loop exits; `finally` on real code can still unlock and close. `stop()` is not used.

```d2
direction: down
want: "Stop a worker" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
ok: "flag + interrupt\nreturn from run()" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
no: "Thread.stop()\nUOE; was ThreadDeath" {
  width: 260
  height: 55
  style.fill: "#fce4ec"
}
want -> ok
want -> no
```

**Fig. 1.** Safe stop is an agreed protocol. Kill-from-outside left monitors unlocked with broken invariants.

> [!warning] Swallowing `InterruptedException` cancels the cancel
> Restore the status (`interrupt()`) or rethrow. An empty `catch` makes the next `wait`/`sleep` ignore the request.

> [!warning] Interrupt does nothing to a loop that never checks
> Status sits until `isInterrupted` / `interrupted` / a blocking interruptible call. CPU-bound work must poll.

> [!tip] Interview answer
> Safely means the thread stops itself after it finishes a consistent unit of work, not `Thread.stop()`. I set a `volatile` flag and call `interrupt()` if it may be waiting. `stop()` is unsafe because it used to unlock every monitor via `ThreadDeath`, and today it only throws `UnsupportedOperationException`.
