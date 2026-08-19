<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: objects added to `PriorityQueue` **MUST be comparable**. Ordered by default in **natural order**, or a `Comparator` at construction. Elements must be mutually comparable or you get a **`ClassCastException`**.

Dump: it **allows duplicates** but not `null`. The **head** is the **least** element. Unbounded; grows dynamically.

> [!warning] Unverified traps from the dump
> - Failure is on `offer`/`add`, not necessarily at construction of an empty queue.
> - “Comparable” here means `Comparable` **or** a supplied `Comparator`.
