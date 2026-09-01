<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Collections/Map/LinkedHashMap #Java/Collections/Map/TreeMap #Java/Language/Enum #SRS

# In what order does `EnumMap` iterate?

> [!abstract] Short answer
> **Declaration order of the enum constants — the keys’ natural order — not `put` order.** `keySet`, `values`, and `entrySet` all walk that sequence. Reordering the constants in the enum type changes iteration. This is not `LinkedHashMap` insertion/access order. `TreeMap` can match enum ordinals by default, but it is a red-black tree and may take a `Comparator`.

## Natural order means source order of the constants

The class javadoc: enum maps are maintained in the natural order of their keys, the order in which the constants are declared. View iterators reflect that. `keySet()` returns keys in that order; `values()` and `entrySet()` follow the same key sequence. [[How do you create an EnumMap]] [[Must EnumMap keys all come from the same enum type]]

`put` of `RUNNING` then `NEW` still iterates `NEW` then `RUNNING` if that is how the enum is written. A second `put` of a live key replaces the value and does not move the slot. Missing constants are simply skipped (the array is sized to the enum; iteration visits present mappings in constant order).

```d2
direction: down
src: "enum State { NEW, RUNNING,\nWAITING, FINISHED }" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
puts: "put RUNNING, WAITING,\nNEW, FINISHED" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
it: "iterator: NEW, RUNNING,\nWAITING, FINISHED" {
  width: 300
  height: 70
  style.fill: "#c8e6c9"
}

src -> it
puts -> it: put order ignored
```

**Fig. 1.** Encounter order is compiled into the enum, not into the map’s `put` history.

```java
enum State { NEW, RUNNING, WAITING, FINISHED }

EnumMap<State, String> m = new EnumMap<>(State.class);
m.put(State.RUNNING, "run");
m.put(State.WAITING, "wait");
m.put(State.NEW, "new");
m.put(State.FINISHED, "done");
// keySet / entrySet / values: NEW, RUNNING, WAITING, FINISHED
```

**Listing 1.** Conceptual: four puts in “runtime” order still iterate in declaration order.

View iterators are **weakly consistent**: they never throw `ConcurrentModificationException` and may or may not show concurrent mods. That is iterator *safety*, not a second ordering rule. Not synchronized. [[Why prefer EnumMap when the keys are enum constants]] [[What are LinkedHashMap ordering guarantees]] [[Does putting an existing key change LinkedHashMap iteration order]]

`LinkedHashMap` default is insertion-order (re-`put` does not move); access-order is LRU. `HashMap` makes no order promise. `TreeMap` sorts with `compareTo` or a `Comparator` — for enum keys without a comparator that is also declaration/`ordinal` order, but you can pass a comparator that scrambles it; `EnumMap` has no comparator constructor. [[Can TreeMap have null keys or null values]]

> [!warning] “I put RUNNING first, so it prints first”
> `EnumMap` is not insertion-ordered. Edit the enum (insert a constant, reorder constants) and every map of that type changes iteration. Do not sort-by-`put` in an `EnumMap`; use `LinkedHashMap` if encounter order must follow inserts.

> [!tip] Interview answer
> **`EnumMap` iterates in the declaration order of the enum constants, for keys, values, and entries.** `put` order does not matter. That is not `LinkedHashMap` insertion order. `TreeMap` of the same enum is ordinal order only while you use natural ordering, not a custom `Comparator`.
