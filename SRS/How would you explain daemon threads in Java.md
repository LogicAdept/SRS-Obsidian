<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How would you explain daemon threads in Java?

> [!abstract] Short answer
> A **daemon** thread is a **background** worker the VM **does not wait for**. The **shutdown sequence starts when every started non-daemon thread has terminated**. Unstarted non-daemon threads do **not** delay that. **`main` is a non-daemon** platform thread. **Virtual threads are always daemons** (`setDaemon(false)` throws). Mark a platform thread **before `start()`** (`IllegalThreadStateException` if already alive). Main as daemon: [[Can the main thread be turned into a daemon thread]].

## Who keeps the JVM alive

Platform threads are daemon or not. Constructors **inherit** daemon status from the **parent at construction**. `Thread.ofPlatform().daemon()` sets it on the builder. `isDaemon()` reports the flag; for virtual threads it is always `true`.

When only daemons remain (and every **started** non-daemon is done), shutdown begins. A daemon still in `run` can be **cut off**; do not put required cleanup only there. `Executor` pooled workers are often daemons depending on the factory; ForkJoin workers are created as daemons.

`setDaemon` after `start` is too late (thread is **alive**). Virtual threads: `IllegalArgumentException` if you pass `false`. Spring’s virtual-thread scheduler can let a process exit unless you keep a non-daemon alive — [[How do you enable virtual threads in Spring Boot]]. Creating threads: [[How do you create a thread in Java]].

```java
public final class DaemonDemo {
    public static void main(String[] args) {
        Thread t = new Thread(() -> {}, "bg");
        t.setDaemon(true);
        t.start();
    }
}
```

**Listing 1.** `main` can return immediately; `bg` does not keep the VM running. Omit `setDaemon` and a long-running `bg` would keep the process alive after `main` ends.

```d2
direction: down
alive: "started non-daemon still running?" {
  width: 300
  height: 45
  style.fill: "#e3f2fd"
}
yes: "VM stays up" {
  width: 160
  height: 40
  style.fill: "#e8f5e9"
}
no: "shutdown may begin\ndaemons do not count" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
alive -> yes: "yes"
alive -> no: "no"
```

**Fig. 1.** Only **started non-daemon** threads gate shutdown. Virtual threads never do.

> [!warning] `setDaemon` after `start()` throws
> The thread is alive. Set the flag on the unstarted `Thread` (or use `ofPlatform().daemon()`).

> [!warning] Daemon `finally` is not a shutdown hook
> The VM can exit while that thread is in the middle of work. Use non-daemon threads or explicit shutdown for data you must flush.

> [!tip] Interview answer
> Daemon threads are background threads the JVM will not wait for. Shutdown starts when all started non-daemon threads are done. I call `setDaemon(true)` before `start`. Virtual threads are always daemons.
