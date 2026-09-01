<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Arrays #SRS

# What backing data structure does `ArrayList` use internally?

> [!abstract] Short answer
> A **resizable object array**. The JavaDoc calls `ArrayList` a “resizable-array implementation of `List`” and exposes operations on “the array that is used internally.” OpenJDK stores that buffer as `transient Object[] elementData`; **`size` is a separate count**, not `elementData.length`.

## `Object[]` plus a logical `size`

```d2
direction: right
list: "ArrayList\nsize = 3" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
buf: "elementData Object[]\n[a, b, c, null, …]\ncapacity = length" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}

list -> buf: "private buffer"
```

**Fig. 1.** The list is not a linked structure. Slots are contiguous references; unused capacity is just extra `null`s after `size` ([[What is the difference between an array and an ArrayList]]).

That array’s `length` is **capacity**. It is always ≥ `size()`. `add` may replace `elementData` with a larger copy ([[How does resize ArrayList]]); `remove` slides elements left and does not shrink the array unless you `trimToSize()` ([[How does removing elements from an ArrayList work and how does size change]]). The language array still has a fixed `length` after each allocation; “grow” means a **new** `Object[]`.

OpenJDK’s no-arg constructor does not allocate ten slots immediately: it shares `DEFAULTCAPACITY_EMPTY_ELEMENTDATA` and inflates to `DEFAULT_CAPACITY` (10) on the first `add`. `new ArrayList<>(n)` (`n > 0`) allocates `new Object[n]`. Elements are **references** (`null` allowed); a primitive `int` is stored as `Integer`.

```java
ArrayList<String> list = new ArrayList<>(4);
list.add("a");
list.add("b");
// conceptual: elementData length 4, size() == 2
```

**Listing 1.** Capacity vs `size()`. There is no public `capacity()` on `ArrayList` (unlike `Vector`).

> [!warning] `size()` is not the array length
> After `remove` or `clear`, the `Object[]` can stay large. Assuming the backing structure “became smaller” confuses logical size with capacity.

> [!warning] Not a linked list and not `int[]`
> `LinkedList` uses nodes. `ArrayList` is an `Object[]` of boxes. `ArrayList<Integer>` does not store a primitive `int[]`.

> [!tip] Interview answer
> **An `Object[]` (`elementData`) plus a `size` field.** Capacity is that array’s `length`. Growth allocates a new array and copies; it does not stretch the old one. That is why `get` is O(1) and middle `add`/`remove` copy a slice.
