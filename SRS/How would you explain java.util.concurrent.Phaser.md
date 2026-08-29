<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# How would you explain java.util.concurrent.Phaser?

> [!abstract] Short answer
> A **`Phaser`** is a **reusable barrier** in the same family as **`CyclicBarrier`** and **`CountDownLatch`**, with **variable party count** and **numbered phases**. Parties **`register`** / **`arriveAndDeregister`**. **`arrive()`** records arrival and **does not block**. **`awaitAdvance(phase)`** waits until the phase **changes**. **`arriveAndAwaitAdvance()`** is the CyclicBarrier-like “arrive and wait.” When the last party of a phase arrives, **`onAdvance`** runs and the phase **increments** (wraps after `Integer.MAX_VALUE`). Default `onAdvance` **terminates** when registered parties hit **zero**. Vs barrier: [[How does Phaser differ from CyclicBarrier]]. Latch idiom: [[How can you emulate CountDownLatch with Phaser]]. `register` / `arrive` / `awaitAdvance`: [[What Phaser methods register arrive and awaitAdvance do]].

## Register, arrive, then optionally wait

Unlike a barrier, **how many** parties sync can change. Registration only updates **counts**; the phaser does not remember *which* tasks registered. Sync methods are for **registered** parties; anyone may **monitor** (`getPhase`, `getRegisteredParties`, …) but those snapshots are **not** for control.

**Terminate:** `onAdvance` returns `true`, or `forceTermination()`. After that, waiters **return at once** (negative phase) and further **register is ignored**. Interruptible/timed waits that throw **do not break** the phaser (unlike CyclicBarrier’s all-or-none breakage). `awaitAdvance` **keeps waiting** through interrupt; recover with `forceTermination` if needed. Trees of phasers (**tiering**) cut contention. Arrive happens-before `onAdvance` and the phase advance, which happen-before waiters proceeding. Latch vs barrier survey: [[What is the difference between CyclicBarrier and CountDownLatch]].

```java
void runTasks(List<Runnable> tasks) {
    Phaser gate = new Phaser(1);
    for (Runnable task : tasks) {
        gate.register();
        new Thread(() -> {
            gate.arriveAndAwaitAdvance();
            task.run();
        }).start();
    }
    gate.arriveAndDeregister();
}
```

**Listing 1.** One-shot start gate with a **variable** party count (self registered as `1`, then each task, then self deregisters).

```d2
direction: down
reg: "register parties" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
arr: "arrive (non-blocking)" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
adv: "last arrival: onAdvance\nphase++" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
wait: "awaitAdvance(oldPhase)" {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
reg -> arr
arr -> adv: "unarrived == 0"
wait -> adv: "unblocks"
```

**Fig. 1.** Arrival and waiting are separate. Phase number is the ticket `awaitAdvance` uses.

> [!warning] Not CyclicBarrier breakage
> A timeout or interrupt on a Phaser wait does **not** automatically fail every other party. The barrier is still intact unless you **`forceTermination`** or `onAdvance` ends it.

> [!warning] Monitoring is not a lock
> `getUnarrivedParties()` can race. Do not spin on it for correctness. Use arrive/await (or a latch/barrier) to wait.

> [!tip] Interview answer
> Phaser is a reusable barrier whose party count can change and that advances through numbered phases. arrive does not block; awaitAdvance waits for the next phase; arriveAndAwaitAdvance is the CyclicBarrier-style call. I override onAdvance to stop after N phases or when nobody is registered.
