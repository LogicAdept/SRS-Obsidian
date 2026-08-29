<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# Can the main thread be turned into a daemon thread?

> [!abstract] Short answer
> **No.** The thread that runs `main` is already a **started, non-daemon** platform thread. `setDaemon` must be called **before** `start()`, and it throws `IllegalThreadStateException` if the thread is **alive**. By the time your code in `main` can call `Thread.currentThread().setDaemon(true)`, that thread is alive.

## Daemon status is frozen once the thread is running

The VM starts with (usually) one non-daemon thread: the one that calls `main`. Shutdown begins when **all started non-daemon** threads have terminated. Unstarted non-daemon threads do not keep the VM up. Daemon vs user threads: [[How would you explain daemon threads in Java]]. Priority is a different, equally non-magical knob: [[Can thread priority reliably control execution order in Java]].

`setDaemon(boolean)` marks a **platform** thread daemon or not. It **must** be invoked before the thread is started. Alive means started and not yet terminated. Virtual threads are always daemon; `setDaemon(false)` on them throws `IllegalArgumentException`. Behavior after termination is unspecified.

```java
public final class MainDaemon {
    public static void main(String[] args) {
        Thread main = Thread.currentThread();
        System.out.println(main.isDaemon()); // false
        main.setDaemon(true); // IllegalThreadStateException
    }
}
```

**Listing 1.** `main` is already alive, so converting it fails. New platform threads inherit daemon status from the parent **at construction**; call `setDaemon` on those **before** `start()`, or use `Thread.ofPlatform().daemon().start(task)`.

```d2
direction: down
main: "main thread\nalready started, non-daemon" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
fail: "setDaemon → IllegalThreadStateException" {
  width: 320
  height: 70
  style.fill: "#fce4ec"
}
ok: "unstarted child.setDaemon(true)\nthen start()" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
main -> fail: "this thread"
main -> ok: "other threads"
```

**Fig. 1.** You cannot flip the thread you are already running on. You can still start daemon helpers so they will not delay shutdown after `main` returns.

> [!warning] “Make main a daemon so the process exits” is the wrong knob
> The process stays up while **any started non-daemon** thread is alive. Returning from `main` ends **that** non-daemon thread. Background work that should not keep the VM alive belongs on daemon threads (or virtual threads, which are always daemon), not on a converted `main`.

> [!warning] Inheritance is at create time
> A child constructed from `main` is non-daemon unless you change it before `start()`. Creating the thread later does not look up `main`’s status again.

> [!tip] Interview answer
> No. `setDaemon` is only legal on a thread that has not been started. The `main` thread is already running, so `Thread.currentThread().setDaemon(true)` throws `IllegalThreadStateException`. Start other threads as daemon (or virtual) if they should not keep the JVM alive after `main` finishes.
