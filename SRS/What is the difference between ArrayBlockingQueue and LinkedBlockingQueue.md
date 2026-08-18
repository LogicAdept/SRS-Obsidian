<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump table:

| Implementation | Characteristics |
|---|---|
| `ArrayBlockingQueue` | **bounded**, array-backed, **single lock**, FIFO |
| `LinkedBlockingQueue` | **optionally bounded**, linked nodes, **separate put/take locks** (higher throughput) |

Dump rule of thumb: `ArrayBlockingQueue` for a simple bounded buffer; `LinkedBlockingQueue` for higher throughput.

Another dump: `ArrayBlockingQueue` has **fair mode** `new ArrayBlockingQueue<>(100, true)` and a **predictable** memory footprint. Unbounded `LinkedBlockingQueue` can **OOME** if producers outpace consumers.

> [!warning] Unverified traps from the dump
> - “Single lock vs two locks” is a dump internals claim, not verified here.
> - Capacity `LinkedBlockingQueue(MAX)` is bounded; the no-arg form is the unbounded dump warning.
