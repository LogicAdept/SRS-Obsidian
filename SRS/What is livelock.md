<!--
reps: 0
priority: 0
-->
#Java/Concurrency #Problems/Concurrency #SRS

# What is livelock?

> [!abstract] Short answer
> **Livelock** is a **liveness** failure: threads **keep running** (they are **not** `BLOCKED` on a monitor) but **make no progress** because each **only reacts** to the other. Same outcome as **deadlock** (no useful work), different mechanics (**busy** vs **stuck**). Classic picture: two people in a corridor who **keep stepping aside** in sync. Often from **over-polite deadlock avoidance** (`tryLock`, drop locks, retry forever). Sibling: [[How would you explain livelock in concurrent programs]]. Trio: [[How would you explain Deadlock, livelock, starvation]]. Deadlock: [[What is deadlock]]. Avoid deadlock: [[How do you avoid deadlock in Java]]. States: [[Which states can a Java thread be in]].

## Not blocked, still going nowhere

**Starvation** is a thread that **rarely gets** a resource (greedy holders). **Deadlock** is a **cycle of waiting** (typically **`BLOCKED`** / parked on locks). **Livelock** threads **change state continuously** in response to each other. No exception is required; CPU can stay **busy**. A **backoff** (random sleep, one side yields, a **total lock order**) breaks the symmetry. `tryLock`: [[How would you explain synchronization with synchronized and locks in Java]].

```java
while (true) {
    if (a.tryLock()) {
        try {
            if (b.tryLock()) {
                try { work(); return; }
                finally { b.unlock(); }
            }
        } finally { a.unlock(); }
    }
    // both unlock and retry immediately → can livelock
}
```

**Listing 1.** Symmetric `tryLock` with **no backoff**. Both threads can loop forever **RUNNABLE**.

```d2
direction: down
d: "deadlock: wait" {
  width: 160
  height: 36
  style.fill: "#ffebee"
}
l: "livelock: react / retry" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
p: "no progress" {
  width: 120
  height: 36
  style.fill: "#f3e5f5"
}
d -> p
l -> p
```

**Fig. 1.** Same stuck outcome. Livelock threads are **not** sitting on a monitor wait.

> [!warning] Livelock is not “a kind of deadlock”
> Deadlocked threads **do not run**. Livelocked threads **run**. A sample of stacks usually shows **RUNNABLE** (or spinning), not a lock cycle.

> [!warning] Fail-fast lock retry without jitter
> Detecting deadlock and **always** releasing in the **same** order as the peer recreates the corridor dance. **Asymmetry** or **sleep** is the usual fix.

> [!tip] Interview answer
> Livelock is when threads stay busy responding to each other and never finish the real work. They are not blocked like deadlock. It often comes from polite tryLock retries with no backoff.
