<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# What is the Iterator design pattern in Java?

> [!abstract] Short answer
> **A separate cursor object walks an aggregate without exposing how that aggregate is stored.** In Java the aggregate is `Iterable` / `Collection` (`iterator()`). The cursor is `java.util.Iterator` (`hasNext` / `next`, optional `remove`). Each collection type supplies its own iterator class. The client can walk `Collection` without knowing array vs nodes vs hash table.

## Cursor separate from the collection

The Collections Framework is a unified API so you manipulate a group of elements **independently of implementation details**. Traversal is part of that: you never index an `ArrayList` from client code that must also walk a `HashSet`. You ask the aggregate for an iterator and drive `hasNext` / `next` [[What is the Iterator interface and why do Java collections use it]], [[How do you iterate the elements of a Java collection]].

**Java mapping**

| Role | Java type |
| --- | --- |
| Aggregate (factory) | `Iterable.iterator()`; `Collection` extends `Iterable` |
| Concrete aggregate | `ArrayList`, `HashSet`, `ArrayDeque`, … |
| Iterator (protocol) | `java.util.Iterator` since 1.2 |
| Concrete iterator | typically a **private inner class** holding a cursor (`ArrayList.Itr`, and so on) |

`iterator()` must return a **new** cursor each call so two walks do not share position. Putting `Iterator` on the collection type itself and returning `this` is the nested-loop trap [[How are Iterable and Iterator related in Java]], [[Why does each collection class supply its own Iterator implementation]].

Java 5 added `Iterable` so enhanced `for` is the language sugar for this pattern: hidden `iterator()` / `hasNext` / `next`. `Iterator` is **not** `Iterable`; `for (E e : someIterator)` does not compile [[What is the Iterable interface in Java]], [[How are Iterable Iterator and for-each related in Java]].

`ListIterator` is a **richer** iterator for `List` only (bidirectional, `add` / `set`). There is no `Iterator.add` because `Iterator` does not promise encounter order [[Compare Iterator and ListIterator capabilities]], [[Why is there no add method on Iterator]]. `Enumeration` is the 1.0 precursor. `Map` is not an aggregate for this pattern; walk `keySet()` / `values()` / `entrySet()`. Arrays are for-each targets without `Iterable`. `Spliterator` is a later, splittable cursor for streams — not the classic single-thread Iterator pattern [[What types of iterators or cursors exist in Java]], [[What is Spliterator]].

Fail-fast `modCount` checks, snapshot iterators, and weakly consistent concurrent iterators are **Java policies** on concrete iterators, not the pattern itself.

```d2
direction: down
agg: "Iterable / Collection\niterator()" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
al: "ArrayList" {
  width: 140
  height: 45
}
hs: "HashSet" {
  width: 140
  height: 45
}
proto: "Iterator\nhasNext / next" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
itr: "ArrayList.Itr" {
  width: 160
  height: 45
  style.fill: "#e8f5e9"
}
hitr: "HashSet iterator" {
  width: 180
  height: 45
  style.fill: "#e8f5e9"
}

agg -> proto
al -> agg
hs -> agg
al -> itr
hs -> hitr
itr -> proto
hitr -> proto
```

**Fig. 1.** Client code depends on `Iterator`, not on array indexes or hash buckets. Each concrete collection hides its own cursor class.

```java
static void printAll(java.util.Collection<?> source) {
    java.util.Iterator<?> it = source.iterator();
    while (it.hasNext()) {
        System.out.println(it.next());
    }
}
```

**Listing 1.** Same walk for `ArrayList`, `HashSet`, or any other `Collection`. The iterator — not the caller — knows the representation.

> [!warning] The collection is not the iterator
> Implementing `Iterator` on the aggregate and returning `this` from `iterator()` shares one cursor. Nested enhanced `for` over the same object then collides. Factory: **new** iterator per `iterator()` call.

> [!warning] External cursor vs `forEach`
> `Iterator` is an **external** iterator: the client calls `next`. `Iterable.forEach` is an **internal**-iteration API (you pass a `Consumer`). The default `forEach` is still specified as enhanced `for` over `this`, so it uses `iterator()` underneath. Overriding `forEach` does not change enhanced `for`.

> [!tip] Interview answer
> **The Iterator pattern is a cursor object that walks a collection without exposing its structure.** In Java, `Collection`/`Iterable` is the aggregate (`iterator()`), and `java.util.Iterator` is the cursor (`hasNext`/`next`). Each collection type ships its own iterator implementation. Enhanced `for` is that pattern with a hidden iterator; `Iterator` itself is not a for-each target.
