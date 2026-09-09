<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS

# How would you explain Deadlock, livelock, starvation

> [!abstract] Short answer
> Three liveness failures. **Deadlock**: threads block forever waiting for each other — nobody runs. **Livelock**: threads stay active, keep reacting and yielding, and still make no progress. **Starvation**: the system makes progress, but one thread never gets its turn because others are always served first.

## The distinctions that matter

Deadlock is a frozen cycle: every participant is `BLOCKED` on a lock held inside the cycle, CPU is idle, and the state never changes — see [[What is deadlock]]. Livelock is the active cousin: threads are `RUNNABLE`, doing real work — acquiring, noticing contention, releasing, retrying — yet the work never converges; CPU burns while nothing advances. Starvation is asymmetric: the system as a whole progresses, but one thread is perpetually passed over — a scheduler always picks ready threads, a fair-share resource always goes to someone else; the starving thread may be `RUNNABLE` and never scheduled, or perpetually beaten to a resource.

```java
if (second.tryLock()) {          // try to take the second fork without blocking
    try {
        System.out.println(name + ": made progress on attempt " + attempt);
        return;
    } finally {
        second.unlock();
    }
}
System.out.println(name + ": attempt " + attempt + " -> releases the fork and yields");
```

**Listing 1.** The polite pattern that produces livelock: take your own fork, see the other is taken, release and yield. On JDK 21 both threads printed `releases the fork and yields` for attempts 1 and 2 — active the whole time, zero progress — before one of them finally made progress.

## How to tell them apart and what to do

```d2
direction: right
dl: "Deadlock\nBLOCKED forever\nwait-for cycle" {
  width: 240
  height: 120
  style.fill: "#ffebee"
}
ll: "Livelock\nRUNNABLE, reacting\nno convergence" {
  width: 240
  height: 120
  style.fill: "#fff3e0"
}
st: "Starvation\nothers progress,\none never served" {
  width: 250
  height: 120
  style.fill: "#e3f2fd"
}
dl -> ll: "add polite retry\nwithout backoff" {
  style.stroke-dash: 3
}
ll -> st: "add fairness\nfixes waiting, not cycles" {
  style.stroke-dash: 3
}
```

**Fig. 1.** The states blur into each other: naive deadlock fixes can create livelock, and fairness fixes starvation but cannot untangle a deadlock cycle.

The remedies differ, so diagnosis matters. Deadlock needs its cycle broken — lock ordering or timed acquisition (see [[How do you avoid deadlock in Java]]). Livelock needs the symmetry broken: add randomness or exponential backoff to the retries so threads stop mirroring each other; the demo above converged only when the two threads' timing drifted apart — the minimal version of that state is described in [[What is livelock]]. Starvation needs fairness: a `ReentrantLock(true)` favors the longest-waiting thread and guarantees lack of starvation, at the cost of lower throughput. A race condition or data race is a different axis entirely — correctness of interleaved updates, not liveness — see [[What is the difference between a race condition and a data race]].

> [!warning] Livelock is often introduced by the deadlock fix
> Release-and-retry politeness without backoff is a textbook way to convert a deadlock into a livelock: nobody blocks, nobody proceeds. There is also no `Thread.State` to grep for — livelocked threads look busy, so neither `BLOCKED`-based detection nor a thread dump will name them.

> [!tip] Interview answer
> Deadlock: a lock cycle, threads blocked forever, zero progress, zero CPU. Livelock: threads active and yielding to each other forever, CPU burned, still zero progress — fix with backoff and asymmetry. Starvation: progress exists, but one thread is never served — fix with fairness, paying throughput for it.

