<!--
reps: 0
priority: 0
-->
#Java/Collections/List #SRS

# What is the List interface in Java?

> [!abstract] Short answer
> **`java.util.List` is an ordered `Collection`: you control insert position, you address elements by zero-based index, and you may search.** Unlike `Set`, lists **typically** allow `e1.equals(e2)` duplicates and multiple `null`s when `null` is allowed. Since 21 it extends `SequencedCollection`. It is the interface, not `ArrayList`.

## Ordered `Collection` with indexes

`List` sits in the Collections Framework (since 1.2). Beyond `Collection` it tightens `iterator`, `add`, `remove`, `equals`, and `hashCode`. Four positional methods — `get`, `set`, `add(int, …)`, `remove(int)` — are zero-based, like arrays. Some implementations (`LinkedList`) take time proportional to the index; iterating is typically preferable when you do not know the class [[Does LinkedList implement Queue and Deque in Java]] [[What is an ArrayList]].

`ListIterator` is bidirectional and can `set` / `add` / `remove` at the cursor; you can start it at an index. Search is `indexOf` / `lastIndexOf` (and `contains`): often a linear `equals` scan — use with caution [[How do you search and remove elements in a List]]. `subList(from, to)` is a view; `subList(from, to).clear()` is the documented range-delete idiom. Bulk insert at an index is `addAll(int, Collection)`.

`equals` is the same size and pairwise `Objects.equals` **in the same order**. A list that contains itself as an element makes `equals` / `hashCode` ill-defined. Optional restrictions (`null`, types) throw unchecked exceptions or may return `false` on queries.

Java 21 sequenced ops (`getFirst` / `getLast` / `addFirst` / `addLast` / `reversed()`) come from `SequencedCollection`. `List.of` / `List.copyOf` are unmodifiable, reject `null`, and throw `UnsupportedOperationException` on mutators.

Not a `Set`: uniqueness is not the contract; `Set` has no `get(int)` [[What is the difference between List and Set]]. Concrete types include `ArrayList` (resizable array), `LinkedList` (doubly-linked `List`+`Deque`), `Vector`, `CopyOnWriteArrayList`.

```d2
direction: right
coll: "Collection" {
  width: 140
  height: 70
  style.fill: "#fff3e0"
}
seq: "SequencedCollection\n(Java 21)" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
list: "List\nindex + ListIterator" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}

coll -> seq -> list
```

**Fig. 1.** `List` is a sequenced `Collection` with positional access. `ArrayList` / `LinkedList` are implementations.

```java
java.util.List<String> list = new java.util.ArrayList<>();
list.add("a");
list.add(0, "b");           // positional insert
String at = list.get(1);    // "a"
int i = list.indexOf("a");  // 1
list.subList(0, 1).clear(); // drop the range [0, 1)
```

**Listing 1.** Interface-visible operations: append, insert at index, `get`, search, range delete via `subList`.

```java
java.util.List<String> frozen = java.util.List.of("x", "y");
frozen.add("z"); // UnsupportedOperationException
```

**Listing 2.** Conceptual: `List.of` is a `List` that rejects mutation. Copy into an `ArrayList` if you need `add`.

> [!warning] `List` is not “always an array” and not “always O(1) `get`”
> `LinkedList.get(i)` walks from an end. `List.of` is a `List` and still not resizable. Program to `List` when any sequence will do; pick `ArrayList` or `LinkedList` when the cost model matters.

> [!warning] Duplicates are typical, not mandatory
> The spec allows a list that throws on duplicate insert; that usage is expected to be rare. `null` policy is per implementation (`List.of` forbids it; `ArrayList` / `LinkedList` allow it). Do not call `equals` on a list that contains itself.

> [!tip] Interview answer
> **`List` is the ordered collection with indexes and (usually) duplicates — a `Collection` plus `get(i)` and `ListIterator`.** It is not `ArrayList`. Search is often linear. `equals` compares the sequence. `Set` is the unique-membership counterpart. Since 21, `reversed()` and first/last are on the sequenced superinterface.
