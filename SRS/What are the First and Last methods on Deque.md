<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: each end has the same throwing-vs-returning split as `Queue`, doubled for first and last:

| | First (head) throws | First returns | Last (tail) throws | Last returns |
| --- | --- | --- | --- | --- |
| Insert | `addFirst(e)` | `offerFirst(e)` | `addLast(e)` | `offerLast(e)` |
| Remove | `removeFirst()` | `pollFirst()` | `removeLast()` | `pollLast()` |
| Examine | `getFirst()` | `peekFirst()` | `getLast()` | `peekLast()` |

```java
Deque<String> d = new ArrayDeque<>();
d.offerFirst("x"); // returns boolean, no throw
d.peekLast();      // null if empty, no throw
d.getFirst();      // NoSuchElementException if empty
```

Dump: inherited `Queue` methods map to the **first** end for removal and the **last** for insertion.

> [!warning] Unverified traps from the dump
> - Empty stub `How does the Queue interface differ from the Deque interface` is the FIFO-vs-both-ends cue; this card is the method grid.
