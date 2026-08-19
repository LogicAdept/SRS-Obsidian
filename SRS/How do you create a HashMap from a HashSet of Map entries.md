<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Map/HashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump:

```java
HashMap<K, V> map = new HashMap<>(set.size());
for (Map.Entry<K, V> entry : set) {
    map.put(entry.getKey(), entry.getValue());
}
```

The set is `HashSet<Map.Entry<K, V>>`.

> [!warning] Unverified traps from the dump
> - Sibling dump builds a `HashSet` from `map.keySet()` in one constructor call; this direction is a loop of `put`.
> - `Map.Entry` uniqueness is `equals` of key **and** value in the dump’s `HashSet`.
