<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS

# What is the difference between the Collection interface and the Collections utility class?

> [!abstract] Short answer
> `java.util.Collection` is the **root interface** of the element-container hierarchy — a type that instances implement and that you pass around as a parameter or return value. `java.util.Collections` is a **final utility class that consists exclusively of static methods**: polymorphic algorithms (`sort`, `binarySearch`, `shuffle`), wrapper factories (`unmodifiableList`, `synchronizedMap`), and empty/singleton constants. You implement or declare a `Collection`; you only call `Collections`.

## Two different roles

`Collection` declares instance operations — `add`, `remove`, `contains`, `size`, `iterator`, `toArray` and the bulk operations — and is implemented by everything from `ArrayList` to `HashSet` ([[What is collection]]). `Collections` has no instances and no storage; its Javadoc states it "contains polymorphic algorithms that operate on collections, 'wrappers', which return a new collection backed by a specified collection, and a few other odds and ends". The algorithms mutate or inspect the collection you pass in — the "destructive" ones (`sort`, `reverse`, `shuffle`) throw `UnsupportedOperationException` when the target does not support the mutation primitive, such as `set` on a fixed-size list ([[How do you obtain a read-only or unmodifiable collection in Java]]).

```d2
direction: right
c: "interface Collection<E>\ninstances: ArrayList, HashSet…" {
  width: 330
  height: 90
  style.fill: "#e3f2fd"
}
x: "class Collections\nall-static toolbox" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
c -> x: "sort / shuffle / binarySearch\nreverse / min / max"
x -> c: "wrappers & factories\nunmodifiableXxx · synchronizedXxx\nemptyList · singleton"
```

**Fig. 1.** The relationship is mutual at the API level: `Collections` algorithms consume and decorate `Collection` types, but only one of the two is ever instantiated.

```java
List<Integer> data = new ArrayList<>(List.of(3, 1, 2));
Collections.sort(data);                       // static algorithm on the interface type
System.out.println(data);

List<Integer> frozen = Collections.unmodifiableList(data);
System.out.println(Collections.max(frozen));  // query algorithm

List<String> empty = Collections.emptyList(); // shared constant
System.out.println(empty.size());
```

**Listing 1.** Verified on JDK 21 — output: `[1, 2, 3]` / `3` / `0`.

> [!warning] Wrappers from `Collections` are views, not copies
> `Collections.unmodifiableList(data)` still reflects every later change of `data`, and mutating it directly throws `UnsupportedOperationException`. An unmodifiable view of a mutable list is not an immutable list — if the backing list leaks, the "read-only" guarantee evaporates ([[When should you use Collections emptyList versus a new empty list instance]]).

> [!tip] Interview answer
> **`Collection` is the interface — the type of actual element containers; `Collections` is a static utility class of algorithms and wrapper factories that operate on such containers.** You call `Collections.sort(list)`, `Collections.unmodifiableList(list)`, or grab `Collections.emptyList()`; you never have a `Collections` instance, while `Collection` is exactly what you declare parameters and fields as.
