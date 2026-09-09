<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS

# What four conditions are required for a deadlock

> [!abstract] Short answer
> All four Coffman conditions must hold at the same time: **mutual exclusion** (the resource serves one thread at a time), **hold and wait** (a thread keeps its resource while asking for another), **no preemption** (the JVM never force-releases it), and **circular wait** (the waiting forms a closed loop). Break any one of them and deadlock becomes impossible.

## The four conditions mapped to Java

In Java terms: a monitor or a `ReentrantLock` is mutually exclusive — one owner at a time. Hold-and-wait is exactly what a nested `synchronized` block does — the outer monitor stays held while the inner is requested. No preemption is a JVM guarantee: only the owning thread can release a monitor (`ReentrantLock.unlock` from a non-owner throws `IllegalMonitorStateException`); the runtime never confiscates one. Circular wait is the only condition that is genuinely your choice: with two threads each taking the opposite lock first, the wait-for graph closes into a cycle — the situation described in [[What is deadlock]].

```java
static void eat(String name) {
    synchronized (forkA) {      // always first — for EVERY thread
        synchronized (forkB) {  // always second
            System.out.println(name + " got both forks");
        }
    }
}
```

**Listing 1.** Acquiring the same two monitors in the same global order removes circular wait; on JDK 21 two threads both printed their line and `both threads finished: circular wait impossible` — nobody blocked.

## Which condition to break in practice

```d2
direction: down
c1: "mutual exclusion\none owner" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
c2: "hold and wait\nkeep A, ask for B" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
c3: "no preemption\nJVM never confiscates" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
c4: "circular wait\nclosed loop" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
dl: "deadlock" {
  width: 180
  height: 70
  style.fill: "#ffebee"
}
c1 -> c4 { style.stroke-dash: 3 }
c2 -> c4 { style.stroke-dash: 3 }
c3 -> c4 { style.stroke-dash: 3 }
c4 -> dl
```

**Fig. 1.** Conditions 1–3 are properties of exclusive locks you rarely control; the practical lever is condition 4 — a global lock order, or a timed `tryLock` that gives up instead of waiting forever. Prevention patterns are compared in [[How do you avoid deadlock in Java]].

Conditions 1–3 are usually unavoidable: the resource is exclusive by design, nested acquisition is how the business logic works, and the JVM will not take locks away. Condition 4 is cheap to break: assign a total order to your locks (for example, by a stable identifier) and always acquire in that order — then the wait-for graph cannot close. Alternatively, acquire with `tryLock` and a timeout, releasing what you hold on failure, which caps hold-and-wait. Both approaches are illustrated in the listings above and in [[What is deadlock]].

> [!warning] Not just `synchronized`, and not just your locks
> The conditions apply to any exclusive resources: `ReentrantLock`, semaphores, connection-pool leases, database row locks — two transactions updating rows in opposite orders deadlock the same way. And an ordering convention only helps if it is global: one module taking A-then-B while another takes B-then-A reintroduces the cycle even though each "looks" ordered locally.

> [!tip] Interview answer
> Deadlock needs all four Coffman conditions together: mutual exclusion, hold-and-wait, no preemption, and circular wait. The first three come with any exclusive lock, so in Java you break circular wait — a global acquisition order or timed `tryLock` with backoff — and deadlock is gone.

