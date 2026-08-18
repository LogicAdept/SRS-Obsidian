<!--
reps: 0
priority: 0
-->
#Java/Collections/List #Java/Collections/Set #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **`LinkedHashSet` is the best approach.** Internally it:

- removes duplicate elements
- **keeps insertion order**

```java
ArrayList<Integer> numbersList = new ArrayList<>(Arrays.asList(1, 1, 2, 3, 3, 3, 4, 5, 6, 6, 6, 7, 8));
LinkedHashSet<Integer> hashSet = new LinkedHashSet<>(numbersList);
ArrayList<Integer> listWithoutDuplicates = new ArrayList<>(hashSet);
```

Dump output: `[1, 2, 3, 4, 5, 6, 7, 8]`.

> [!warning] Unverified traps from the dump
> - The dump picks `LinkedHashSet` because it both deduplicates and **preserves order**; a plain `HashSet` is not what it recommends here.
