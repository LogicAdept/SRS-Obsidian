<!--
reps: 0
priority: 0
-->
#Java/Collections/Set #Java/Versions/9 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `Set.of(...)` (Java 9+) returns a small **immutable** set. Any mutating call (`add`, `remove`, `clear`) throws **`UnsupportedOperationException`**. Passing a **duplicate** to the factory throws **`IllegalArgumentException`** — unlike a normal `add` that silently ignores dups.

```java
Set<String> s = Set.of("a", "b", "c");
s.add("d"); // UnsupportedOperationException

Set<String> dup = Set.of("a", "a"); // IllegalArgumentException at creation
```

Dump: also rejects **null** (NPE). Iteration order is **unspecified** and can vary between runs. Use it for compact constant sets; use `LinkedHashSet` / `TreeSet` when you need order or mutability.

> [!warning] Unverified traps from the dump
> - `Set.of` duplicate handling is stricter than `HashSet.add`.
> - Unspecified order is not insertion order and not sorted order.
