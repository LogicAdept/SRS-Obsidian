<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Set/LinkedHashSet #Java/Collections/Set/TreeSet #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump:

- `HashSet`: membership tests, **no order**, fastest
- `LinkedHashSet`: **dedupe with stable insertion order**
- `TreeSet`: **sorted** set, **range** operations

```java
Set<String> hs = new HashSet<>(List.of("b", "a", "c"));        // order not guaranteed
Set<String> lhs = new LinkedHashSet<>(List.of("b", "a", "c")); // insertion order
Set<String> ts = new TreeSet<>(List.of("b", "a", "c"));        // [a, b, c]
```

Dump one-liner: `HashSet` fastest and unordered; `LinkedHashSet` insertion order; `TreeSet` sorted.

> [!warning] Unverified traps from the dump
> - Pairwise HashSet vs TreeSet / HashSet vs LinkedHashSet cards already exist; this is the three-way “which one” cue.
> - `EnumSet` is the dump’s fourth choice when the elements are enums.
