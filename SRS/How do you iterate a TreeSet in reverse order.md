<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: use `descendingSet()` (a reverse-ordered **view**) or `descendingIterator()`. Both walk the tree from largest to smallest without copying or re-sorting.

```java
NavigableSet<Integer> s = new TreeSet<>(List.of(1, 2, 3));
for (int n : s.descendingSet()) {
    System.out.print(n + " "); // 3 2 1
}

Iterator<Integer> it = s.descendingIterator();
while (it.hasNext()) { /* 3, then 2, then 1 */ }
```

Dump: `descendingSet()` is a **live view** — mutations affect the original set and vice versa. Idiomatic alternative to `new TreeSet<>(Comparator.reverseOrder())` when you only need reverse iteration occasionally.

> [!warning] Unverified traps from the dump
> - It is a view, not a copy.
> - `HashSet` has no descending view.
