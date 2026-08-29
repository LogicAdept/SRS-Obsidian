<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# What is the difference between CyclicBarrier and CountDownLatch?

> [!abstract] Short answer
> **`CountDownLatch`:** **one-shot** count. **`countDown`** does **not** wait; **`await`** waits until the count hits **zero**, then stays **open** (**no reset**). **`CyclicBarrier`:** a **fixed** set of **parties** all **`await`** each other, then the barrier **resets** and can be used **again**. Optional **barrier action** runs on the **last arriver**. A **broken** barrier fails **all** waiters (`BrokenBarrierException`). Latch: [[What is CountDownLatch]]. Barrier action: [[How does CyclicBarrier run a barrier action when all parties arrive]]. Phaser: [[How does Phaser differ from CyclicBarrier]]. Start gun: [[How do you use CountDownLatch so several threads start together]]. Permits (not this pair): [[What is Semaphore]].

## Asymmetric count vs all-arrive, then reuse

**Latch:** constructor **N**. Workers **`countDown`** and **continue**. Coordinators **`await`**. Extra `countDown` at zero is a **no-op**. **`await` after zero returns immediately.** Roles can be **uneven** (100 workers, 1 waiter).

**Barrier:** constructor **parties** (and optional **`Runnable`**). **Every** party **`await`s**. When the last arrives, the action (if any) runs, then **all** are released and the generation **recycles**. **`reset()`** exists but **breaks** waiters if called while they wait. **Interrupt**, **timeout**, or a **throwing action** **breaks** the barrier: others wake with **`BrokenBarrierException`**. A latch **interrupt** only affects **that** `await`.

**`Semaphore`** is a **permit count**, not a rendezvous. **`Phaser`** is the **flexible** reuse + **dynamic** parties option.

```java
CountDownLatch done = new CountDownLatch(n);
// workers: work(); done.countDown();
done.await(); // one-shot

CyclicBarrier bar = new CyclicBarrier(n, this::merge);
bar.await(); // all meet; then reuse
bar.await();
```

**Listing 1.** Latch: N downs, waiters block. Barrier: N `await`s, then again.

```d2
direction: down
l: "CountDownLatch: countDown / await; no reset" {
 width: 360
 height: 40
 style.fill: "#fff8e1"
}
b: "CyclicBarrier: all await; recycles" {
 width: 320
 height: 40
 style.fill: "#e8f5e9"
}
l -> b: "need another round: new latch or a barrier"
```

**Fig. 1.** Latch opens once. Barrier is a repeating meeting point.

> [!warning] Do not `await` the latch on the only counting thread
> If one thread must both **finish the work** and **`await`**, it can **deadlock**. Count down **then** await on **other** threads, or use a barrier where **all** arrive.

> [!warning] A broken barrier is sticky
> After a break, **`await` fails** until you **`reset`** (and you must **coordinate** that). A spent latch is just **open**, not broken.

> [!tip] Interview answer
> CountDownLatch is a one-shot counter: some threads count down and others await zero, and you cannot reset it. CyclicBarrier is reusable: a fixed number of threads all await each other, then they can meet again, and you can run an action when the last one arrives. If you need changing party counts or many phases, use Phaser.
