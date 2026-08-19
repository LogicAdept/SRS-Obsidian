<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: by default a `PriorityQueue` is a **min-heap** (natural order). Pass a `Comparator` to change the policy — `reverseOrder()` makes a **max-heap**, and a key extractor orders by a field.

```java
PriorityQueue<Integer> max = new PriorityQueue<>(Comparator.reverseOrder());
max.offer(1);
max.offer(9);
max.offer(5);
max.poll(); // 9

PriorityQueue<Task> tasks =
    new PriorityQueue<>(Comparator.comparingInt(Task::priority));
```

Dump: the comparator is **fixed at construction**. Without an ordering the heap throws `ClassCastException` on the first `offer`.

> [!warning] Unverified traps from the dump
> - Default is smallest-first, not largest-first.
> - You cannot swap the comparator after construction in this dump.
