<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/Collections/Set/TreeSet #Java/Collections/Map/TreeMap #SRS

# Can you use a Java enum with `TreeSet` or `TreeMap`?

> [!abstract] Short answer
> **Yes.** `Enum` implements `Comparable<E>`, which is what a `TreeSet` of values and a `TreeMap` of keys need for natural order. That order is declaration order (`compareTo` / `ordinal`). You still usually want `EnumSet` / `EnumMap` instead: they are specialized for one enum type. Use the tree types when you need a `Comparator` or navigable views (`higher`, `subSet`, `headMap`, …).

## Why it compiles and how it sorts

`TreeSet` and `TreeMap` order by `Comparable.compareTo`, or by a `Comparator` passed to the constructor. Enum constants of one type are mutually comparable. `compareTo` is `final` and uses declaration order ([[Can you override compareTo on a Java enum]]). `equals` is identity, so that order is consistent with `equals` — the contract sorted maps/sets ask for.

You cannot drop constants of two different enum types into one tree: `compareTo` is typed to `E`, and mixing declaring classes is a `ClassCastException` even through a raw collection.

```d2
direction: down
en: "enum Priority\nComparable, declaration order" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
tree: "TreeSet / TreeMap\nlog n, Navigable, optional Comparator" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
spec: "EnumSet / EnumMap\nbit vector / array, same natural order" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}

en -> tree
en -> spec
```

**Fig. 1.** Both families iterate in declaration order. The tree types buy `Navigable*` and a custom comparator; the enum types buy compactness and constant-time ops.

```java
enum Priority { LOW, MEDIUM, HIGH }

class Demo {
    void natural() {
        java.util.TreeSet<Priority> set = new java.util.TreeSet<>();
        set.add(Priority.HIGH);
        set.add(Priority.LOW);
        // iteration: LOW, HIGH  (MEDIUM was never added)

        java.util.TreeMap<Priority, String> map = new java.util.TreeMap<>();
        map.put(Priority.HIGH, "p1");
        map.put(Priority.LOW, "p0");
        // keySet iteration: LOW, HIGH
    }
}
```

**Listing 1.** Natural order among the constants that are actually present — not a listing of every constant.

```java
java.util.TreeSet<Priority> byName = new java.util.TreeSet<>(
        (a, b) -> a.name().compareTo(b.name()));
byName.add(Priority.HIGH);
byName.add(Priority.LOW);
// iteration: HIGH, LOW — alphabetical names, not declaration order
```

**Listing 2.** Conceptual (uses `Priority` from Listing 1): different order without overriding `compareTo`. `EnumSet` has no comparator constructor; this is a real reason to keep `TreeSet`.

`null` is not a legal element/key under natural ordering (`NullPointerException`). Enum constants themselves are never null; `set.add(null)` still is.

## Prefer the enum collections unless you need the tree

`EnumSet` stores a bit vector of constants from one enum type; iteration is declaration order; basic ops are constant time ([[Why does Java provide EnumSet in addition to HashSet and TreeSet]], [[What is EnumSet]]). `EnumMap` stores an array of values indexed by the key type; keys from one enum; also declaration order; constant-time ops ([[Why prefer EnumMap when the keys are enum constants]]).

Reach for `TreeSet`/`TreeMap` with enums when you need:

- a `Comparator` other than declaration order
- `NavigableSet` / `NavigableMap` (`lower`, `floor`, `subSet`, `headMap`, …) — `EnumSet`/`EnumMap` are not navigable
- a sorted view that is not “all keys are this enum” (for example a `TreeMap<Priority, …>` is fine, but so is mixing enum values as *values*, not keys)

> [!warning] Adding `HIGH` and `LOW` does not iterate `MEDIUM`
> Interview snippets often print `LOW, MEDIUM, HIGH` after inserting two constants. The tree only contains what you `add`/`put`. Declaration order ranks **present** elements; it does not insert the missing names.

> [!warning] Legal is not the same as “use TreeSet for enums”
> `TreeSet<Priority>` is O(log n) on a red-black tree. `EnumSet` is the specialized set for this key domain. Answer “yes, because `Comparable`” first, then name `EnumSet`/`EnumMap` unless the interviewer asked for navigable order or a custom comparator.

> [!tip] Interview answer
> **Yes — enums implement `Comparable`, so they work as `TreeSet` elements and `TreeMap` keys, sorted in declaration order.** You cannot mix two enum types. Prefer `EnumSet` and `EnumMap` unless you need a `Comparator` or navigable range views.
