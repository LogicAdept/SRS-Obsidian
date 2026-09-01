<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# What interface lets you traverse elements of a Java collection?

> [!abstract] Short answer
> **`Iterator`.** `Collection.iterator()` (from `Iterable`) returns an `Iterator` with `hasNext()` / `next()` and optional `remove()`. `Iterable` is the **source** (for-each target); `Iterator` is the **cursor**. `ListIterator` extends `Iterator` for lists. `Enumeration` is the 1.0 predecessor. `Map` is not a `Collection` — traverse `keySet()` / `values()` / `entrySet()`.

## Cursor vs source

`Iterator` is “an iterator over a collection.” It replaced `Enumeration` in the Collections Framework: shorter names and optional `remove` [[What is the Iterator interface and why do Java collections use it]], [[What types of iterators or cursors exist in Java]].

You obtain one with `collection.iterator()`. `Collection` extends `Iterable`; `Iterable.iterator()` is the same factory. Enhanced `for` over a collection calls that method and hides the cursor [[How are Iterable and Iterator related in Java]], [[How do you iterate the elements of a Java collection]].

`Iterable` does **not** walk: it only **produces** iterators. Implementing `Iterator` on your type without `Iterable` does not enable for-each. `ListIterator` adds `previous` / `set` / `add` and exists only on `List`. `Spliterator` (Java 8) is a different type for splitting/streams, not `hasNext`/`next`.

```d2
direction: down
c: "Collection extends Iterable" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
it: "iterator()" {
  width: 180
  height: 45
}
cur: "Iterator\nhasNext / next / remove" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

c -> it -> cur
```

**Fig. 1.** The collection is `Iterable`. Traversal methods live on the `Iterator` it returns.

```java
class TraverseWithIterator {
    static void walk(java.util.Collection<String> coll) {
        java.util.Iterator<String> it = coll.iterator();
        while (it.hasNext()) {
            it.next();
        }
        for (String s : coll) {
            System.out.print(s);
        }
    }
}
```

**Listing 1.** Explicit `Iterator` and enhanced `for` both traverse via `iterator()`. Only the explicit variable can call `remove()`.

> [!warning] `Iterable` is not the walker
> `for (E e : someIterator)` does not compile. Pass the `Collection` / `Iterable`. `Iterator` itself is not `Iterable`.

> [!warning] `Collection` is not `Map`
> `Map` has no `iterator()`. Walk a view. Hashtable `keys()`/`elements()` return `Enumeration`, not `Iterator`.

> [!tip] Interview answer
> **`Iterator` — from `collection.iterator()`.** `hasNext` / `next`, optional `remove`. `Iterable` is what for-each uses to *get* that iterator. Lists may use `ListIterator`; maps are traversed through their views.
