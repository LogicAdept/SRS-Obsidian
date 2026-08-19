<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `TreeSet` is a `NavigableSet`. Neighbor lookups (inclusive vs exclusive of the target):

| Method | Returns |
| --- | --- |
| `floor(e)` | greatest element ≤ e |
| `ceiling(e)` | smallest element ≥ e |
| `lower(e)` | greatest element strictly < e |
| `higher(e)` | smallest element strictly > e |

```java
NavigableSet<Integer> s = new TreeSet<>(List.of(10, 20, 30));
s.floor(20);   // 20
s.lower(20);   // 10
s.ceiling(20); // 20
s.higher(20);  // 30
s.floor(5);    // null — nothing ≤ 5
```

Dump: all return **null** when no such element exists. O(log n). Related dump also names range views `subSet` / `headSet` / `tailSet`.

> [!warning] Unverified traps from the dump
> - `HashSet` has none of these navigation methods.
> - Callers must null-check; the dump does not mention `NoSuchElementException` here.
