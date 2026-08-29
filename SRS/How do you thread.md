<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How do you thread?

> [!abstract] Short answer
> The dump mixes two questions: **how you start** a thread and **how you stop** one. Start with **`start()`** (or a builder / `startVirtualThread`): that **schedules** `run`; you cannot force the CPU. Stop **cooperatively**: **`interrupt()`** and/or a **`volatile` flag**, then **return from `run`**. **`Thread.stop()`** is not a stop API anymore (`UnsupportedOperationException`). Full notes: [[How do you forcibly start a Java thread]], [[How do you stop a Java thread safely and what does safely mean]].

## Start schedules; stop is a protocol

`new Thread(runnable).start()` (or `Thread.ofVirtual().start`) is how a second thread of execution begins — [[How do you create a thread in Java]]. `start` at most once. `run()` on the caller is not a start. `join` on a thread that was **never** started returns immediately. There is no API to pin a runnable onto a core “now.”

`stop()` / `suspend()` / `resume()` are historical. `stop()` used to throw `ThreadDeath` in the victim and **unlock every monitor** — unsafe, not a clean shutdown. Today **`stop()` always throws `UnsupportedOperationException`**. Do not design around `suspend`.

Cancellation: `interrupt()` sets the interrupt status, or wakes `wait` / `join` / `sleep` with **`InterruptedException`** and **clears** the status. Poll with `isInterrupted()` (does not clear) or `Thread.interrupted()` (clears) — [[What is the difference between interrupted and isInterrupted in Java]]. A CPU loop that never checks the flag **does not stop**. A custom `volatile boolean` is the other documented signal; it **does not** unblock `wait` — you still `interrupt()` for that. Interruptible NIO (`InterruptibleChannel`) can close the channel; a blocked classic `InputStream.read` is not the same.

```java
public final class StartAndStop {
    private volatile boolean cancelled;

    public Thread startWorker() {
        Thread t = new Thread(() -> {
            while (!cancelled && !Thread.currentThread().isInterrupted()) {
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }, "worker");
        t.start();
        return t;
    }

    public void stopWorker(Thread t) {
        cancelled = true;
        t.interrupt();
    }
}
```

**Listing 1.** `start()` to run; flag plus `interrupt()` to finish. No `stop()`.

```d2
direction: down
q: "How do you thread?" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
st: "start() — schedule once" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
sp: "interrupt + flag\nreturn from run" {
  width: 240
  height: 55
  style.fill: "#fff8e1"
}
q -> st
q -> sp
```

**Fig. 1.** The garbled cue is start **and** stop. Neither is `Thread.stop()`.

> [!warning] “No API to start a thread” is false
> There is no **force-run-now**. There **is** `start()`. The dump collapsed those two.

> [!warning] A homemade flag does not wake `wait`
> Without `interrupt()`, a thread in `Object.wait` never sees your `boolean`. `volatile` only makes the flag itself visible.

> [!tip] Interview answer
> I start a thread with `start()`, which only schedules it. I stop it by interrupting and checking a `volatile` flag so `run` returns cleanly. I never call `Thread.stop()`.
