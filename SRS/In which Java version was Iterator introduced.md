<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Versions #SRS

# In which Java version was `Iterator` introduced?

> [!abstract] Short answer
> **Java 1.2**, with the Collections Framework — same generation as `ListIterator` and `ArrayList`. `Enumeration` is older (**Java 1.0**). Do not mix this up with `Iterable` / enhanced `for` (Java 5) or `Spliterator` (Java 8).

## 1.2 cursor, not 1.0 and not 8

`java.util.Iterator` is marked since **1.2**. It takes the place of `Enumeration` in the Collections Framework: shorter names (`hasNext` / `next` vs `hasMoreElements` / `nextElement`) and an optional `remove`. New code should prefer `Iterator`; `Enumeration.asIterator()` (Java 9) is only an adapter whose `remove` throws `UnsupportedOperationException` [[What is the difference between Enumeration and Iterator in Java]], [[What is the Iterator interface and why do Java collections use it]].

`Enumeration` (since **1.0**) is the Vector / Hashtable-era cursor: the specification’s example is `Vector.elements()`, and it also covers hashtable keys and values [[In which Java version was Hashtable introduced]].

`ListIterator` is also since **1.2** — the `List`-only bidirectional cursor, not a later add-on [[Compare Iterator and ListIterator capabilities]].

`Spliterator` is since **1.8**, for streams and splitting, not a rename of `Iterator` [[What is Spliterator]]. `Iterator.forEachRemaining` is likewise Java 8. The `remove` **method** has been on `Iterator` since 1.2; making it a `default` that throws `UnsupportedOperationException` is the Java 8 shape.

```d2
direction: right
e: "Enumeration\nJava 1.0" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
i: "Iterator\nListIterator\nJava 1.2" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
s: "Spliterator\nforEachRemaining\nJava 8" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}

e -> i -> s
```

**Fig. 1.** Framework cursor timeline. `Iterator` is the 1.2 Collections type. Java 8 added a parallel traversal type, not the original iterator.

```java
class IteratorSince {
    static void walk(java.util.List<String> list) {
        java.util.Iterator<String> it = list.iterator(); // type exists since 1.2
        while (it.hasNext()) {
            it.next();
        }
    }
}
```

**Listing 1.** Using `Iterator` does not require Java 8. `forEachRemaining` and `Spliterator` do. Generics on the listing need Java 5; the `Iterator` type itself is 1.2.

> [!warning] `Iterator` ≠ `Iterable` ≠ `Spliterator`
> `Iterator` is 1.2. Enhanced `for` needs `Iterable` (Java 5). `Spliterator` is Java 8. Answering “Java 8” because of streams mixes up the stream engine with the collections cursor.

> [!warning] Default `remove()` is not when `Iterator` appeared
> Java 8 made `remove` a default method (throws `UnsupportedOperationException` unless overridden). The interface and the remove operation are 1.2.

> [!tip] Interview answer
> **`Iterator` is Java 1.2 — Collections Framework, same wave as `ListIterator`.** `Enumeration` is Java 1.0 (`Vector` / `Hashtable`). Java 8 is `Spliterator` and `forEachRemaining`, not the introduction of `Iterator`.
