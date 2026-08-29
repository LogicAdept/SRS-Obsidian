<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How would you explain which statement about threads is incorrect?

> [!abstract] Short answer
> Garbled cue: **which of these claims about threads is false?** The **false** one is **“calling `run()` directly throws.”** It does **not**. On a **platform** `Thread` built with a `Runnable`, `run()` runs that task on the **current** thread; on a **virtual** thread, `run()` **does nothing**. No exception either way. **`start()` twice** (or after terminate) throws **`IllegalThreadStateException`**. **Start order is not execution order.** **`sleep` does not drop monitors.** Start vs `run`: [[What is the difference between Thread start and run]]. Restart: [[How do you forcibly start a Java thread]]. Order/priority: [[Can thread priority reliably control execution order in Java]]. `wait` vs sleep: [[How would you explain the Object wait method and waiting on monitors]].

## Four exam claims

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | `start()` twice throws at run time | **True** — `IllegalThreadStateException`; a `Thread` starts **at most once** |
| 2 | The order you `start` threads may not be the order they run | **True** — the scheduler (OS or VT carriers) is not a FIFO of `start` |
| 3 | Calling `run()` directly throws | **False** — this is the incorrect statement |
| 4 | `sleep` inside `synchronized` does not release the lock | **True** — **“the thread does not lose ownership of any monitors”** |

`wait` **does** leave the monitor (and uses the wait set). `sleep` / `yield` do not. `sleep` is **`TIMED_WAITING`**, not a reason the lock vanishes. Interrupt during `sleep` → `InterruptedException` — [[How would you explain InterruptedException in Java threads]].

```java
Thread t = new Thread(() -> {}, "t");
t.run();                 // caller thread; no exception
t.start();
t.start();               // IllegalThreadStateException
```

**Listing 1.** The quiz trap: `run` is silent (wrong thread or no-op). A second `start` is the method that throws.

```d2
direction: down
q: "which statement is false?" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
a: "run() throws" {
  width: 160
  height: 36
  style.fill: "#ffebee"
}
b: "the other three" {
  width: 160
  height: 36
  style.fill: "#e8f5e9"
}
q -> a: "this one"
q -> b: "true"
```

**Fig. 1.** Pick the lie: `run()` does not throw. `start` twice does.

> [!warning] `run()` is not “start but illegal”
> It is simply the wrong API for concurrency. Virtual-thread `run()` is a **no-op**, still not an exception.

> [!warning] Sleeping is not waiting on the monitor
> Holding a lock and calling `sleep` **keeps** the lock. That can stall everyone else on that monitor for the whole sleep.

> [!tip] Interview answer
> The false statement is that calling run throws; it runs on the caller or does nothing on a virtual thread. Start may be called only once, or you get IllegalThreadStateException. Sleep does not release monitors, and start order is not run order.
