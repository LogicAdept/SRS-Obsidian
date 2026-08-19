<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Set/TreeSet #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **`HashSet` / `LinkedHashSet`:** `hashCode()` to find the bucket, then `equals()` within it. **`TreeSet`:** `compareTo()` or the supplied `Comparator` — **`equals` is ignored**.

```java
Set<String> s = new HashSet<>();
s.add("x");
s.add("x"); // still size 1

Set<String> ci = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
ci.add("Java");
ci.add("JAVA"); // compare == 0 → treated as duplicate
ci.size();      // 1
```

> [!warning] Unverified traps from the dump
> - A `TreeSet` can drop an element as a “duplicate” even though `equals` says it is different (and vice versa). Keep `compareTo` consistent with `equals`.
> - `LinkedHashSet` follows the HashSet uniqueness rule, plus insertion order.
