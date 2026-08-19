<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **`SortedSet`** is the older interface: sorted iteration, `first()`, `last()`, `headSet`, `tailSet`, `subSet`, `comparator()`. **`NavigableSet`** (Java 6+) extends it with neighbour lookups and reverse-order views. **`TreeSet` implements both.**

```java
NavigableSet<Integer> s = new TreeSet<>(List.of(10, 20, 30, 40));
s.first();           // 10        (SortedSet)
s.last();            // 40
s.floor(25);         // 20  <= 25 (NavigableSet)
s.ceiling(25);       // 30  >= 25
s.descendingSet();   // [40, 30, 20, 10]
s.pollFirst();       // 10, and removes it
```

Dump: in practice declare the variable as `NavigableSet` (or `TreeSet`) to get the full method set — `SortedSet` alone lacks `floor` / `ceiling` / `higher` / `lower`.

> [!warning] Unverified traps from the dump
> - Sibling dump “TreeSet vs SortedSet” only says SortedSet is the interface TreeSet implements; this card is the SortedSet vs NavigableSet split.
> - `ConcurrentSkipListSet` is another NavigableSet in concurrent dumps.
