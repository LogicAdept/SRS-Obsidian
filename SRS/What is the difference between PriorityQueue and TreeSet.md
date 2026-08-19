<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #Java/Collections/Queues/PriorityQueue #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **`PriorityQueue` allows duplicates** and retrieves by **head priority**. **`TreeSet` forbids duplicates** and supports **full sorted-set** operations.

```java
PriorityQueue<Integer> pq = new PriorityQueue<>(Comparator.reverseOrder());
pq.addAll(List.of(5, 1, 5));
System.out.println(pq.poll()); // 5 (top priority)
```

> [!warning] Unverified traps from the dump
> - Iteration order of a `PriorityQueue` is not the sorted-set order of a `TreeSet`.
> - Two equal-priority elements in a PQ are both kept; in a `TreeSet` the second add is dropped.
