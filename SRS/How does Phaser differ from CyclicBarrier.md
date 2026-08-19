<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: Phaser is also a **barrier**, but more flexible than `CyclicBarrier`:

- each cycle has a **phase number**
- party count is **not fixed**: a thread can **register** and **deregister**
- a party need **not wait** for everyone; it can just **report arrival** and continue
- **observers** can watch the barrier
- a thread **need not be a registered party** to wait for the barrier to advance
- Phaser has **no optional barrier action** (unlike `CyclicBarrier(int, Runnable)`)

Constructors in the dump: `Phaser()` (no parties, barrier “closed”) and `Phaser(int parties)`. Barrier opens when all parties arrive, or when the **last** party is removed.

> [!warning] Unverified traps from the dump
> - Dump skips parent/child Phaser constructors.
> - “No optional action” contradicts how people reuse `onAdvance` in other write-ups; treat as this article’s claim.
