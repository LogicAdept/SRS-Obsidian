<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# Why is there no `add` method on `Iterator`?

> [!abstract] Short answer
> **Because `Iterator` does not promise encounter order, so “insert here” has no single meaning.** `remove()` is well-defined: it deletes the last element `next()` returned. `add` would need a **cursor position in a sequence**. That exists on `ListIterator` (a `List` walk), not on a general `Iterator` over a `Set` or unordered `Collection`.

## Order is the missing contract

`Collection.iterator()` may return elements in **any** order unless that collection documents one. `HashSet` does not. An `Iterator.add(e)` could not mean “insert after the current element” without a stable sequence, and it could not mean the same thing as `Collection.add(e)` (membership / append-at-end / map-specific rules). So the collections design left `add` off `Iterator`.

`remove` does not need that sequence: it names **one already-returned element**. That is why `Iterator` added `remove` relative to `Enumeration`, and why `remove` stays optional (default: `UnsupportedOperationException`) [[What is the Iterator interface and why do Java collections use it]], [[How do you remove an element from a collection while iterating]].

`ListIterator` **does** have `add`. A `List` has proper sequence and `n+1` cursor slots between elements. `add` inserts immediately **before** what `next()` would return and **after** what `previous()` would return; the new element sits before the cursor (`next` unchanged, `previous` returns the new value) [[Compare Iterator and ListIterator capabilities]], [[How do you iterate a List in reverse using ListIterator]].

Dump lines that say “Iterator only enumerates” or “every collection already has `add` so Iterator.add is pointless” miss the point: `Collection.add` is a **collection** mutator with no iterator cursor, and Iterator’s job includes optional **in-walk remove**, not insert-at-cursor. Fail-fast / `modCount` is not why `add` is absent.

```d2
direction: down
it: "Iterator\nno order contract" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
rm: "remove()\nlast next() element" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
no: "no add()\ninsert position undefined" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
li: "ListIterator\nList sequence + cursor" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ad: "add() before next\nafter previous" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

it -> rm
it -> no
li -> ad
```

**Fig. 1.** `remove` names an element. `add` needs a gap in a sequence. Only `ListIterator` has that gap.

```java
class InsertAtCursor {
    static void viaListIterator(java.util.List<String> list) {
        java.util.ListIterator<String> it = list.listIterator();
        while (it.hasNext()) {
            if (it.next().isEmpty()) {
                it.add("(was empty)"); // ListIterator only — not Iterator
            }
        }
    }

    static void viaCollection(java.util.Collection<String> coll) {
        coll.add("anywhere-the-collection-allows");
    }
}
```

**Listing 1.** `it.add` does not compile on a plain `Iterator`. `coll.add` ignores the walk position (`HashSet` just accepts or rejects the element).

> [!warning] `ListIterator.add` is not `Iterator.add`
> Interview “there is no add on an iterator” means **`java.util.Iterator`**. The list cursor is a different interface [[What types of iterators or cursors exist in Java]].

> [!warning] `Collection.add` is not insert-at-iterator
> On a `List`, `add(e)` appends (or `add(index, e)` uses an index, not this iterator). On a `Set`, there is no “here.” Using `coll.add` inside a fail-fast for-each is still the CME story, not a missing `Iterator.add`.

> [!tip] Interview answer
> **`Iterator` has no `add` because it does not guarantee iteration order, so there is no well-defined insert position.** `remove` only needs the last `next()` element. For insert-at-cursor, use `ListIterator.add` on a `List`. `Collection.add` is a different operation.
