<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# Can thread priority reliably control execution order in Java?

> [!abstract] Short answer
> **No.** `setPriority` is a **hint**. Platform threads are scheduled by the **OS**; a JVM may map Java’s 1–10 range however it likes, **including ignoring it**. Virtual threads are stuck at `NORM_PRIORITY`. Correctness of order needs `join`, a latch, or another synchronizer — not a bigger `int`.

## Preference is not a sequence

`Thread` exposes `MIN_PRIORITY` (1), `NORM_PRIORITY` (5), and `MAX_PRIORITY` (10). `setPriority` throws `IllegalArgumentException` outside that range. For a platform thread the stored value is the **minimum** of what you asked and the thread group’s max. New platform threads inherit priority (and daemon status) from the parent at **construction**. Older class text said higher priority is executed “in preference” to lower; that is still not a specified start/finish order, and current `Thread` docs no longer even lead with that sentence.

Platform threads are typically **1:1 kernel threads**. The OS decides preemption, time slices, and which ready thread runs. The same official VM note that documents the 1–10 constants says a JVM is free to implement priorities **any way it chooses, including ignoring the value**, and that `setPriority` / `yield` are **advisory** — useful to tune, **not** for correctness. `Thread.yield` is explicitly a hint the scheduler may ignore. Monitor entry and `notify` wakeups are similarly unordered.

```java
public final class PriorityIsNotOrder {
    public static void main(String[] args) throws InterruptedException {
        Thread low = new Thread(() -> {}, "low");
        Thread high = new Thread(() -> {}, "high");
        low.setPriority(Thread.MIN_PRIORITY);
        high.setPriority(Thread.MAX_PRIORITY);
        low.start();
        high.start();
        high.join();
        low.join();
    }
}
```

**Listing 1.** `MAX_PRIORITY` vs `MIN_PRIORITY` does not specify who runs first. `join` does. A start-together gate: [[How do you use CountDownLatch so several threads start together]].

```d2
direction: down
prio: "setPriority(1..10)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
os: "OS / JVM mapping\nmay collapse or ignore" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
order: "join / latch / queue\nspecifies happens-before" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
prio -> os: "not a sequence"
os -> order: "use these for order"
```

**Fig. 1.** Priority may affect how much CPU a **compute-bound** platform thread gets relative to others on some OSes. It does not create a happens-before with another thread’s `run`.

Virtual threads are scheduled by the Java runtime on carriers; their priority is always `NORM_PRIORITY` and `setPriority` **ignores** the argument. Daemon vs priority is a different knob: [[Can the main thread be turned into a daemon thread]].

> [!warning] Do not use priority as a mutex
> If the OS *does* honor a high priority, a looping high-priority thread can **starve** lower ones. That is still not a portable ordering contract. Frivolous `setPriority` calls can also be expensive on some mappings.

> [!warning] Ten Java levels are not ten OS levels
> Historical HotSpot/Solaris mapping put several Java values on the **same** native priority. Two threads at 8 and 9 can be identical to the kernel. Never assume `MAX_PRIORITY` always preempts `NORM_PRIORITY`.

> [!tip] Interview answer
> No. Priority is an advisory 1–10 hint for platform threads; the JVM and OS may ignore or collapse it, and virtual threads cannot change it. “Higher preference” was never a specified execution order. Use `join` or a synchronizer when one thread must wait for another.
