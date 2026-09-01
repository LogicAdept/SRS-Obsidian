<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Collections/List #SRS

# How do you iterate a `List` in reverse using `ListIterator`?

> [!abstract] Short answer
> **Place the cursor after the last element with `list.listIterator(list.size())`, then walk with `hasPrevious()` / `previous()`.** `ListIterator` is the `List`-only bidirectional iterator: no current element — the cursor sits *between* slots. `listIterator(size())` is legal (`index` may equal `size()`). `listIterator(size() - 1)` skips the last element if you only call `previous()`.

## Cursor after the last element

`List` supplies a `ListIterator` in addition to a plain `Iterator`: traverse either way, `set` / `add` / `remove` on the last element returned by `next` or `previous`, and read `nextIndex()` / `previousIndex()`. A list of length `n` has `n + 1` cursor positions (before the first element through after the last) [[Compare Iterator and ListIterator capabilities]].

`listIterator(int index)` starts at that cursor. `index` is the element an initial `next()` would return; an initial `previous()` returns the element at `index - 1`. Out of range is `index < 0 || index > size()` — so `listIterator(list.size())` starts **after** the last element: `next()` throws `NoSuchElementException`, `previous()` returns the last element and steps the cursor backward.

`listIterator()` with no argument starts at the beginning (`previous()` is immediately empty). Reverse walk must pass `size()`, not `0`.

`ListIterator` is not `Iterable`. You cannot write `for (E e : list.listIterator(...))`. For a reverse **for-each** since Java 21, use `for (E e : list.reversed())` — a reverse-ordered `List` view, not a `ListIterator` [[How can you iterate a Deque in both directions]].

`ArrayList` (and typical JRE lists) document fail-fast `listIterator`s: structural change except that iterator’s own `remove` / `add` generally throws `ConcurrentModificationException` (best-effort). `set` after `previous()` replaces the last returned element and is not a structural modification on `ArrayList` [[What is ConcurrentModificationException]].

```d2
direction: right
c0: "^" {
  width: 50
  height: 45
}
a: "a" {
  width: 70
  height: 45
  style.fill: "#e3f2fd"
}
c1: "^" {
  width: 50
  height: 45
}
b: "b" {
  width: 70
  height: 45
  style.fill: "#e3f2fd"
}
c2: "^" {
  width: 50
  height: 45
}
c: "c" {
  width: 70
  height: 45
  style.fill: "#e3f2fd"
}
end: "^  size()" {
  width: 110
  height: 45
  style.fill: "#fff3e0"
}

c0 -> a -> c1 -> b -> c2 -> c -> end
```

**Fig. 1.** Four cursor positions for three elements. Reverse iteration starts at the rightmost caret (`listIterator(3)`), then `previous()` yields `c`, `b`, `a`.

```java
class ReverseListWalk {
    static void printReversed(java.util.List<String> list) {
        java.util.ListIterator<String> it = list.listIterator(list.size());
        while (it.hasPrevious()) {
            System.out.print(it.previous());
        }
    }
}
```

**Listing 1.** For `["a", "b", "c"]` this prints `cba`. `it.previousIndex()` before the first `previous()` is `size() - 1`; after walking off the front it is `-1`.

```java
java.util.ListIterator<String> wrong = list.listIterator(list.size() - 1);
// previous() first returns "b", not "c" — last element only via next()
```

**Listing 2.** Conceptual start-index mistake. `size() - 1` is the last element’s index for `next()`, so a `previous()`-only loop never visits that last element.

> [!warning] `listIterator(size() - 1)` is not “start at the end”
> Reverse with `previous()` needs the cursor **after** the last element: `listIterator(size())`. Off-by-one here silently drops the last value. `listIterator(-1)` throws `IndexOutOfBoundsException`; `size()` does not.

> [!warning] `ListIterator` is not a for-each source
> It is an `Iterator`, not an `Iterable`. Enhanced `for` over the list is always head-to-tail. Java 21 `list.reversed()` is the reverse view if you want for-each rather than `previous()`.

> [!tip] Interview answer
> **Call `list.listIterator(list.size())` and loop `hasPrevious` / `previous()`.** The cursor sits between elements, so `size()` means “after the last,” which is legal. `size() - 1` is the wrong start if you only walk backward. `ListIterator` also gives `set` / `add` / indexes; it is not usable in a for-each.
