<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS

# When should a method return a concrete collection type versus an abstraction?

> [!abstract] Short answer
> Return the **most general type that still gives callers the operations they need**: `Iterable` for "iterate once, that's all", `Collection` for size/contains/add-removal semantics, `List`/`Set`/`SortedMap` when the contract — order, uniqueness, keying — is part of your API. Return a concrete class (`ArrayList`, `LinkedHashMap`) only when implementation semantics are the product itself. The JDK models this: `Map.values()` returns a `Collection` view, `Map.keySet()` returns `Set`, not `LinkedHashSet` or `ArrayList` ([[What is the Map interface in Java]]).

## The generality ladder, read from the caller's needs

Each step down the ladder adds contract you must then honor forever. `Iterable` promises only `iterator()`; `Collection` adds `size`, `contains`, and mutation; `List` adds index access and **ordered equality** — two `List`s are equal only if their elements line up position by position. `Set` adds uniqueness and order-insensitive equality. Declaring the wider type keeps you free to swap the implementation later; declaring `ArrayList` in a signature welds callers to a machine choice ([[What is the difference between ArrayList and LinkedList]]).

```d2
direction: right
impl: "Concrete class\nArrayList · LinkedHashMap\nmax commitments" {
  width: 300
  height: 96
  style.fill: "#ffebee"
}
i1: "List / Set / SortedMap\ncontract matters" {
  width: 280
  height: 88
  style.fill: "#fff3e0"
}
coll: "Collection\nsize · contains · mutation" {
  width: 300
  height: 88
  style.fill: "#e3f2fd"
}
it: "Iterable / Stream\n'just iterate / pipeline'" {
  width: 280
  height: 88
  style.fill: "#e8f5e9"
}
impl -> i1: "narrow when the API\nmeans ordered or unique"
i1 -> coll: "narrow to elements-only\nsemantics"
coll -> it: "narrow when callers\nonly read once"
```

**Fig. 1.** Widest reasonable return type: move left only when callers truly need that contract.

```java
public Iterable<String> recentEvents() {        // caller only iterates
    return recent;                              // may even be lazy
}

public List<String> recentEventsIndexed() {     // order + get(i) needed
    return List.copyOf(recent);
}

public Map<String, Integer> scoresByPlayer() {  // keyed lookup needed
    return Collections.unmodifiableMap(scores);
}
```

**Listing 1.** Conceptual signatures: each return type names exactly what the caller may rely on. `List.copyOf` and `Map.copyOf` (Java 10+) hand out unmodifiable copies.

```java
Map<String, Integer> map = new HashMap<>();
map.put("a", 1);
Collection<Integer> values = map.values();
List<Integer> asList = new ArrayList<>(values);
System.out.println(values.getClass().getSimpleName() + " → " + asList);
```

**Listing 2.** The JDK itself returns the abstraction: `values()` is a `Collection` view, and converting is the caller's move. Verified on JDK 21 — output: `Values → [1]`.

> [!warning] Returning `List` for unordered data promises order that callers will rely on
> `List.equals` is order-sensitive, so a "List" of map values silently becomes part of the API contract; `Map.values()` deliberately returns `Collection`. Symmetric trap: returning a mutable `ArrayList` lets callers mutate what you consider internal state — hand out `List.copyOf`/unmodifiable views when the collection is state ([[How do you obtain a read-only or unmodifiable collection in Java]]).

> [!tip] Interview answer
> **Default to the interface that matches the promise: `Iterable` for single-pass reading, `Collection` for element semantics, `List`/`Set`/`Map` when order, uniqueness or keying are the API.** Concrete classes in signatures are a smell unless the implementation is the point. That keeps implementations swappable, prevents accidental contracts like list ordering, and matches how the JDK returns `Set` from `keySet()` or `Collection` from `values()`.
