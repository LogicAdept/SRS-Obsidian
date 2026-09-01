<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# What is the `Iterator` interface and why do Java collections use it?

> [!abstract] Short answer
> **`java.util.Iterator<E>` (Java 1.2) is the cursor over a collection: `hasNext()`, `next()`, and optional `remove()`.** Collections use it so one loop walks any `Collection` without knowing array indexes, linked nodes, or hash buckets. It replaced `Enumeration` with better names and a defined in-iteration `remove`. Enhanced `for` is this cursor, hidden.

## Uniform cursor, per-collection engine

`Collection.iterator()` (and `Iterable.iterator()`) returns an `Iterator` over that source. There is **no** order promise unless the collection type documents one (`List` does; `HashSet` does not) [[How do you iterate the elements of a Java collection]], [[What interface lets you traverse elements of a Java collection]].

**Contract**

- `hasNext()` — more elements?
- `next()` — next element, or `NoSuchElementException` if none [[What happens if you call Iterator.next without calling hasNext first]]
- `remove()` — delete the last element returned by `next()`, **once**, or `IllegalStateException`. The **default** method throws `UnsupportedOperationException`. Collection implementations that allow it override it [[How do you remove an element from a collection while iterating]]
- `forEachRemaining(Consumer)` (Java 8 default) — drain the rest with `next()`

**Why the framework standardized on it**

The Collections Framework is a unified API so you manipulate a group of elements independently of representation. Indexing `get(i)` is `List`-only and slow on a linked list. `Enumeration` (1.0) had `hasMoreElements` / `nextElement` and **no** `remove`. `Iterator` is the 1.2 replacement: same idea, shorter names, optional `remove` with defined semantics [[What is the difference between Enumeration and Iterator in Java]], [[In which Java version was Iterator introduced]].

Each collection type still **implements** its own iterator (inner class with a cursor). The **interface** is shared so client code and algorithms stay generic [[Why does each collection class supply its own Iterator implementation]], [[What is the Iterator design pattern in Java]]. There is no `Iterator.add`: the protocol does not promise encounter order, so “insert here” has no single meaning. `ListIterator` adds `add` / `set` / `previous` for lists only [[Why is there no add method on Iterator]], [[Compare Iterator and ListIterator capabilities]].

Java 5 `Iterable` is the **source** that produces iterators. Enhanced `for` over a collection is exactly `iterator()` + `hasNext` / `next`. `Iterator` itself is **not** a for-each target [[How are Iterable and Iterator related in Java]], [[How are Iterable Iterator and for-each related in Java]], [[What is the Iterable interface in Java]]. `Map` is not `Iterable`; walk a collection view.

Fail-fast `ConcurrentModificationException` on `ArrayList` / `HashSet` iterators is a **concrete** policy, not part of the `Iterator` interface.

```d2
direction: down
col: "Collection / Iterable" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
it: "Iterator<E>" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
hn: "hasNext()" {
  width: 140
  height: 40
}
nx: "next()" {
  width: 120
  height: 40
}
rm: "remove()\noptional" {
  width: 150
  height: 50
}

col -> it: "iterator()"
it -> hn
it -> nx
it -> rm
```

**Fig. 1.** The collection is the source. `Iterator` is the cursor the framework (and enhanced `for`) actually drives.

```java
static int count(java.util.Collection<?> source) {
    int n = 0;
    java.util.Iterator<?> it = source.iterator();
    while (it.hasNext()) {
        it.next();
        n++;
    }
    return n;
}
```

**Listing 1.** The same `Iterator` loop works for `ArrayList`, `HashSet`, or any other `Collection`. `hasNext()` does not consume; `next()` does.

> [!warning] `Iterator` is not `Iterable`
> `for (E e : someIterator)` does not compile. Implement `Iterable` or use `while (it.hasNext())`. Returning `this` from `iterator()` if the collection also *is* an `Iterator` shares one cursor and breaks nested loops.

> [!warning] Default `remove` is unsupported
> `Iterator.remove()`’s default body throws `UnsupportedOperationException`. Unmodifiable collections and snapshot iterators (for example `CopyOnWriteArrayList`) keep that. Even when `remove` works, `collection.remove(...)` during a fail-fast walk is a different path and usually `ConcurrentModificationException`.

> [!tip] Interview answer
> **`Iterator` is the Java 1.2 cursor: `hasNext` / `next`, optional `remove`.** Collections use it so every `Collection` is walked the same way, without exposing its structure, and so in-iteration remove has a defined method. `Iterable` (Java 5) is the factory enhanced `for` calls. Iterator is not Iterable.
