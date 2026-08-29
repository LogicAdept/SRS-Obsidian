<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# How do you use CountDownLatch so several threads start together?

> [!abstract] Short answer
> Give the workers a **start gate**: `new CountDownLatch(1)`, each worker calls `await()` before the shared work, and the coordinating thread calls `countDown()` when it is ready. The count is how many `countDown`s open the gate, **not** how many threads may wait. When the count hits zero, every thread already in `await` is released and later `await` calls return immediately. The latch is one-shot.

## A count of one is the start signal

A latch initialized with **1** is an on/off gate: all threads that `await()` stay parked until one `countDown()` opens it. That is the documented way to keep workers from running until the driver is ready. Worker count does not belong in the constructor unless those workers are also the events you are counting.

```java
import java.util.concurrent.CountDownLatch;

public final class StartTogether {
    public void startWorkers(int n) throws InterruptedException {
        CountDownLatch startSignal = new CountDownLatch(1);
        for (int i = 0; i < n; i++) {
            new Thread(() -> {
                try {
                    startSignal.await();
                    doWork();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }).start();
        }
        startSignal.countDown();
    }

    private static void doWork() { /* shared start */ }
}
```

**Listing 1.** `CountDownLatch(1)` as a start gate (Java 5+). Threads may call `countDown` without waiting; threads may `await` without ever decrementing. After zero, `countDown` is a no-op.

```d2
direction: down
create: "CountDownLatch(1)\nstart workers" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
wait: "each worker await()\nbefore doWork" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
open: "driver countDown()\ncount 1 → 0" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
run: "parked waiters released\nlate await() returns at once" {
  width: 320
  height: 80
  style.fill: "#fce4ec"
}
create -> wait
wait -> open
open -> run
```

**Fig. 1.** The gate does not wait for every worker to reach `await` first. A worker that parks late, after the count is already zero, passes immediately. That is still “do not start work until the signal”; it is not a rendezvous.

The same class page shows a second latch, `doneSignal = new CountDownLatch(N)`, so the driver can `await()` until each worker `countDown()`s at the end. That is “wait until N actions finish”, not this cue. [[What is CountDownLatch]] covers both shapes.

## Count vs waiters, and “together”

`countDown` only decrements while the count is greater than zero. Opening the gate releases **all current waiters together** in the latch sense: none of them proceeds past `await` until the count is zero, and actions before that `countDown` happen-before a successful `await` in another thread. The scheduler still runs those threads independently; the latch is not a simultaneous `start()`.

If several **events** must happen before anyone proceeds (arrivals plus a starter), set the count to that many `countDown`s. Threads that both signal arrival and wait do `countDown()` then `await()`; threads that only open the gate just `countDown()`. Do not treat those event slots as “number of cars”. A `CountDownLatch(8)` that is really five waiters plus three extra decrements is the same gate with a larger count, not a different API.

Need every party present **and** then a reusable release? That is a barrier, not a spent latch — [[What is the difference between CyclicBarrier and CountDownLatch]]. The Phaser stand-in for this gate is [[How can you emulate CountDownLatch with Phaser]].

> [!warning] The latch cannot be reset
> After the count reaches zero, every later `await` returns immediately. There is no `reset`. A second heat needs a new `CountDownLatch` (or a `CyclicBarrier` / `Phaser`).

> [!warning] `await` is interruptible
> `await()` throws `InterruptedException` and clears the interrupted status. Swallowing it and falling through to `doWork()` starts without the gate. Restore the interrupt (as in Listing 1) or abort. Plain Phaser `awaitAdvance` is the opposite: it keeps waiting after an interrupt.

> [!tip] Interview answer
> Use `CountDownLatch(1)`: workers `await()` at the top of `run`, the coordinator `countDown()` when it wants them to go. The constructor argument is the number of `countDown`s, not the number of threads. When the count hits zero all parked waiters are released and the latch is spent — create another latch if you need a second start.
