<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# What is the access time to the last element of an `ArrayList`?

> [!abstract] Short answer
> **Constant time.** `get` is specified as O(1); the last slot is just `get(size() - 1)` (or `getLast()` since Java 21). There is no walk from index 0. Empty list: `IndexOutOfBoundsException` / `NoSuchElementException`, not a linear scan.

## Last index is still random access

```d2
direction: right
idx: "size() - 1" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
slot: "elementData[size-1]\nO(1)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

idx -> slot
```

**Fig. 1.** Capacity may be larger than `size()`; the last **element** is at `size - 1`, not `elementData.length - 1` ([[What backing data structure does ArrayList use internally]]).

The class javadoc: `get` (with `set`, `size`, `isEmpty`, iterators) “run in constant time.” OpenJDK `get` is `Objects.checkIndex` then `elementData(index)`. `getLast()` (Java 21) uses `elementData(size - 1)` and throws `NoSuchElementException` if `size == 0`.

```java
List<String> list = new ArrayList<>();
list.add("a");
list.add("b");
list.add("c");
list.get(list.size() - 1); // "c" — O(1)
list.getLast();             // Java 21, same slot
```

**Listing 1.** Same cost as `get(0)`. End **`add`** is amortized O(1), a different method ([[Does ArrayList always add elements in O(1) time]]). Overview: [[What is an ArrayList]].

`LinkedList` also reaches the last node in O(1) (`getLast` / nearer-end walk). The ArrayList-vs-`LinkedList` gap is **middle** `get(i)`, not the last element ([[When is ArrayList faster than LinkedList and when is it slower]]).

> [!warning] Last element ≠ last capacity slot
> After `remove`s, spare `null`s may sit past `size`. Reading `elementData[length-1]` (not public) is not `getLast()`. Use `size() - 1`.

> [!warning] Empty list is not O(1) “null”
> `get(-1)` / `get(0)` on empty throws `IndexOutOfBoundsException`. `getLast()` throws `NoSuchElementException`. Do not write a loop to “find” the last element.

> [!tip] Interview answer
> **O(1) — `get(size() - 1)` or `getLast()`.** `ArrayList` is an array of references; the last live index is arithmetic, not a traversal. Don’t confuse that with O(n) `contains` or middle `add`.
