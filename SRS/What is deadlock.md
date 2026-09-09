<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS

# What is deadlock

> [!abstract] Short answer
> A deadlock is two or more threads blocked forever, each holding a lock the next one needs — a closed cycle in the wait-for graph. Since the JVM never preempts a monitor and nobody releases voluntarily, no thread in the cycle ever runs again, and the JVM will not fix it by itself.

## How the cycle forms

The minimal case needs two threads and two locks. Thread-1 takes lock A, thread-2 takes lock B, then each tries to take the other's lock while still holding its own: thread-1 holds A and waits for B, thread-2 holds B and waits for A. Both threads sit in the `BLOCKED` state — "waiting for a monitor lock to enter a synchronized block" — and stay there until the process dies. This can only happen when all four Coffman conditions hold at once (mutual exclusion, hold-and-wait, no preemption, circular wait), which is why breaking any single one prevents deadlock — see [[What four conditions are required for a deadlock]] for the full list.

```java
Thread t1 = new Thread(() -> {
    synchronized (forkA) { sleep(100); synchronized (forkB) { } }
}, "thread-1");
Thread t2 = new Thread(() -> {
    synchronized (forkB) { sleep(100); synchronized (forkA) { } }
}, "thread-2");
```

**Listing 1.** The classic interleaving: opposite acquisition orders with a small delay so both threads hold their first monitor before asking for the second.

## Detection in the JDK

```d2
direction: right
t1: "thread-1\nholds forkA" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
t2: "thread-2\nholds forkB" {
  width: 220
  height: 100
  style.fill: "#fff3e0"
}
t1 -> t2: "waits for forkB\n(BLOCKED)" {
  style.stroke: "#c62828"
}
t2 -> t1: "waits for forkA\n(BLOCKED)" {
  style.stroke: "#c62828"
}
```

**Fig. 1.** The wait-for graph has a cycle; with no preemption and no release, the cycle is permanent until the JVM exits.

The JDK ships detection machinery: `ThreadMXBean.findDeadlockedThreads()` finds cycles of threads waiting to acquire object monitors or ownable synchronizers, and the same picture is visible from the outside — a `jstack` thread dump prints every thread's stack, and the victims sit in `BLOCKED` waiting for monitors owned by each other. Running the demo above and probing the bean after a pause printed on JDK 21: `t1 state: BLOCKED, t2 state: BLOCKED`, then `deadlocked: thread-1` and `deadlocked: thread-2`. Detection only names the victims; it never unwinds them — recovery is yours. Prevention strategies are the topic of [[How do you avoid deadlock in Java]], and deadlock is distinct from active-but-stuck states like [[What is livelock]].

> [!warning] Deadlock is not limited to `synchronized`
> The same cycle appears with `ReentrantLock` (every thread waiting for a lock held in the cycle), with semaphores, database row locks, or a thread waiting for another thread's result while that thread waits on yours. Two `synchronized` blocks in opposite orders in two methods are enough — no exotic API needed.

> [!tip] Interview answer
> Deadlock: two or more threads wait forever in a lock cycle — each holds a resource the next one wants, the JVM never preempts monitors, so none of them ever proceeds. Threads stay `BLOCKED`; `ThreadMXBean.findDeadlockedThreads` or a `jstack` dump detects the cycle, but only prevention — like a global lock order — fixes it.

