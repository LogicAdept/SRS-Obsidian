<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# Why does `ArrayList` store `size` separately from `elementData.length`?

> [!abstract] Short answer
> **`elementData.length` is capacity; `size` is how many elements are in the list.** A Java array’s `length` is fixed for that allocation. Spare slots after `size` make amortized O(1) `add` possible. `size()` is O(1) because it is stored, not scanned.

## Capacity vs live count

```d2
direction: right
sz: "size = 3\nlive elements" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
cap: "elementData.length = 6\ncapacity" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}

sz -> cap: "size <= length"
```

**Fig. 1.** Same buffer; two numbers ([[What backing data structure does ArrayList use internally]]).

`ArrayList` is a resizable-array `List`. The language array cannot change `length`; “grow” allocates a **new** `Object[]` and copies ([[How does resize ArrayList]]). Until that copy, extra slots sit after the last live element (typically `null`). If `size` were `elementData.length`, those slots would count as elements and you could not keep unused capacity.

`add` stores at `elementData[size]` and increments `size` when `size < length`. When `size == length`, grow first. `remove` decrements `size` and shifts left; **length does not drop** ([[How does removing elements from an ArrayList work and how does size change]]). `trimToSize()` is the documented way to set capacity down to `size`.

Dump “capacity is always greater than `size`” is **false when the list is full** (`size == length`) and for the empty default buffer (`length == 0`, `size == 0`). Capacity is always **≥** `size`. There is no public `capacity()` on `ArrayList` (unlike `Vector`).

```java
ArrayList<String> list = new ArrayList<>(4);
list.add("a");
list.add("b");
// conceptual: length 4, size() == 2 — length is not the list size
list.remove("a");
// still length 4, size() == 1
```

**Listing 1.** Conceptual OpenJDK fields. Spare capacity is why end `add` is amortized O(1) ([[Does ArrayList always add elements in O(1) time]]).

> [!warning] `list.size()` is not `elementData.length`
> Using the array length as the `List` size would treat leftover capacity as elements (or forbid leftover capacity). `size()` stays O(1) because the count is a field.

> [!warning] Empty `ArrayList()` is not ten slots yet
> OpenJDK shares a zero-length empty array until the first `add`, then inflates to default capacity 10. `size` is still 0 before that `add`.

> [!tip] Interview answer
> **`length` is the allocated capacity; `size` is the live element count.** They differ so the list can grow in chunks and shrink logically on `remove` without reallocating. `size <= capacity`; they are equal only when the buffer is full (or both empty).
