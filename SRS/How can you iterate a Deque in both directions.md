<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: a normal iterator (or for-each) goes **head to tail**. `Deque` adds **`descendingIterator()`**, which walks **tail to head** — handy when a deque is used as a stack and you want top-to-bottom order, or to reverse without copying.

```java
Deque<Integer> d = new ArrayDeque<>(List.of(1, 2, 3));

for (int x : d) System.out.print(x); // 123 (head → tail)

var it = d.descendingIterator();
while (it.hasNext()) System.out.print(it.next()); // 321 (tail → head)
```

Dump: no random access on a `Deque` (no `get(i)`). Structurally modifying the deque during iteration throws **`ConcurrentModificationException`**.

> [!warning] Unverified traps from the dump
> - `descendingIterator` is not a copy; CME still applies in this dump.
> - `PriorityQueue` has no descending iterator of this kind.
