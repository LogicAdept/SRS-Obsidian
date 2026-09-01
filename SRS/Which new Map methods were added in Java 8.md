<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/Versions/8 #SRS

# Which new `Map` methods were added in Java 8?

> [!abstract] Short answer
> **Eleven default methods on `java.util.Map`, all `@since 1.8`:** `getOrDefault`, `forEach`, `replaceAll`, `putIfAbsent`, `remove(key, value)`, two `replace` overloads, `computeIfAbsent`, `computeIfPresent`, `compute`, and `merge`. They exist because interfaces gained **default methods**. `Map.of` / `ofEntries` / `copyOf` are **not** Java 8. Defaults are **not** atomic; `ConcurrentMap` already had some of the conditional writes since 1.5 and re-abstracts them.

## The 1.8 surface

```text
query          getOrDefault(k, default)

walk           forEach(BiConsumer)
               replaceAll(BiFunction)          // setValue on each entry

conditional    putIfAbsent(k, v)
               remove(k, v)                    // true if that pair gone
               replace(k, v)                   // only if mapped
               replace(k, old, new)            // CAS-style; boolean

compute        computeIfAbsent(k, Function)
               computeIfPresent(k, BiFunction)
               compute(k, BiFunction)
               merge(k, v, BiFunction)         // v must be non-null
```

**Listing 1.** `Map` method summary, Java SE 8. Overloads of `remove` / `replace` sit beside the 1.2 methods. `putIfAbsent`, `remove(k,v)`, and both `replace`s were already on `ConcurrentMap` (1.5); Java 8 lifts them to every `Map`.

They are **default** implementations: typically `get` then `put`, or a walk of `entrySet()`. The javadoc says they make **no** synchronization or atomicity guarantees. `HashMap` is still not a concurrent map if you call `computeIfAbsent`. [[What is the difference between HashMap put and computeIfAbsent]]

```d2
direction: down
lang: "Java 8\ndefault methods on interfaces" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
map: "Map default methods\ngetOrDefault … merge" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
entry: "Map.Entry static\ncomparingByKey / ByValue" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
later: "9: of / ofEntries / entry\n10: copyOf\n21: SequencedMap" {
  width: 280
  height: 90
  style.fill: "#ffe0b2"
}

lang -> map
lang -> entry
map -> later: not these
```

**Fig. 1.** Language feature first; factories and sequenced maps later. [[How do you iterate all key value pairs in a Map]] is `forEach` vs `entrySet()`.

`getOrDefault` uses **no mapping**, not “value is null”: a stored `null` is returned, not the default. `putIfAbsent` / `compute*` / `merge` treat “mapped to `null`” like absent. `computeIfAbsent` skips a null result from the function (does not insert). `computeIfPresent` / `compute` / `merge` **remove** the mapping if the function returns `null`. `merge`’s value argument is non-null. `compute(..., (k, v) -> v.concat(...))` **NPEs** when `v` is null — use `(v == null) ? msg : v.concat(msg)` or `merge(key, msg, String::concat)` ([[What is functional interface BiConsumerT,U]], [[What is functional interface BiFunctionT,U,R]], [[Why should you use computeIfAbsent on ConcurrentHashMap]]).

`Map.Entry.comparingByKey` / `comparingByValue` (natural or a `Comparator`) are also 1.8 — on the nested type, not on `Map`.

> [!warning] Do not credit Java 8 with `Map.of`
> Unmodifiable factories are Java **9** (`of`, `ofEntries`, `entry`); `copyOf` is **10**. Hash-bin trees in `HashMap` are a Java 8 **implementation** change, not new `Map` methods. Default `forEach` / `compute*` on `HashMap` are not a lock.

> [!tip] Interview answer
> **Java 8 added default methods on `Map`: `getOrDefault`, `forEach`, `replaceAll`, `putIfAbsent`, conditional `remove`/`replace`, and the four compute/merge methods. They are not atomic. `Map.of` is Java 9. `ConcurrentMap` had `putIfAbsent`/`replace` since 1.5.**
