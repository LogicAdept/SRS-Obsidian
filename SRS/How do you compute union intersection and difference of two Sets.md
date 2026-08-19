<!--
reps: 0
priority: 0
-->
#Java/Collections/Set #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump trio (`addAll` = union, `retainAll` = intersection, `removeAll` = difference). Always **copy first** so you do not mutate the caller’s set.

```java
Set<Integer> a = new HashSet<>(List.of(1, 2, 3));
Set<Integer> b = new HashSet<>(List.of(3, 4, 5));

Set<Integer> union = new HashSet<>(a);
union.addAll(b);          // {1, 2, 3, 4, 5}

Set<Integer> intersection = new HashSet<>(a);
intersection.retainAll(b); // {3}

Set<Integer> diff = new HashSet<>(a);
diff.removeAll(b);         // {1, 2}
```

Dump: a common bug is calling `a.addAll(b)` and silently changing the caller’s set. Symmetric difference is union minus intersection (already a Collection-methods card in the vault).

> [!warning] Unverified traps from the dump
> - Copy before bulk ops.
> - For intersection, dump says copy and iterate the smaller set against the larger one — O(min(a, b)) lookups on a HashSet.
