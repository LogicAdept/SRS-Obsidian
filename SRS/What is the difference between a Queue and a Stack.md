<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: a **queue** is a collection designed to hold elements prior to processing. Besides basic collection operations it provides extra insert, extract, and inspect operations. **Usually but not necessarily FIFO.** A **stack** is also a form of queue, but **LIFO**.

Dump: whichever order, the head is the element you can remove with `remove()` or `poll()`. Stack and Vector are both synchronized.

Usage in the dump: process an incoming stream in receive order → queue (work lists, request handling). Only push/pop the top → stack (recursion).

> [!warning] Unverified traps from the dump
> - `PriorityQueue` is a Queue that is not FIFO.
> - Legacy `Stack` is not the modern recommendation; another dump names `ArrayDeque`.
> - Existing FIFO / FILO cards answer “which collection”; this card is Queue vs Stack.
