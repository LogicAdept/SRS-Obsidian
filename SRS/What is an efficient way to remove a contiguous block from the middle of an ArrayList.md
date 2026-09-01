<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# What is an efficient way to remove a contiguous block from the middle of an `ArrayList`?

> [!abstract] Short answer
> `list.subList(from, to).clear()`. That is the `List` javadoc’s range idiom. One suffix `arraycopy`, `size()` drops by `to - from`. Do **not** call `remove(i)` once per element in the hole.

## Range `clear` on a view

```d2
direction: down
before: "[a b | c d e | f g]\n          from    to" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
one: "arraycopy f,g onto c's slot\nsize -= 3" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

before -> one
```

**Fig. 1.** The tail after `to` slides left once. OpenJDK `removeRange` is `shiftTailOverGap` ([[How does removing elements from an ArrayList work and how does size change]]).

`subList(fromIndex, toIndex)` is a view of `[from, to)`. “This method eliminates the need for explicit range operations… `list.subList(from, to).clear()`.” `ArrayList.removeRange` (protected) shifts succeeding elements left and shortens the list by `toIndex - fromIndex`. Structural edits must go through that view, or the view’s contract is undefined.

```java
List<String> list = new ArrayList<>(
        Arrays.asList("a", "b", "c", "d", "e", "f"));
list.subList(2, 5).clear(); // drops c, d, e
// [a, b, f], size() == 3
```

**Listing 1.** Indexes are 0-based, `to` exclusive.

`n` times `remove(from)` (same index) is correct but copies the tail **n** times (quadratic in the remaining suffix). A loop that increments `i` while removing **skips** elements because later items slide into `i`. Last-element `remove` is cheap in OpenJDK, but `n` trailing `remove`s plus `trimToSize()` after a manual shift is still more work than one `removeRange` copy.

> [!warning] `removeRange` is `protected`
> Application code uses `subList(...).clear()`, not a public `removeRange`. Hand-copying with `set` then `n` last-element `remove`s plus `trimToSize()` is the same idea, clumsier.

> [!warning] `subList` is not a snapshot
> It is backed by the list. Clearing it **is** the efficient delete. Mutating the parent list another way while you hold the view is undefined. Do not 1-base indexes. Dump timings are not a spec.

> [!tip] Interview answer
> **`list.subList(from, to).clear()` — one tail shift.** Repeating `remove` in the middle is O(n) per call. Don’t increment the index as the hole closes.
