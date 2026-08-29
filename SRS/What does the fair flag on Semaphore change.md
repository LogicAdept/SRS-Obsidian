<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# What does the fair flag on Semaphore change?

> [!abstract] Short answer
> It chooses **FIFO vs barging** under contention. `new Semaphore(n, true)` grants permits in the order `acquire` calls were processed. `new Semaphore(n)` (and `fair == false`) makes **no** order promise: a new `acquire()` may take a permit ahead of a thread that is already waiting. Untimed `tryAcquire` **ignores** the flag either way.

## FIFO at the ordering point, not a nicer parking lot

A `Semaphore` (Java 5+) is a permit count: `acquire` takes, `release` gives back. The boolean constructor sets fairness; the one-argument constructor is documented as **nonfair**. `isFair()` reports the choice. Fairness does not change how many permits exist, who may `release`, or that `acquire(int)` / `release(int)` can move several permits at once.

When `fair` is **false**, barging is allowed: a caller of `acquire()` may be served first, as if it jumped to the head of the waiters. When `fair` is **true**, threads that invoke any of the **`acquire` methods** are selected FIFO by when those invocations were processed **inside** the method. One thread can call `acquire` earlier and still reach that internal point later, so call-site order is not a wall-clock guarantee.

```java
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;

public final class FairFlag {
    static Semaphore nonfair(int permits) {
        return new Semaphore(permits);
    }

    static Semaphore fair(int permits) {
        return new Semaphore(permits, true);
    }

    static boolean tryAcquireHonoringFairness(Semaphore s)
            throws InterruptedException {
        return s.tryAcquire(0, TimeUnit.SECONDS);
    }
}
```

**Listing 1.** Default construction is nonfair. Untimed `tryAcquire()` / `tryAcquire(int)` still barge on a fair semaphore if a permit is free; the timed form with zero timeout is the documented way to respect the queue (and it can throw `InterruptedException`).

```d2
direction: down
flag: "Semaphore(n, fair)" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
fifo: "true: FIFO among acquire\nat the internal ordering point" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}
barge: "false: no order\nnew acquire may skip waiters" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
flag -> fifo
flag -> barge
```

**Fig. 1.** The flag is about **who gets the next permit**, not about protecting the resource’s own data. The class `Pool` sample uses `new Semaphore(MAX_AVAILABLE, true)` to limit how many threads enter, and **separate** `synchronized` methods to keep the item array consistent — and it does not hold that lock across `acquire()`, so a `release()` can run.

Use **fair** when the semaphore is a scarce-resource gate so waiters are not starved. For other synchronization, the page says nonfair throughput often wins. `permits == 1` is a binary semaphore (mutex **without** ownership). Fair `true` then means waiters are handed the single permit FIFO; unfair still allows barging, so it is not automatically a single-file queue. Multi-permit `acquire(3)` vs `acquire(2)` has no extra preference; in fair mode the thread whose `acquire` hit the ordering point first is the one that can take a newly freed batch. Limiting concurrent access: [[What is Semaphore]]. Other synchronizers do not take this flag — [[How do you use CountDownLatch so several threads start together]].

> [!warning] Untimed `tryAcquire` breaks fairness on purpose
> Even with `fair == true`, `tryAcquire()` takes an available permit immediately if waiters exist. That barging is documented. Honor the queue with `tryAcquire(0, TimeUnit.SECONDS)` (or the multi-permit timed overload).

> [!warning] Fair does not mean “first line of Java ran first”
> FIFO applies at an internal point in `acquire`. Interruption while waiting in `acquireUninterruptibly()` can also change when a thread is assigned a permit relative to others.

> [!tip] Interview answer
> `Semaphore(n, true)` is FIFO among `acquire` callers under contention; `Semaphore(n)` is nonfair and allows barging. Use fair for resource pools so nobody starves; leave nonfair when throughput matters more. Untimed `tryAcquire` still barges on a fair semaphore — use the timed zero-timeout form if you need the queue honored.
