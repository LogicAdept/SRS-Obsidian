<!--
reps: 0
priority: 0
-->
#Java/JMM/HappensBefore #Java/Concurrency/Synchronizers #SRS

# What memory consistency do barrier synchronizers guarantee in Java

> [!abstract] Short answer
> **Actions prior to `CyclicBarrier.await()` and `Phaser.awaitAdvance()` (and their variants) happen-before the actions of the barrier action, and the barrier action's actions happen-before actions subsequent to a successful return from the corresponding await in other threads.** A barrier is a two-stage publication: everyone's work reaches the barrier action, and the barrier action's output reaches everyone.

Barriers therefore have a stronger shape than a plain latch: instead of one release and many acquires, every participant's pre-barrier writes become visible to the optional `Runnable` barrier action, and whatever that action computes (aggregation, snapshot, checkpoint) is published onward to all participants as their awaits complete ([[How does CyclicBarrier run a barrier action when all parties arrive]]). In the JDK source the edge path is concrete: `CyclicBarrier.dowait` runs under a `ReentrantLock`, executes `command.run()` while still holding the lock before advancing the generation and signalling the parties — so the lock's unlock/lock pairs plus the barrier sequencing deliver the documented edges ([[What is the difference between CyclicBarrier and CountDownLatch]]).

```d2
direction: right
p1: "Party 1" {
  width: 200
  height: 74
  w1: "phase work 1" {
    width: 200
    height: 74
    style.fill: "#e3f2fd"
  }
  a1: "await()" {
    width: 200
    height: 74
    style.fill: "#fff3e0"
  }
  w1 -> a1: "prior actions"
}
p2: "Party 2" {
  width: 200
  height: 74
  w2: "phase work 2" {
    width: 200
    height: 74
    style.fill: "#e3f2fd"
  }
  a2: "await()" {
    width: 200
    height: 74
    style.fill: "#fff3e0"
  }
  w2 -> a2: "prior actions"
}
b: "Barrier action\n(command.run)" {
  width: 200
  height: 104
  style.fill: "#f3e5f5"
}
r1: "Party 1 after await\nsees barrier action output" {
  width: 294
  height: 104
  style.fill: "#e8f5e9"
}
r2: "Party 2 after await\nsees barrier action output" {
  width: 294
  height: 104
  style.fill: "#e8f5e9"
}
a1 -> b: "happens-before"
a2 -> b: "happens-before"
b -> r1: "happens-before"
b -> r2: "happens-before"
```

**Fig. 1.** Two-stage publication: pre-await actions of every party are visible to the barrier action, and the barrier action's writes are visible to every party after its await returns.

```java
CyclicBarrier barrier = new CyclicBarrier(2, () -> {
    // runs once per trip, after both parties arrived:
    // guaranteed to see both parties' phase writes
    merge(phase1Results, phase2Results);
});

// party threads
phaseWork();                     // plain writes
barrier.await();                 // publishes to the barrier action...
render(mergedSnapshot);          // ...and after return, mergedSnapshot is visible
```

**Listing 1.** The barrier action aggregates pre-barrier state; each party reads the aggregate after its await returns — both stages are guaranteed by the property.

> [!warning] "Successful return" is part of the rule
> A barrier that is broken — by timeout, interruption of another party, or an exception thrown by the barrier action — resets the generation, and awaits that end in `BrokenBarrierException` or timeout do not carry the publication guarantee for that trip ([[How would you explain java.util.concurrent.Phaser]]). With `Phaser` the same edges apply per phase via `awaitAdvance`/`arriveAndAwaitAdvance`; note that a plain `arrive()` without waiting publishes your writes to whoever advances the phase, but gives you no receive edge for others' writes.

> [!tip] Interview answer
> **For barriers the j.u.c property is two-stage: everything before CyclicBarrier.await or Phaser.awaitAdvance happens-before the barrier action, and the barrier action happens-before the post-await code of all parties. So the barrier action can aggregate everyone's work, and everyone then sees the aggregate. The guarantee rides on successful returns — broken or timed-out trips deliver no edges.**
