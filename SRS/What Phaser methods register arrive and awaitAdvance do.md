<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump Phaser API:

- `int register()` — register a new party; returns current phase
- `int getPhase()` — current phase number
- `int arriveAndAwaitAdvance()` — this party finished the phase; **block** until the others finish. Dump: exact analogue of `CyclicBarrier.await()`. Returns current phase
- `int arrive()` — this party finished the phase; **does not block**; returns phase
- `int arriveAndDeregister()` — finished **all** phases for this party and **unregister**; returns phase
- `int awaitAdvance(int phase)` — if `phase` equals the current phase, **block** until that phase ends; otherwise return the argument immediately

> [!warning] Unverified traps from the dump
> - `arrive()` vs `arriveAndAwaitAdvance()` is the “report and keep running” vs “wait at the barrier” split.
> - `awaitAdvance(phase)` does nothing useful if you pass a **stale** phase number (returns immediately).
