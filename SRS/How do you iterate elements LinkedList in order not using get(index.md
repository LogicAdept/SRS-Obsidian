<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #Java/Collections/Iteration #SRS

# How do you iterate elements LinkedList in order not using get(index)?

> [!abstract] Short answer
> **Walk with `iterator()` / enhanced `for` / `listIterator()` — head to tail, one node at a time.** Do not write `for (int i = 0; i < list.size(); i++) list.get(i)`. On `LinkedList`, each `get(i)` starts a new walk from the nearer end, so an indexed scan is quadratic. `descendingIterator()` is the **reverse** walk, not list order.

## Proper sequence, not `get(i)`

`List.iterator()` returns elements **in proper sequence** (index 0 through `size() - 1`). Enhanced `for` over a `LinkedList` is that iterator: `Expression.iterator()`, then `hasNext` / `next`. `AbstractSequentialList.iterator()` is just `listIterator()`. `listIterator()` / `listIterator(index)` is the same forward walk plus `previous`, `set`, `add`, and indexes [[Compare Iterator and ListIterator capabilities]] [[How do you iterate the elements of a Java collection]].

`LinkedList` is a doubly-linked `List` (and `Deque`). Index operations traverse from the beginning or the end, whichever is closer. OpenJDK `get(i)` is `node(index).item`: if `i < size/2` it follows `next` from `first`, otherwise `prev` from `last`. `ListItr.next()` does `next = next.next` — O(1) per element after the iterator exists. `List.iterator()` in a loop is therefore linear; repeating `get(i)` is not.

`List` itself says iterating is typically preferable to indexing when the caller does not know the implementation, and names `LinkedList` as the example whose positional access costs time proportional to the index.

```d2
direction: right
bad: "for i: get(i)" {
  width: 180
  height: 80
  style.fill: "#fff3e0"
}
walk: "restart from an end\neach call" {
  width: 200
  height: 80
  style.fill: "#ffebee"
}
good: "iterator() / for-each" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
step: "follow node.next\nonce per element" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}

bad -> walk
good -> step
```

**Fig. 1.** Indexed `get` restarts a link walk. An iterator holds the current node and steps once.

```java
class LinkedListInOrder {
    static void printForward(java.util.LinkedList<String> list) {
        for (String s : list) {          // Iterable → iterator()
            System.out.print(s);
        }
        java.util.Iterator<String> it = list.iterator();
        while (it.hasNext()) {
            System.out.print(it.next());
        }
        java.util.ListIterator<String> li = list.listIterator();
        while (li.hasNext()) {
            System.out.print(li.next());
        }
    }
}
```

**Listing 1.** Three equivalent **in-order** walks. For `["a","b","c"]` each prints `abc`. Keep an explicit `Iterator` / `ListIterator` when you need `remove` (or `set` / `add` on `ListIterator`).

```java
// Anti-pattern — n calls to get(i), each a fresh link walk
for (int i = 0; i < list.size(); i++) {
    list.get(i);
}
```

**Listing 2.** Conceptual quadratic scan. Same visible order as Listing 1, wrong cost.

Reverse is a different cue: `listIterator(list.size())` then `previous()`, or `descendingIterator()` (tail → head, since 1.6), or Java 21 `list.reversed()` in a for-each [[How do you iterate a List in reverse using ListIterator]] [[How can you iterate a Deque in both directions]]. `descendingIterator()` is an `Iterator`, not `Iterable` — it is not a for-each source.

`iterator` and `listIterator` are fail-fast: structural change except that iterator’s own `remove` / `add` throws `ConcurrentModificationException` (best-effort) [[What is ConcurrentModificationException]].

> [!warning] `get(i)` in a counted loop is the slow “in order” walk
> It is still proper sequence, just not a sequential iterator. `size()` in the loop header is cheap; `get(i)` is not. `indexOf` / `lastIndexOf` are also documented in terms of `get(i)`-style scans.

> [!warning] `descendingIterator()` is reverse order
> It is not how you iterate **in** list order. Forward: enhanced `for` / `iterator()` / `listIterator()`. Reverse: `previous()` from `size()`, `descendingIterator()`, or `reversed()`.

> [!tip] Interview answer
> **Use the iterator — enhanced `for` or `listIterator()` — not `get(index)` in a for-i loop.** `LinkedList.get(i)` walks from the nearer end every time, so indexing the whole list is quadratic. The iterator follows `next` pointers once per element. `descendingIterator()` is the reverse direction, not this question.
