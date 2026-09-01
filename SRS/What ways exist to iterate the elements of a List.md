<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Collections/List #SRS

# What ways exist to iterate the elements of a List?

> [!abstract] Short answer
> **Sequence walks:** enhanced-`for` (JLS desugars to `Iterator`), explicit `iterator()`, bidirectional `listIterator()` / `listIterator(index)`, `forEach`, and `stream()` / `spliterator()`. **Index loops** (`get(i)`) are legal on `List` but `O(n²)` on `LinkedList`. Reverse: `ListIterator` from the end, or Java 21 `list.reversed()`. Prefer iterator-style over `get` unless you know `RandomAccess`.

## Iterator, indexes, and views

`List.iterator()` yields elements in proper sequence. An enhanced `for (E e : list)` requires an `Iterable` (or array); for a `List` it is that iterator [[What is the List interface in Java]] [[How do you iterate elements LinkedList in order not using get(index]]. `Iterator.remove` is the safe in-loop delete; structural `add`/`remove` on the list during iteration is fail-fast (`ConcurrentModificationException`) on the usual implementations.

`ListIterator` adds `previous` / `hasPrevious`, `nextIndex` / `previousIndex`, `set`, and `add`. `listIterator(i)` starts so `next()` returns the element at `i` [[Compare Iterator and ListIterator capabilities]] [[How do you iterate a List in reverse using ListIterator]]. Reverse without indexes: `listIterator(size())` then `previous`, `LinkedList.descendingIterator()`, or `reversed()` (a view; `Collections.reverse` mutates) [[How do you traverse a LinkedList in reverse without using get index]] [[How do you reverse a List in Java]].

Indexed `for` / `while` with `get(i)` is a `List` extra, not how `Collection` iterates. It is `O(1)` per `get` on `ArrayList` (`RandomAccess`) and `O(n)` per `get` on `LinkedList` — a full scan is quadratic [[What is the time complexity of random access by index in a LinkedList]]. A `while` + `get` is the same cost model as the index `for`, not a fifth iterator kind.

`Iterable.forEach` / `Iterator.forEachRemaining` apply a `Consumer` (no `remove` in the lambda unless you use the iterator). `stream()` is sequential encounter order; `parallelStream()` is not a simple left-to-right loop. Default `List.spliterator()` is `SIZED` and `ORDERED`; on `RandomAccess` it may call `get(int)`, otherwise it wraps `iterator()`.

```d2
direction: down
list: "List" {
  width: 80
  height: 40
}
it: "iterator()\nenhanced-for / forEach" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
li: "listIterator()\nbidirectional + set/add" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
idx: "get(i) loop\nRandomAccess only if cheap" {
  width: 240
  height: 70
  style.fill: "#ffe0b2"
}
rev: "reversed() / ListIterator from end" {
  width: 260
  height: 70
  style.fill: "#f3e5f5"
}

list -> it
list -> li
list -> idx
list -> rev
```

**Fig. 1.** Four families: forward iterator, `ListIterator`, index, reverse view/cursor.

```java
java.util.List<String> list = java.util.List.of("a", "b", "c");

for (String e : list) { /* e */ }                    // iterator

java.util.Iterator<String> it = list.iterator();
while (it.hasNext()) { String e = it.next(); }

java.util.ListIterator<String> li = list.listIterator();
while (li.hasNext()) { String e = li.next(); }

list.forEach(e -> { /* e */ });
```

**Listing 1.** Conceptual forward walks. `List.of` is still `Iterable`; mutators on the iterator throw `UnsupportedOperationException`.

```java
for (int i = 0; i < list.size(); i++) {
    String e = list.get(i); // ArrayList: fine; LinkedList: do not
}
```

**Listing 2.** Index loop. Same idea as `while (i < size) get(i++)`. Use it only when `get` is `O(1)`.

> [!warning] `get(i)` in a loop is not “just another `for`”
> On `LinkedList` it is `Θ(n²)`. Enhanced-`for` / `iterator` / `ListIterator` walk pointers once. Dump “`for` vs `while`” is the same indexed pattern twice.

> [!warning] Do not mutate the list inside enhanced-`for`
> Use `Iterator.remove`, `removeIf`, or iterate a snapshot. `ListIterator.set` / `add` are the in-place edits the extra iterator is for. `forEach` + `list.remove` is still concurrent modification.

> [!tip] Interview answer
> **Enhanced-`for` and `iterator()`; `ListIterator` when you need back/`set`/`add`; `get(i)` only for `RandomAccess`; `forEach`/`stream` for bulk.** Reverse with `ListIterator` from `size()` or `reversed()`. Never sell an index loop as the `LinkedList` answer.
