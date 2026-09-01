<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Collections/List #SRS

# Compare `Iterator` and `ListIterator` capabilities

> [!abstract] Short answer
> **`ListIterator` is an `Iterator` with a list cursor:** still `hasNext` / `next` / optional `remove`, plus `hasPrevious` / `previous`, `nextIndex` / `previousIndex`, `set`, and `add`. `Iterator` is the general `Iterable` walk (any `Collection`, and other `Iterable`s). `ListIterator` exists only on `List` (`listIterator()` / `listIterator(int)`). The list cursor sits **between** elements, not on one.

## Same family, extra list operations

`ListIterator` **extends** `Iterator`. Everything an `Iterator` can do, a `ListIterator` can do. The extra methods are defined only on the list iterator [[What types of iterators or cursors exist in Java]], [[What is the Iterator interface and why do Java collections use it]].

**Direction.** `Iterator` is forward: `hasNext` / `next`. `ListIterator` also walks backward: `hasPrevious` / `previous`. Alternating `next` and `previous` returns the **same** element repeatedly. Reverse walk: `list.listIterator(list.size())` then `previous()` [[How do you iterate a List in reverse using ListIterator]].

**Cursor.** A `ListIterator` has **no current element**. Its position is between what `previous()` would return and what `next()` would return. A list of length `n` has `n+1` cursor slots. `nextIndex()` is `size()` at the end; `previousIndex()` is `-1` at the start. `Iterator` has no index API.

**Mutation.** `Iterator.remove()` deletes the last element `next()` returned (once per `next()`). `ListIterator.remove()` deletes the last `next()` **or** `previous()`. `ListIterator.set` replaces that last returned element. `ListIterator.add` inserts immediately before `next()` and after `previous()` (new element sits before the cursor). `Iterator` has **no** `set` or `add` — insert-at-cursor is undefined without a sequence [[Why is there no add method on Iterator]], [[How do you remove an element from a collection while iterating]].

**Where you get them.** `iterable.iterator()` — any `Collection` (`Set`, `Queue`, `Deque`, map views, …). `list.listIterator()` — `List` only. A `HashSet` has no `ListIterator`. `Deque.descendingIterator()` is still an `Iterator`, not a `ListIterator`.

Both inherit `forEachRemaining` (Java 8). `remove` / `set` / `add` remain optional (`UnsupportedOperationException` on unmodifiable lists).

```d2
direction: down
it: "Iterator\nIterable.iterator()" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
fwd: "hasNext next\nremove (last next)" {
  width: 280
  height: 70
}
li: "ListIterator extends Iterator\nList.listIterator()" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
extra: "hasPrevious previous\nindexes  set  add" {
  width: 300
  height: 70
}

it -> fwd
it -> li
li -> extra
```

**Fig. 1.** `ListIterator` is a subinterface. Extra power is the list cursor (between elements), not a different fail-fast story.

```java
class IteratorVsListIterator {
    static void forward(java.util.Collection<String> coll) {
        java.util.Iterator<String> it = coll.iterator();
        while (it.hasNext()) {
            if (it.next().isEmpty()) {
                it.remove();
            }
        }
    }

    static void bothWays(java.util.List<String> list) {
        java.util.ListIterator<String> it = list.listIterator();
        while (it.hasNext()) {
            String s = it.next();
            if (s.isEmpty()) {
                it.set("(empty)");
                it.add("inserted-after-empty");
            }
        }
        while (it.hasPrevious()) {
            it.previous();
        }
    }
}
```

**Listing 1.** `forward` compiles for any `Collection`. `bothWays` needs a `List`. `it.set` / `it.add` do not exist on `Iterator`.

> [!warning] `Iterator` already has `remove`
> A dump that says only `ListIterator` can modify the collection is wrong. `Iterator.remove()` is the specified in-walk delete. What `ListIterator` adds is **`set` and `add`**, and `remove` after `previous()`.

> [!warning] Between-elements cursor
> `add` is defined on the **gap**, `remove`/`set` on the **last returned** element. After `add`, `remove`/`set` throw `IllegalStateException` until another `next`/`previous`. `listIterator(size() - 1)` is not “start at the end” for a `previous()`-only reverse.

> [!tip] Interview answer
> **`ListIterator` extends `Iterator` and exists only for `List`.** Iterator is forward plus optional `remove`. ListIterator adds backward walk, indexes, `set`, and `add`, with the cursor between elements. For a `Set` or `Queue` you get `Iterator`, not `ListIterator`.
