<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #Java/Collections/Iteration #SRS

# How do you traverse a LinkedList in reverse without using get index?

> [!abstract] Short answer
> **`listIterator(list.size())` then `hasPrevious()` / `previous()`, or `descendingIterator()` (since 1.6).** Both walk `prev` links. Java 21 `for (E e : list.reversed())` is a reverse-ordered `List` view. Do not `get(i)` from `size()-1` down: each `get` starts a new walk from an end, so the scan is quadratic.

## Reverse walk holds the node; `get(i)` does not

`LinkedList` is a doubly-linked `List` and `Deque`. Index operations traverse from the nearer end. OpenJDK `get(i)` is `node(index).item` — from `first` if `i < size/2`, else from `last`. Calling `get` again **restarts** that walk. A reverse counted loop is still O(n²).

`ListIterator` has no current element: the cursor sits *between* slots. `listIterator(index)`: `next()` would return the element at `index`; `previous()` returns `index - 1`. `index` may equal `size()`, so `listIterator(list.size())` starts **after** the last node. Repeated `previous()` is tail → head. OpenJDK `ListItr.previous()` follows `node.prev` in O(1) per step [[How do you iterate a List in reverse using ListIterator]].

`descendingIterator()` is the `Deque` reverse iterator (since 1.6): last (tail) to first (head). OpenJDK’s adapter is a `ListItr` parked at `size()` whose `next()` is `previous()`. It is an `Iterator`, not `Iterable` — not a for-each source. For-each reverse since 21: `list.reversed()`, a write-through reverse view (`LinkedList.reversed()` returns a `List`) [[How can you iterate a Deque in both directions]] [[Does LinkedList implement Queue and Deque in Java]].

Forward in-order without `get` is enhanced `for` / `iterator()` [[How do you iterate elements LinkedList in order not using get(index]].

```d2
direction: right
idx: "get(size-1) … get(0)" {
  width: 210
  height: 80
  style.fill: "#fff3e0"
}
restart: "node(i) from an end\nevery call" {
  width: 200
  height: 80
  style.fill: "#ffebee"
}
it: "listIterator(size())\ndescendingIterator()" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
prev: "follow node.prev\nonce per element" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}

idx -> restart
it -> prev
```

**Fig. 1.** Reverse `get(i)` restarts a link walk. A reverse iterator keeps the current node.

```java
class LinkedListReverseWalk {
    static void viaListIterator(java.util.LinkedList<String> list) {
        java.util.ListIterator<String> it = list.listIterator(list.size());
        while (it.hasPrevious()) {
            System.out.print(it.previous());
        }
    }

    static void viaDescending(java.util.LinkedList<String> list) {
        java.util.Iterator<String> it = list.descendingIterator();
        while (it.hasNext()) {
            System.out.print(it.next());
        }
    }

    static void viaReversedView(java.util.LinkedList<String> list) {
        for (String s : list.reversed()) { // Java 21
            System.out.print(s);
        }
    }
}
```

**Listing 1.** For `["a","b","c"]` each prints `cba`. `descendingIterator().next()` is the `Deque` spelling of `previous()`.

```java
java.util.ListIterator<String> wrong = list.listIterator(list.size() - 1);
// first previous() is "b" if the list is [a, b, c] — last element skipped
```

**Listing 2.** Conceptual: `size() - 1` is the last index for `next()`, not “after the last” for `previous()`.

`iterator` / `listIterator` are fail-fast: structural change except that iterator’s own `remove` / `add` throws `ConcurrentModificationException` (best-effort).

> [!warning] `listIterator(size() - 1)` is not reverse from the tail
> Reverse with `previous()` needs the cursor **after** the last element: `listIterator(size())`. `size() - 1` is legal but a `previous()`-only loop never visits the last value. `listIterator(-1)` throws `IndexOutOfBoundsException`; `size()` does not.

> [!warning] Reverse `get(i)` is still the slow walk
> `get(size() - 1)` is cheap once; repeating `get(i)` from the high end still calls `node(i)` each time. `descendingIterator()` is not for-each. `pollLast()` in a loop **mutates** the list — that is draining, not traversing.

> [!tip] Interview answer
> **Do not index. Park a `ListIterator` at `size()` and call `previous()`, or use `descendingIterator()`. ** Each step follows `prev`. Java 21 `reversed()` is the for-each reverse view. `get(i)` from either end restarts a walk, so a reverse counted loop is still quadratic.
