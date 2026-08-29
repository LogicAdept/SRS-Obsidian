<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency #Problems/Concurrency #SRS

# Is there a universal fix for race conditions in concurrent code?

> [!abstract] Short answer
> **No.** There is no one API or pattern that removes every race. The memory model only defines a **data race**: **conflicting** accesses with **no happens-before**. **Correct synchronization** (every sequentially consistent execution is data-race-free) makes executions **appear sequentially consistent** — it does **not** make the program **logically** correct. **Data-race-free** still allows bugs in **groups** of ops that must look atomic and do not (`i++`). A **race condition** (check-then-act, lost update) may use only **atomic** accesses and still be wrong. Vs data race: [[What is the difference between a race condition and a data race]]. Survey: [[How would you explain race conditions in concurrent programs]]. Tools: [[How do you synchronize access in a multithreaded Java application]]. `++` vs `volatile`: [[How does volatile visibility differ from atomicity for compound updates]]. JMM: [[How would you explain memory Java]].

## Pick a happens-before that matches the bug

**`volatile`** publishes **one** field; it does not atomicize **read-modify-write**. **`synchronized` / `Lock`** exclude others from a **region** — too coarse and you can **deadlock**. **Atomics / `VarHandle`** fix **one variable’s** RMW. **Concurrent maps** fix **some** map races (`putIfAbsent`), not “the map is my whole invariant.” **Immutability** / **confinement** avoid sharing. **`Thread.start` / `join`** order a one-shot handoff. CHM check-then-act: [[How do you avoid a check-then-act race on ConcurrentHashMap]]. `volatile`: [[How would you explain the volatile field modifier in Java]].

A “local copy plus `volatile`” is **not** a general patch: the copy is a **snapshot**; the next read can still interleave. There is no language switch that “turns off races.”

```java
int n;                    // two n++ : lost updates, and a data race
volatile int v;           // two v++ : still lost updates (not a single RMW)
AtomicInteger a = new AtomicInteger();
a.incrementAndGet();      // one counter, still not “the whole feature is safe”
```

**Listing 1.** Each tool closes a **different** hole. None of them is a universal fix.

```d2
direction: down
rc: "race / data race" {
  width: 180
  height: 36
  style.fill: "#ffebee"
}
t: "tool must match the invariant" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
rc -> t: "no single hammer"
```

**Fig. 1.** Identify conflicting accesses and the **compound** action that must be atomic, then choose a happens-before (or don’t share).

> [!warning] Data-race-free is not “correct”
> The spec says correct synchronization lets you **reason in SC**, not that business rules hold. Two locked methods can still deadlock or break a higher-level invariant.

> [!warning] There is no “always use X”
> Always-`synchronized`, always-`volatile`, or always-`AtomicInteger` will miss other races or add new bugs (contention, deadlock, torn compounds).

> [!tip] Interview answer
> No, there is no universal fix. I find the shared mutable state and give it a happens-before that matches the invariant — a lock, an atomic, a concurrent collection, or no sharing. Volatile and a local copy do not make i-plus-plus or check-then-act safe by themselves.
