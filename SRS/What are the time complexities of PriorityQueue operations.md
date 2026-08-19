<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: the binary heap gives:

| Operation | Complexity |
| --- | --- |
| `offer` / `add` (insert) | O(log n) — sift up |
| `poll` / `remove()` (poll head) | O(log n) — sift down |
| `peek` / `element` (head) | O(1) |
| `remove(Object)` / `contains` | O(n) — linear scan |

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(7);  // O(log n)
pq.peek();    // O(1)
pq.remove(7); // O(n) — must search first
```

Dump: building a heap from a known collection (the constructor that takes one) is **O(n)**, better than n inserts. Heaps are great at “give me the min,” weak at “find this element.”

> [!warning] Unverified traps from the dump
> - Head `remove()` is O(log n); arbitrary `remove(Object)` is O(n).
> - A short untagged dump already says O(log n) offer/poll and O(1) peek; this card adds `contains` / arbitrary remove and heapify.
