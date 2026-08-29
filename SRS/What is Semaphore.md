<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# What is Semaphore?

> [!abstract] Short answer
> A **`Semaphore`** is a **count of permits**. **`acquire()`** takes one and **blocks** if the count is **0**. **`release()`** adds one and may wake a waiter. There are **no permit objects**. Use it to **cap how many threads** may use a scarce resource (pool, connections). A permit of **one** is a **binary semaphore**: mutex-like, but **no owner** — **any** thread may `release`. It is **not** a `Lock` and **not** reentrant. Fair vs barge: [[What does the fair flag on Semaphore change]]. Vs monitor: [[How would you explain monitor locks and intrinsic locks in Java]]. One-shot latch: [[What is CountDownLatch]]. OS wording: [[How would you explain semaphores for limiting concurrent access]].

## Count, not a mutex object

Construct with **N** permits. `acquire` / `acquire(k)` / timed / `acquireUninterruptibly` exist. **`release` happens-before** a successful **`acquire`** in another thread. Resource-control pools are usually **`new Semaphore(N, true)`** so waiters are not starved; **nonfair** allows **barging**. Untimed **`tryAcquire` ignores fairness**.

The semaphore **limits concurrency**. A **separate** lock (or concurrent structure) keeps the **pool’s data** consistent. **Do not hold that mutex across `acquire()`** — the thread that would `release` could not run. Extra `release` **raises** the count past N. Same thread **`acquire()` twice** on `Semaphore(1)` **deadlocks** (no reentrancy).

```java
Semaphore slots = new Semaphore(8, true);
slots.acquire();
try { useScarceResource(); }
finally { slots.release(); }
```

**Listing 1.** At most eight overlapping users. Return the permit in `finally`.

```d2
direction: down
acq: "acquire()" {
  width: 110
  height: 36
  style.fill: "#fff8e1"
}
zero: "permits == 0?" {
  width: 140
  height: 36
  style.fill: "#ffebee"
}
go: "enter; count--" {
  width: 130
  height: 36
  style.fill: "#e8f5e9"
}
rel: "release(); count++" {
  width: 170
  height: 36
  style.fill: "#e3f2fd"
}
acq -> zero
zero -> go: "no: take"
zero -> acq: "yes: block"
go -> rel
rel -> acq: "may wake"
```

**Fig. 1.** Permits are a number. Zero means wait for a `release`.

> [!warning] Not a `Lock`
> No owner. Another thread can `release`. `Semaphore(1)` is **not** `ReentrantLock`.

> [!warning] Extra `release` widens the gate
> Permits are not checked out to a thread id. A stray `release` allows **more** concurrency than you constructed.

> [!tip] Interview answer
> Semaphore is a permit counter: acquire takes one and may block, release gives one back. I use it to limit how many threads can borrow a scarce resource, usually with fairness for that kind of pool. It is not a Lock — there is no owner, it is not reentrant, and anyone can release.
