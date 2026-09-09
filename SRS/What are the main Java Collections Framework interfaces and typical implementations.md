<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS

# What are the main Java Collections Framework interfaces and typical implementations?

> [!abstract] Short answer
> Four element interfaces cover the `Collection` tree — **`List`** (ordered, index access, duplicates), **`Set`** (no duplicates), **`Queue`**/`Deque` (holding before processing, both ends) — plus **`Map`** for key-value mappings in its own tree. The JDK's typical implementations: `ArrayList`/`LinkedList` for `List`, `HashSet`/`LinkedHashSet`/`TreeSet` for `Set`, `ArrayDeque`/`LinkedList`/`PriorityQueue` for `Queue`/`Deque`, and `HashMap`/`LinkedHashMap`/`TreeMap` for `Map`.

## Interface → implementation map

The implementation Javadocs name the backing machine directly: `ArrayList` is a "resizable-array implementation of the `List` interface"; `HashSet` is backed by "a hash table (actually a `HashMap` instance)" ([[How is HashSet implemented in terms of HashMap]]); `TreeSet` is "based on a `TreeMap`" ([[Is TreeSet implemented using TreeMap]]); `ArrayDeque` is a "resizable-array implementation of the `Deque` interface"; `PriorityQueue` is "an unbounded priority queue based on a priority heap" ([[What are the time complexities of PriorityQueue operations]]).

| Interface | Typical implementations | Backing structure | Ordering | `null` elements |
| --- | --- | --- | --- | --- |
| `List` | `ArrayList`, `LinkedList` | dynamic array; doubly-linked list | insertion/index order | allowed ([[What is an ArrayList]]) |
| `Set` | `HashSet`, `LinkedHashSet`, `TreeSet` | `HashMap`; hash + linked list; red-black tree via `TreeMap` | none; insertion; sorted | `HashSet` one; `TreeSet` none ([[Can a TreeSet contain null]]) |
| `Queue`/`Deque` | `ArrayDeque`, `PriorityQueue`, `LinkedList` | circular resizable array; binary heap; linked nodes | FIFO/LIFO ends; priority | `ArrayDeque` and `PriorityQueue` forbid ([[Does PriorityQueue allow null]]) |
| `Map` | `HashMap`, `LinkedHashMap`, `TreeMap` | hash buckets; hash + doubly-linked list; red-black tree | none; insertion; sorted by key | `HashMap` one null key; `TreeMap` none ([[Can TreeMap have null keys or null values]]) |

```d2
direction: right
list: "List\nArrayList · LinkedList" {
  width: 260
  height: 72
  style.fill: "#e3f2fd"
}
set: "Set\nHashSet · LinkedHashSet · TreeSet" {
  width: 320
  height: 72
  style.fill: "#e8f5e9"
}
queue: "Queue / Deque\nArrayDeque · PriorityQueue · LinkedList" {
  width: 360
  height: 72
  style.fill: "#fff3e0"
}
map: "Map (separate root)\nHashMap · LinkedHashMap · TreeMap" {
  width: 340
  height: 72
  style.fill: "#ffebee"
}
```

**Fig. 1.** The four working interfaces with their everyday implementations; `LinkedList` serves two interfaces at once (`List` and `Deque` — [[Does LinkedList implement Queue and Deque in Java]]).

```java
List<String> tasks = new ArrayList<>();       // index access
Set<Integer> ids = new HashSet<>();           // uniqueness
Deque<String> undo = new ArrayDeque<>();      // ends, stack/queue use
Map<String, Integer> scores = new HashMap<>(); // keyed lookup
```

**Listing 1.** The common idiom: declare the interface, instantiate the implementation.

> [!warning] "Typical" is per workload, not per interface
> `LinkedList` is rarely the best `List`: `ArrayDeque` is documented as "likely to be faster than `LinkedList` when used as a queue" ([[When is ArrayList faster than LinkedList and when is it slower]]). And `LinkedHashSet` exists precisely because plain `HashSet` gives no iteration-order guarantee ([[When should you choose HashSet LinkedHashSet or TreeSet]]).

> [!tip] Interview answer
> **The core interfaces are `List`, `Set`, `Queue`/`Deque` under `Collection`, and `Map` as a separate root.** Typical implementations: `ArrayList` for indexed access, `HashSet`/`LinkedHashSet`/`TreeSet` for uniqueness with none/insertion/sorted order, `ArrayDeque` for both ends, `PriorityQueue` for a heap, and `HashMap`/`LinkedHashMap`/`TreeMap` for keyed lookup with the same ordering trio. Choose by required operations and ordering, then program to the interface.
