<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump constructors: `Semaphore(int permits)` and `Semaphore(int permits, boolean fair)`.

If **`fair` is true**, `acquire()` hands out permits **in queue order**. Parking sample: `new Semaphore(5, true)` — at most five cars in the lot; extras block on `acquire()` until `release()`.

Dump: Semaphore can **acquire/release more than one permit at a time**; the parking sample does not need that.

Clinic-lamp dump: `permits = 1` is a single-file queue into a room.

> [!warning] Unverified traps from the dump
> - Fairness is a constructor flag, not the default in the no-boolean constructor (this article does not spell the default).
> - The parking array is still guarded with `synchronized`; the semaphore only limits **how many** threads enter.
