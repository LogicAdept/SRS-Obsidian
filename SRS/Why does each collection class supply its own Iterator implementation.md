<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# Why does each collection class supply its own `Iterator` implementation?

> [!abstract] Short answer
> **Because only that class knows how its elements are stored.** `Iterator` is a protocol (`hasNext` / `next` / optional `remove`), not a shared engine. `AbstractCollection.iterator()` is **abstract**: even an unmodifiable collection must write `iterator()` and `size()`. Array vs nodes vs hash buckets vs snapshot vs weakly consistent walk cannot share one cursor class.

## Protocol shared, cursor private

The Collections Framework lets client code walk any `Collection` the same way. The **representation** stays private, so the object that actually steps through memory has to live next to that representation — almost always a private inner class returned from `iterator()` [[What is the Iterator interface and why do Java collections use it]], [[What is the Iterator design pattern in Java]], [[How do you iterate the elements of a Java collection]].

`AbstractCollection` is explicit: to implement an unmodifiable collection you extend it and provide **`iterator` and `size`**. The iterator must implement `hasNext` and `next`. A modifiable collection must also make that iterator’s `remove` work (the default `Iterator.remove` throws `UnsupportedOperationException`). `contains`, `toArray`, `remove`, `clear` in `AbstractCollection` are all written in terms of **your** iterator.

That is why there is no JDK-wide `Iterator` implementation you reuse for `HashSet` and `ArrayList`.

**What differs per class**

- **Shape.** `ArrayList` walks `elementData` with an index (`ArrayList.Itr`). A linked list walks nodes. `HashSet` walks table buckets. `ArrayDeque` walks a circular array. `Map` is not `Iterable`; its views each have their own iterators [[What types of iterators or cursors exist in Java]].
- **Order.** `List` iterators are in sequence. `HashSet` documents no encounter order. `Collection.iterator()` itself promises none unless the type does.
- **Failure policy.** General-purpose implementations are fail-fast (`modCount`). `CopyOnWriteArrayList` iterators are snapshots (`remove` unsupported). `ConcurrentHashMap` iterators are weakly consistent. Those rules are not on the `Iterator` interface [[What is fail-fast iterator behavior in Java collections]], [[What are examples of fail-safe iterators in Java]], [[What is the difference between fail-fast and fail-safe iterators]], [[What counts as a structural modification for fail-fast iterators]].

**The `AbstractList` exception.** `AbstractList.iterator()` *does* supply a default: it calls `size()`, `get(int)`, and `remove(int)`. That only works because `List` has indexes. It is O(1) `get` on `ArrayList` and O(n) `get` per step on a sequential list if you leave it in place. `ArrayList` still replaces it with `Itr` so it reads the array directly and fail-fast-checks `modCount`. Non-lists cannot use this default at all [[Compare Iterator and ListIterator capabilities]].

Each `iterator()` call must return a **new** cursor. Nested enhanced `for` over the same collection depends on that [[How are Iterable and Iterator related in Java]], [[What is the Iterable interface in Java]].

```d2
direction: down
proto: "Collection.iterator()\nIterator protocol" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
al: "ArrayList.Itr\narray + index" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
hs: "HashSet iterator\nbuckets" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
cow: "COW iterator\nsnapshot" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}

proto -> al
proto -> hs
proto -> cow
```

**Fig. 1.** Clients depend on `Iterator`. Each collection hides a cursor that matches its storage and its modification policy.

```java
final class One extends java.util.AbstractCollection<String> {
    @Override
    public int size() {
        return 1;
    }

    @Override
    public java.util.Iterator<String> iterator() {
        return java.util.List.of("x").iterator();
    }
}
```

**Listing 1.** `AbstractCollection` does not walk your fields for you. `iterator()` is abstract; this class has to supply a cursor.

> [!warning] A `get(i)` loop is not a universal iterator
> Indexing works on `List` and is the `AbstractList` default. It does not exist on `Set` or `Queue`, and it is the wrong complexity on a linked list. Do not assume one iterator class can sit on `Collection`.

> [!warning] Do not make the collection *be* the iterator
> Implementing `Iterator` on the collection and returning `this` from `iterator()` shares one cursor. Nested loops collide. Factory: a **new** inner iterator per `iterator()` call.

> [!tip] Interview answer
> **Each collection hides a different data structure, so each ships its own cursor class.** `Iterator` is only `hasNext` / `next` / optional `remove`. `AbstractCollection` even leaves `iterator()` abstract. Fail-fast, snapshot, and weakly consistent behavior are properties of those concrete iterators, not of the interface.
