<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Set/TreeSet #SRS

# Is `TreeSet` implemented using `TreeMap`?

> [!abstract] Short answer
> **Yes.** `TreeSet` is a `NavigableSet` **based on a `TreeMap`**. Elements are the map’s **keys**. Uniqueness and order are that tree’s `compareTo` / `Comparator` (log(n) `add` / `remove` / `contains`). `HashSet` is the same idea on a `HashMap`.

## A set wrapper around a sorted map

The class specification opens with that sentence. Public constructors build an empty `TreeMap` (natural order or a given `Comparator`) and keep it as a `NavigableMap`. `add` is `put(element, dummy)`; `contains` is `containsKey`; iteration is the map’s navigable key set. Subsets wrap `subMap` / `headMap` / `tailMap`. Clone and deserialization allocate a fresh `TreeMap`.

The dummy is a private static sentinel so every key maps to the same value. You never see that map: `TreeSet` is not a `Map`, and there is no accessor for the backing instance. The red-black tree is `TreeMap`’s ([[What data structure backs TreeMap in Java]], [[Which tree data structure backs Java TreeSet]]).

`HashSet` is specified as backed by a hash table that is **actually a `HashMap` instance** — same set-on-map shape, hash instead of order ([[What internal structures back HashSet and TreeSet]]). Duplicate tests follow the map, so `TreeSet` uses compare-zero, `HashSet` uses `equals` ([[How do HashSet and TreeSet decide whether two elements are duplicates]], [[How does TreeMap decide whether two keys are the same]]).

```d2
direction: down
set: "TreeSet" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
map: "TreeMap\nkeys = elements" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
dummy: "one dummy value\nper mapping" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
set -> map: "add / contains / iterate"
map -> dummy
```

**Fig. 1.** The set is a façade. The tree, comparator, and log(n) cost live on the map.

```java
import java.util.Comparator;
import java.util.TreeSet;

class Demo {
    static void orderedSet() {
        var s = new TreeSet<String>();
        s.add("b");
        s.add("a");
        s.first();          // "a" — map firstKey
        s.contains("b");    // map containsKey
    }

    static void sameCompareZeroRule() {
        var s = new TreeSet<String>(Comparator.comparingInt(String::length));
        s.add("One");
        s.add("Two");       // compare == 0 → not a second element
        s.size();           // 1
    }
}
```

**Listing 1.** Client code stays on `Set`. Length-only order collapses `"One"` and `"Two"` because the backing `TreeMap` does.

```java
// Conceptual — JDK field and add, not a public API
NavigableMap<E, Object> m = new TreeMap<>();
static final Object PRESENT = new Object();
boolean add(E e) { return m.put(e, PRESENT) == null; }
```

**Listing 2.** Conceptual: dummy value, keys only. Same pattern as `HashSet` on `HashMap`.

`EnumSet` is a different `Set` for a single enum type — not this `TreeMap` wrapper ([[Why does Java provide EnumSet in addition to HashSet and TreeSet]], [[Can you use a Java enum with TreeSet or TreeMap]]).

> [!warning] You do not get a `TreeMap` reference
> There is no `asMap()`. Do not downcast. Subviews (`headSet`, `subSet`) are more `TreeSet`s on `subMap` views, still not a public map. Mutating a set element in a way that changes order is as unspecified as mutating a `TreeMap` key.

> [!warning] “No null” is the natural-order case
> `add(null)` throws `NullPointerException` when the set uses natural order **or** a comparator that rejects null — same rule as `TreeMap` keys ([[Can a TreeSet contain null]]). A null-friendly comparator can allow one null, as with `nullsFirst`.

> [!tip] Interview answer
> **Yes — `TreeSet` is a `NavigableSet` implemented on a `TreeMap`: elements are keys, a dummy object is the value, order and uniqueness come from `compare`. `HashSet` is the same trick with `HashMap`. That is why `TreeSet` is log(n) and sorted, and why compare-zero, not `equals`, decides duplicates.**
