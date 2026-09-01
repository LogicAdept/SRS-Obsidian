<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# What design idea does `ArrayList` implement?

> [!abstract] Short answer
> A **dynamic array**: a `List` over a growable `Object[]`. The JavaDoc’s own name is “resizable-array implementation of the `List` interface,” “roughly equivalent to `Vector`, except that it is unsynchronized.” Indexed `get`/`set` stay constant time; growth is **amortized** on `add`.

## Resizable array, not a linked structure

```d2
direction: down
idea: "Dynamic array / resizable List" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
api: "List: get, set, add, size" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
store: "Object[] + size\nreplace array when full" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

idea -> api -> store
```

**Fig. 1.** The idea is “array that can grow,” not “nodes with pointers.” Internals: [[What backing data structure does ArrayList use internally]].

A language array has a fixed `length` ([[What is the difference between an array and an ArrayList]]). `ArrayList` keeps a **capacity** (that length) and a logical `size()`. When `add` needs more room, it allocates a **new** array and copies — the growth factor is unspecified beyond amortized-constant `add` ([[How does resize ArrayList]]). `get`/`set`/`size`/`iterator` stay O(1); other ops are linear with a **low constant factor compared to `LinkedList`**.

The same idea in the old collections library is `Vector` (synchronized, since 1.0). `ArrayList` (1.2) is that resizable array **without** the intrinsic lock ([[Why was ArrayList added when Vector already existed]]).

```java
List<String> list = new ArrayList<>(16); // capacity hint for the idea
list.add("a");
list.get(0); // O(1) index into the array
```

**Listing 1.** You program to `List`; the design you get is still a contiguous buffer. `LinkedList` is the other `List` idea (doubly-linked `Deque`).

> [!warning] “Dynamic array” is not “automatic shrink”
> Capacity grows on overflow. `remove` does not shrink the `Object[]`; `trimToSize()` does. Confusing size with capacity misses the design.

> [!warning] Not a GoF pattern name
> Interview dumps sometimes say “Iterator” or “adapter.” Those are incidental (`iterator()`, `List` wrapping an array). The defining idea in the specification is **resizable array** + unsynchronized `Vector`.

> [!tip] Interview answer
> **A dynamic / resizable array implementing `List`.** Contiguous `Object[]`, O(1) index, grow-by-copy so append is amortized O(1). Same shape as `Vector`, without synchronization.
