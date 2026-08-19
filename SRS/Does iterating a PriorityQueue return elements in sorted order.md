<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** A `PriorityQueue`’s iterator (and `toString`) traverses the internal **heap array**, which is only **partially** ordered — the heap invariant guarantees a parent precedes its children, not a fully sorted sequence. Only **`poll`** returns elements in priority order.

```java
PriorityQueue<Integer> pq = new PriorityQueue<>(List.of(5, 1, 3, 2, 4));
System.out.println(pq); // e.g. [1, 2, 3, 5, 4] — NOT sorted

while (!pq.isEmpty())
    System.out.print(pq.poll()); // 12345 — sorted, by draining
```

Dump: to get a sorted view you must repeatedly `poll` (which empties the queue) or copy into a list and `sort` it.

> [!warning] Unverified traps from the dump
> - “The queue prints unsorted” is a classic interview trap.
> - Empty stub `What is java.util.PriorityQueue` is the definition cue; this card is the iterator lie.
