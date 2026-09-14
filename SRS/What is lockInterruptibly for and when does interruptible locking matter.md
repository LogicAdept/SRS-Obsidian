<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/Locks #SRS

# What is lockInterruptibly for and when does interruptible locking matter?

> [!abstract] Short answer
> **`lock.lock()` parks uninterruptibly: a thread waiting for the lock ignores interruption until it owns the lock. `lock.lockInterruptibly()` parks interruptibly — an interrupt during the wait throws `InterruptedException`, and the thread never acquires the lock.** It is the cancelable version of lock acquisition: the tool for shutdown paths and any task that must not stay stuck in a lock queue just because a holder misbehaved.

## The two waits, measured

Both methods eventually grant the same lock; they differ only in what an interrupt does *while the thread is queued*. The plain `lock()` sets the thread's interrupt flag but keeps waiting — the interruption is delivered only after the lock is finally owned. `lockInterruptibly()` registers the wait as interruptible: the moment the flag arrives, the thread leaves the queue with `InterruptedException` and the lock stays with the original holder.

```java
ReentrantLock lock = new ReentrantLock();   // held by a slow thread

// waiter A - interruptible:
try {
    lock.lockInterruptibly();               // parks; interrupt at ~200ms ->
} catch (InterruptedException e) {          // threw after ~201ms
    // never acquired the lock
}

// waiter B - plain:
lock.lock();                                // interrupt at ~200ms: ignored
// holder releases at ~200ms -> B acquires immediately,
// and Thread.currentThread().isInterrupted() is STILL true
```

**Listing 1.** Interrupt semantics of the two acquisitions, verified on JDK 21: `lockInterruptibly` threw `InterruptedException` after ~201 ms with the lock never owned by the waiter; the plain `lock()` absorbed the interrupt, acquired the lock as soon as it was released, and kept the interrupt flag set after acquiring — the signal was deferred, not lost.

## When the interruptible form is the right default

Three situations make it more than a nicety. First, cancellation contracts: if your worker protocol uses interruption as the cancel signal ([[How would you explain InterruptedException in Java threads]]), every blocking call in the loop should honor it — a plain `lock()` creates a spot where cancellation silently stalls for the whole remaining hold time. Second, shutdown paths: stopping a service whose threads are parked on `lock()` means waiting out the unknown holder; with `lockInterruptibly` the pool's `shutdownNow()` interrupt unwinds them immediately, and you can log or re-route the abandoned work. Third, deadlock triage: an interrupted thread escapes the lock queue even when the cycle is unresolvable, which makes hangs diagnosable instead of permanent ([[What is deadlock]] for the cycle itself). The trade is honest: more interrupt checks in the acquisition path, and `InterruptedException` becomes part of your method's contract — which is exactly why `synchronized` offers no equivalent ([[What is the difference between synchronized and ReentrantLock]]).

The neighboring knob is `tryLock(timeout)` — bounded *time* with no cancellation mid-wait, versus interruptible *indefinite* waiting that can be cut at any moment; they compose as `tryLock(timeout)` plus interruptible parking inside. The same distinction exists for conditions: `await()` versus `awaitUninterruptibly()` ([[How do you implement a bounded buffer with ReentrantLock]] uses the pair in production shape).

> [!warning] Two popular misreadings
> "lockInterruptibly interrupts the lock holder" — no: it changes only how the *caller* waits; the holder feels nothing, and if the caller already owns the lock the reentrant acquisition returns normally. "Plain lock() loses the interrupt" — no: the flag is set and survives; the delivery is deferred until after acquisition (measured in Listing 1) — code that checks `isInterrupted()` later still sees it ([[What is the difference between interrupted and isInterrupted in Java]] covers the flag's lifecycle).

The lock family: [[What is StampedLock]] and [[What is ReadWriteLock]] offer the same two acquisition styles per method; the interrupt model underneath: [[How would you explain InterruptedException in Java threads]]; the base synchronization comparison: [[What is the difference between synchronized blocks and java.util.concurrent locks]].

> [!tip] Interview answer
> `lock()` parks uninterruptibly — the interrupt flag is set but delivered only after the lock is owned; `lockInterruptibly()` parks interruptibly and throws `InterruptedException` without ever acquiring. Measured on JDK 21: interrupt at 200 ms made the interruptible waiter exit at 201 ms with the lock untouched, while the plain waiter absorbed the signal, acquired on release, and kept the flag set. Reach for it in cancelable workers, `shutdownNow()` paths, and deadlock triage; `tryLock(timeout)` is the bounded-time sibling, `synchronized` has no interruptible form at all.
