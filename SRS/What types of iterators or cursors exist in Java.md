<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# What types of iterators or cursors exist in Java?

> [!abstract] Short answer
> **Four named cursor APIs:** `Enumeration` (Java 1.0), `Iterator` (1.2), `ListIterator` (1.2, a subinterface of `Iterator`), and `Spliterator` (1.8). `Iterator` is the general `Iterable` walk (`hasNext` / `next`, optional `remove`, forward only). `ListIterator` adds backward walk, `set`, and `add`, but only on `List`. `Enumeration` is the legacy read API (`hasMoreElements` / `nextElement`). `Spliterator` is a **different** type: split + characteristics for sequential or parallel traversal, not an `Iterator`.

## Four APIs, two inheritance lines

`Iterator` is obtained from `Iterable.iterator()` (every `Collection`). Forward only. `remove()` is optional — default throws `UnsupportedOperationException`. There is no type named “universal cursor” [[What is the Iterator interface and why do Java collections use it]], [[In which Java version was Iterator introduced]].

`ListIterator` **extends** `Iterator`. `List.listIterator()` / `listIterator(index)` only. Extra: `hasPrevious` / `previous`, `nextIndex` / `previousIndex`, `set`, `add`. Dump “most powerful” is sloppy: it is the richest **list** cursor, not a parallel engine [[Compare Iterator and ListIterator capabilities]].

`Enumeration` does **not** extend `Iterator`. Classic sources: `Vector.elements()`, `Hashtable.keys()` / `elements()`. No `remove`. `asIterator()` (Java 9) is an adapter whose `remove` throws UOE. Not fail-fast on those legacy methods [[What is the difference between Enumeration and Iterator in Java]], [[Is Enumeration fail-fast]].

`Spliterator` does **not** extend `Iterator`. `Collection.spliterator()` (and streams). `tryAdvance` / `forEachRemaining` for traversal, `trySplit` to partition work, `characteristics()` among `ORDERED`, `DISTINCT`, `SORTED`, `SIZED`, `NONNULL`, `IMMUTABLE`, `CONCURRENT`, `SUBSIZED`. Designed for efficient parallel decomposition and a single-method advance (no `hasNext`/`next` race). Primitive specializations: `Spliterator.OfInt` / `OfLong` / `OfDouble` [[What is Spliterator]].

`descendingIterator()` on a `Deque` still returns an `Iterator`. `PrimitiveIterator` is still an `Iterator`. Neither is a fifth interview “kind.”

```d2
direction: down
en: "Enumeration\n1.0  read names" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
it: "Iterator\n1.2  forward ± remove" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
li: "ListIterator\nextends Iterator\n± previous / set / add" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
sp: "Spliterator\n1.8  trySplit + bits" {
  width: 240
  height: 70
  style.fill: "#f3e5f5"
}

it -> li
```

**Fig. 1.** `ListIterator` is an `Iterator`. `Enumeration` and `Spliterator` are separate interfaces. Spelling is **Spliterator**, not “Spilterator.”

```java
class CursorTypes {
    static void obtain(java.util.List<String> list, java.util.Vector<String> vector) {
        java.util.Enumeration<String> e = vector.elements();
        java.util.Iterator<String> it = list.iterator();
        java.util.ListIterator<String> li = list.listIterator();
        java.util.Spliterator<String> sp = list.spliterator();
        e.hasMoreElements();
        it.hasNext();
        li.hasPrevious();
        sp.tryAdvance(s -> {});
    }
}
```

**Listing 1.** How you get each cursor. `for (E x : list)` uses `iterator()`, not `ListIterator` or `Spliterator`.

> [!warning] `Spliterator` is not a fourth `Iterator`
> It does not implement `hasNext`/`next`. Parallel streams use it internally. Calling it an “iterator” in the `Iterator` sense is the usual mix-up (and the usual misspelling).

> [!warning] “Universal” / “most powerful” are not API terms
> `Iterator` is not usable on a non-`Iterable` array without wrapping. `ListIterator` cannot walk a `HashSet`. `Spliterator` can split a `Collection` that has no `ListIterator` at all.

> [!tip] Interview answer
> **Name four: `Enumeration`, `Iterator`, `ListIterator`, `Spliterator`.** Iterator is forward plus optional remove; ListIterator is the List-only bidirectional cursor with set/add; Enumeration is the 1.0 read API; Spliterator (Java 8) splits and reports characteristics for parallel traversal — it is not an Iterator.
