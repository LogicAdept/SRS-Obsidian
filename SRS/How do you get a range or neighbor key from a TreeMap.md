<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #SRS

# How do you get a range or neighbor key from a `TreeMap`?

> [!abstract] Short answer
> Use the `SortedMap` / `NavigableMap` API `TreeMap` implements. Ranges are **views**: `subMap`, `headMap`, `tailMap`. Neighbors are **lookups** that return `null` when missing: `floorKey` / `ceilingKey` (inclusive) and `lowerKey` / `higherKey` (strict). Ends are `firstKey` / `lastKey` or `firstEntry` / `lastEntry`; `pollFirstEntry` / `pollLastEntry` also **remove**.

## Ranges are views; neighbors are searches

`TreeMap` is a `NavigableMap` (since 6) on top of `SortedMap`. Range methods return a live view backed by the same tree — puts and removes show up on both sides. An insert whose key is outside the view’s range throws `IllegalArgumentException`. The two-argument forms keep `SortedMap` defaults:

| Call | Keys in the view |
| --- | --- |
| `subMap(from, to)` | `from` **inclusive**, `to` **exclusive** (`subMap(from, true, to, false)`) |
| `headMap(to)` | strictly **less than** `to` (`headMap(to, false)`) |
| `tailMap(from)` | **greater than or equal to** `from` (`tailMap(from, true)`) |

The three- and four-argument overloads add `boolean` inclusive flags. If `fromKey` equals `toKey`, two-arg `subMap` is empty; the four-arg form is empty unless **both** endpoints are inclusive. `fromKey > toKey` throws `IllegalArgumentException`. The endpoints need not already be keys in the map.

Neighbor methods locate the closest key; they do not walk the map. `*Entry` variants return a **snapshot** `Map.Entry` that does not support `setValue`.

```d2
direction: right
k: "keys 1 · 2 · 3" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
low: "lower(2) → 1\nfloor(2) → 2" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
high: "ceiling(2) → 2\nhigher(2) → 3" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
k -> low
k -> high
```

**Fig. 1.** Inclusive `floor` / `ceiling` vs strict `lower` / `higher`. Same idea for `*Entry`. See [[What interfaces does TreeMap implement]] and [[When was NavigableMap introduced for TreeMap]].

```java
import java.util.TreeMap;

class Demo {
    static void rangeAndNeighbors() {
        var m = new TreeMap<Integer, String>();
        m.put(1, "Banana");
        m.put(2, "Orange");
        m.put(3, "Apple");

        m.subMap(1, 3);           // {1=Banana, 2=Orange}  — [1, 3)
        m.subMap(1, true, 3, true); // includes 3 as well
        m.headMap(2);             // {1=Banana}            — < 2
        m.tailMap(2);             // {2=Orange, 3=Apple}   — ≥ 2

        m.floorKey(2);            // 2
        m.ceilingKey(2);          // 2
        m.lowerKey(2);            // 1
        m.higherKey(2);           // 3
        m.floorKey(0);            // null — no key ≤ 0
    }

    static void ends() {
        var m = new TreeMap<Integer, String>();
        m.firstEntry();           // null on empty
        // m.firstKey();          // NoSuchElementException on empty
        m.put(1, "a");
        m.put(2, "b");
        m.pollFirstEntry();       // removes 1=a; map left {2=b}
    }
}
```

**Listing 1.** Two-arg `subMap(1, 3)` is the dump’s `[1, 3)` slice. `floorKey(2)` and `ceilingKey(2)` both yield `2` when `2` is present; `lowerKey` / `higherKey` skip it. `poll*` mutates.

`HashMap` has no range or neighbor API — only `get` / `put` / the three collection views. That is one reason to pick `TreeMap` when you need ordered slices; log(n) cost and a required key order are the others ([[Compare HashMap and TreeMap tradeoffs]], [[How do you customize TreeMap key order]]).

> [!warning] Half-open `subMap` and live views
> `subMap(1, 3)` does **not** include key `3`. Use `subMap(1, true, 3, true)` for a closed interval. The result is not a copy: `view.put(0, x)` throws `IllegalArgumentException` if `0` is outside the range, and `view.remove(2)` deletes `2` from the backing map.

> [!warning] `firstKey` vs `poll` vs `null`
> `firstKey` / `lastKey` throw `NoSuchElementException` on an empty map. `firstEntry` / `lastEntry` / `floorKey` / `ceilingKey` / `lowerKey` / `higherKey` return `null` when there is no such key. `pollFirstEntry` / `pollLastEntry` return that snapshot **and remove** the mapping. A `null` search key under natural order still throws `NullPointerException`.

> [!tip] Interview answer
> **Ranges: `subMap` / `headMap` / `tailMap` — live views, two-arg `subMap` is inclusive–exclusive. Neighbors: `floorKey` / `ceilingKey` for ≤ / ≥, `lowerKey` / `higherKey` for strict, `null` if none. Ends: `firstKey` throws when empty; `pollFirstEntry` removes. HashMap cannot do any of this.**
