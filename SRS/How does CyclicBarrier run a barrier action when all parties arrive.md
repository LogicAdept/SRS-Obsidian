<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# How does CyclicBarrier run a barrier action when all parties arrive?

> [!abstract] Short answer
> Pass a `Runnable` to `new CyclicBarrier(parties, barrierAction)`. After the last party calls `await()`, **that same last thread** runs the action, **then** the other waiters are released. The action runs once per generation, before anyone continues, so it can update shared state while the rest of the party is still parked. A successful trip resets the barrier for the next cycle.

## Last arriver runs the `Runnable` before release

`CyclicBarrier` is a reusable rendezvous for a **fixed** party size. The two-argument constructor trips when that many threads have called `await()`, and it executes the given action at the trip — “performed by the last thread entering the barrier.” `null` means no action. `parties < 1` throws `IllegalArgumentException`.

`await()` returns an arrival index: `getParties() - 1` is first in, **0 is last in**. The last arriver is therefore the thread that both runs a non-null constructor action and then sees `0` from `await()`.

```java
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.atomic.AtomicInteger;

public final class BarrierActionDemo {
    public static void main(String[] args) {
        AtomicInteger trips = new AtomicInteger();
        CyclicBarrier barrier = new CyclicBarrier(3, () ->
            System.out.println("trip " + trips.incrementAndGet()));
        for (int i = 0; i < 9; i++) {
            new Thread(() -> {
                try {
                    barrier.await();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } catch (BrokenBarrierException e) {
                    return;
                }
            }).start();
        }
    }
}
```

**Listing 1.** Nine `await()` calls on a 3-party barrier: three generations, action once per trip, last arriver in each generation runs the `Runnable` before the other two continue.

```d2
direction: down
await: "parties await()\nN-1 park" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
last: "last thread arrives\nruns barrierAction" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
release: "waiters released\nbarrier reusable" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
await -> last
last -> release
```

**Fig. 1.** Constructor action runs **after** the last arrival and **before** any waiter proceeds. Actions before `await` happen-before the barrier action, which happen-before successful `await` returns in the other threads.

If the extra work does **not** need the others still suspended, skip the constructor `Runnable` and branch on the index after `await` returns:

```java
if (barrier.await() == 0) {
    // this thread was last; others are already released
}
```

**Listing 2.** Conceptual index check from the class page. Unlike the constructor action, this runs **after** the trip, so parties may already be executing.

The barrier is cyclic: after waiters are released it can be used again — same threads in a loop, or a later group of `parties` arrivals (nine cars on a ferry of three is three trips). That is not `Thread.join()`, which waits for a thread to **die**. The documented `Solver` sample runs a merge `Runnable` at the barrier **and** `join()`s workers at the end. Phaser’s analogue is `onAdvance`, run by the party that trips the phase — [[How does Phaser differ from CyclicBarrier]]. A latch has no per-generation action and does not reset — [[What is the difference between CyclicBarrier and CountDownLatch]], [[How do you use CountDownLatch so several threads start together]].

> [!warning] An exception in the action breaks the barrier
> The last arriver runs the `Runnable`. If that action throws, the exception is propagated on **that** thread and the barrier enters the broken state. Everyone else waiting at this point leaves with `BrokenBarrierException`. One interrupt or timeout does the same all-or-none break. `reset()` after a break is awkward; a new barrier is often simpler.

> [!warning] `await` has two checked exceptions
> `await()` throws `InterruptedException` and `BrokenBarrierException` (the timeout form also `TimeoutException`). Catching raw `Exception` and continuing treats a broken barrier as success. On interrupt, restore the interrupt flag; on `BrokenBarrierException`, stop using that generation.

> [!tip] Interview answer
> Construct `CyclicBarrier(n, runnable)`. When the nth thread `await()`s, that last arriver runs the `Runnable` while the others are still parked, then the barrier releases and can be used again. Use the constructor action when shared state must be updated before anyone continues; use `await() == 0` only when the extra work does not need the party suspended. If the action throws, the barrier is broken.
