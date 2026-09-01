<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Map/HashMap #Java/HashCodeEquals #SRS

# How does `TreeMap` decide whether two keys are the same?

> [!abstract] Short answer
> By the map’s **ordering**, not by `equals` or `hashCode`. Two keys are the same mapping when `compareTo` (natural order) or `Comparator.compare` returns **0**. `put` then **replaces the value**. `HashMap` instead matches with `equals` after `hashCode` buckets the key.

## Ordering is identity; `equals` is the `Map` contract

`TreeMap.get` looks for a key `k` such that the argument **compares equal** to `k` under the tree’s order. There can be at most one such mapping. `put` uses the same test: if the map already contained that key, the old value is replaced. `hashCode` is not part of that search — the tree is log(n) comparisons.

The `Map` interface still defines `containsKey` / `get` in terms of `equals`. A sorted map that is a correct `Map` therefore needs an ordering **consistent with equals**: `compare(a, b) == 0` if and only if `a.equals(b)`. If you break that, the tree is still well-defined, but `containsKey` and `equals` on the map can disagree with what `HashMap` would do. Full rule: [[Why must TreeMap ordering be consistent with equals]]. Custom `Comparator`s are the usual way to get that wrong ([[How do you customize TreeMap key order]]).

`HashMap.get` is specified with `(key==null ? k==null : key.equals(k))`. Hashing chooses the bucket; `equals` decides the match. Override `equals` and `hashCode` together for hash maps ([[Why should equals and hashCode be overridden together]]). `TreeMap` keys still need a total order, not a hash.

```d2
direction: down
q: "is this the same key?" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
tm: "TreeMap\ncompare / compareTo == 0" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
hm: "HashMap\nhashCode then equals" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
q -> tm
q -> hm
```

**Fig. 1.** Same `Map` method names, different sameness tests. High-level contrast: [[What is the difference between HashMap, TreeMap, and LinkedHashMap]].

```java
import java.util.Comparator;
import java.util.HashMap;
import java.util.TreeMap;

class Demo {
    static void compareZeroIsSameKey() {
        var byLen = new TreeMap<String, Integer>(
                Comparator.comparingInt(String::length));
        byLen.put("One", 1);
        byLen.put("Two", 2);     // length 3 == length 3 → same key
        byLen.size();            // 1
        byLen.get("One");        // 2
        byLen.get("Two");        // 2  — both compare equal
        "One".equals("Two");     // false
    }

    static void hashMapKeepsBoth() {
        var h = new HashMap<String, Integer>();
        h.put("One", 1);
        h.put("Two", 2);
        h.size();                // 2 — equals is false
    }
}
```

**Listing 1.** A length-only `TreeMap` treats `"One"` and `"Two"` as one key. The same `put`s on a `HashMap` are two keys. `BigDecimal` `4.0` vs `4.00` is the core-library example of natural order inconsistent with `equals`.

Mutating a key so its order (or `equals`) changes while it sits in the map is unspecified ([[What happens if you mutate a TreeMap key after insertion]]).

> [!warning] `compare == 0` can merge keys that are not `equals`
> From the tree’s point of view those keys **are** equal. The second `put` replaces the value; `size` does not grow. `Comparable` recommends documenting “natural ordering inconsistent with equals” when you do this on purpose. A `HashMap` would keep both entries.

> [!warning] HashMap bucket trees are not `TreeMap`
> Since Java 8, a crowded `HashMap` bin may become a balanced tree (JEP 180). That is an **implementation** of hashing: specs were not changed. `HashMap.get` is still `equals`. `TreeMap` is a different type: ordered keys, no `hashCode` in the lookup. Comparable keys in a `HashMap` may be used only to **break ties** inside a bin.

> [!tip] Interview answer
> **`TreeMap` treats two keys as the same when `compareTo` or the constructor `Comparator` returns 0 — `hashCode` is unused. `put` replaces the value. `HashMap` uses `hashCode` then `equals`. If compare-zero disagrees with `equals`, the tree is a broken `Map`. Java 8 HashMap tree bins are still HashMap, not TreeMap.**
