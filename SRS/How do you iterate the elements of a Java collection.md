<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# How do you iterate the elements of a Java collection?

> [!abstract] Short answer
> **Enhanced `for`, `iterator()`, or `forEach` — all start from `Iterable`.** Every `Collection` is `Iterable`. For-each is a hidden `iterator()` loop. Keep an explicit `Iterator` when you need `remove()`. Java 8 adds `forEach` and `stream()`. `List` also has `ListIterator`; `Deque` has `descendingIterator()`. `Map` is not a `Collection`: walk `keySet()`, `values()`, or `entrySet()`.

## `Iterable` is the common door

`Collection.iterator()` returns an `Iterator` (order unspecified unless that collection documents one). Enhanced `for` over a collection is exactly that iterator, hidden [[How are Iterable Iterator and for-each related in Java]], [[What types of iterators or cursors exist in Java]].

**Pick by need:**

- **Read only, one collection:** `for (E e : coll)`.
- **Delete during the walk:** `Iterator` + `remove()` after `next()`, or `coll.removeIf(...)` — not `coll.remove` inside for-each [[Can you modify a collection while iterating with a for-each loop]].
- **Java 8 callback:** `coll.forEach(consumer)` (default: enhanced `for` over `this`).
- **Pipeline:** `coll.stream()` / `parallelStream()` (spliterator-backed; not an `Iterator` you hold).
- **List both ways / `set` / `add`:** `list.listIterator()` [[How do you iterate a List in reverse using ListIterator]], [[Compare Iterator and ListIterator capabilities]].
- **Deque tail → head:** `deque.descendingIterator()` or Java 21 `deque.reversed()` [[How can you iterate a Deque in both directions]].
- **Legacy Vector/Hashtable:** `elements()` / `keys()` return `Enumeration` (not fail-fast). Prefer the collection views’ iterators.

Indexed `list.get(i)` is not the iterator API (`LinkedList` makes it quadratic). `Map` iteration is on the views [[How do you iterate all key value pairs in a Map]].

```d2
direction: down
c: "Collection / Iterable" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
fe: "for-each / forEach" {
  width: 240
  height: 50
}
it: "iterator()" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
st: "stream()" {
  width: 180
  height: 50
}

c -> fe
c -> it
c -> st
```

**Fig. 1.** Three everyday doors. For-each and default `forEach` still create an `Iterator`. `stream()` uses a `Spliterator`.

```java
class WalkCollection {
    static void ways(java.util.Collection<String> coll) {
        for (String s : coll) {
            System.out.print(s);
        }
        java.util.Iterator<String> it = coll.iterator();
        while (it.hasNext()) {
            it.next();
        }
        coll.forEach(System.out::print);
        coll.stream().forEach(System.out::print);
    }
}
```

**Listing 1.** All four walk the same `Collection`. Only the `Iterator` variable can call `remove()` in the middle of the walk.

> [!warning] For-each cannot `Iterator.remove()`
> The cursor is compiler-generated. `coll.remove` during for-each is the fail-fast CME story on `ArrayList`. Use an explicit iterator or `removeIf`.

> [!warning] `Map` is not `Iterable`
> `for (V v : map)` does not compile. Iterate `map.values()`, `keySet()`, or `entrySet()` (or `map.forEach`). Hashtable `elements()` is an `Enumeration`, not a fail-fast iterator.

> [!tip] Interview answer
> **For-each over the collection — it is `Iterable` and uses `iterator()` underneath.** Hold the `Iterator` when you must `remove()`. Java 8: `forEach` or a stream. Lists get `ListIterator`; maps are iterated through their views, not as a `Collection`.
