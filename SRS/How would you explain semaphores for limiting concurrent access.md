<!--
reps: 0
priority: 0
-->
#OperatingSystems/Concurrency #Java/Concurrency/Synchronizers #SRS

# How would you explain semaphores for limiting concurrent access?

> [!abstract] Short answer
> **A semaphore is an atomic counter plus a wait queue: `acquire` (P) blocks while the count is zero and `release` (V) increments it and wakes one waiter — so a semaphore initialized to N caps concurrent access at N.** It counts *permission*, not possession: any thread may release, which is exactly what separates it from a mutex and what makes it fit both resource limiting and signaling.

## The primitive and its two jobs

The kernel-level concept is minimal: a non-negative counter; an acquire that parks the caller in a queue when the counter would go negative; a release that bumps the counter and wakes the head waiter. Two use cases fall out of that shape. **Limiting**: initialize to the number of identical resources (connections, slots, licenses); every worker acquires before entering the section, so at most N are inside — this is the counting semaphore's headline job. **Signaling**: initialize to 0; a producer's release makes one consumer's acquire succeed — an event handoff rather than a resource claim. The ownership distinction is the interview centerpiece: a mutex must be released by the thread that locked it (ownership is tracked), while a semaphore has no owner — thread A may acquire and thread B release, which is legitimate for resource slots and nonsense for mutual exclusion ([[What is Semaphore]] shows the userland version with permits).

## The classic construction: a bounded buffer from three semaphores

```text
semaphore empty = N;   // free slots
semaphore full  = 0;   // filled slots
semaphore mutex = 1;   // guards the buffer itself

producer:                       consumer:
  P(empty)                        P(full)
  P(mutex)                        P(mutex)
  put(item)                       take(item)
  V(mutex)                        V(mutex)
  V(full)                         V(empty)
```

**Listing 1.** The bounded-buffer idiom: `empty`/`full` count available capacity in each direction, `mutex` keeps buffer mutation exclusive. The order matters — taking `mutex` before `empty`/`full` deadlocks; the resource counters must be acquired first.

The construction shows the real lesson of the primitive: semaphores compose *counting* concerns (capacity) separately from *exclusion* concerns (the mutex), which is why the same three-line skeleton expresses producer-consumer, rate limiting, and connection pools. Modern implementations park blocked threads (futex-style syscalls) instead of spinning, and add optional fairness — a FIFO handoff so a released permit goes to the longest waiter rather than the luckiest racer ([[What does the fair flag on Semaphore change]] measures the throughput cost of that promise).

## From OS primitive to the Java API

`java.util.concurrent.Semaphore` is the userland analogue with the same contract: `acquire()` parks, `tryAcquire()` probes, `release()` wakes one waiter; `acquire(n)`/`release(n)` extend the unit from one permit to many. It is deliberately not tied to a kernel object — permits are an in-JVM contract with no OS resource behind them, which is why they guard logical capacity (in-flight requests, pool leases), not file locks. The measured behavior of the Java side lives in the sibling cards: permit accounting under contention ([[What is Semaphore]]), fairness trade-offs, and the exercise of building a lock-free structure on acquire/release ([[How do you implement a lock-free stack using Semaphore]]). What the OS layer adds underneath: blocking on a semaphore parks the thread (no user-space busy-wait), wakeups are ordered by the implementation's queue policy, and the counter's atomicity is the same hardware compare-and-swap story the JVM builds on ([[How does the Java Memory Model define visibility and ordering]] covers the memory side of the handoff).

> [!warning] Two popular misreadings
> "A semaphore is just a mutex" — no: no ownership, no reentrancy, and a release you did not pair with your own acquire is a silent permit leak that widens the limit; binary semaphore ≈ mutex only for the simplest exclusion patterns. "The count shows how many threads are waiting" — no: it shows *available permits*; waiters are invisible in the count (only queue instrumentation sees them), which is why APIs expose separate drain-queue introspection.

The Java-side mechanics: [[What is Semaphore]]; the fairness knob: [[What does the fair flag on Semaphore change]]; the built structure: [[How do you implement a lock-free stack using Semaphore]]; the exclusion primitive it is not: [[What is the difference between synchronized and ReentrantLock]].

> [!tip] Interview answer
> Semaphore = atomic permit counter + wait queue: acquire blocks at zero, release increments and wakes one waiter; initialized to N it caps concurrent access at N. Two canonical jobs — resource limiting (counting) and signaling (start at 0). Key distinction from a mutex: no ownership, so any thread may release — perfect for slot accounting, wrong for mutual exclusion; the bounded-buffer idiom (empty N, full 0, mutex 1) shows counting and exclusion composed separately, with the resource semaphores acquired before the mutex or you deadlock. Java's `Semaphore` mirrors the contract (tryAcquire, acquire(n), optional fair FIFO handoff) and guards logical capacity, not kernel objects; blocking parks the thread, spinning only until the queue settles.
