<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# What is the time complexity of random access by index in a LinkedList?

> [!abstract] Short answer
> **`O(n)`, not `O(1)`.** `get(i)` / `set(i)` (and other index ops) go through `node(index)`, which walks `next` from `first` or `prev` from `last`, whichever is nearer. Ends are `Θ(1)` hops; the **middle** is the worst index (`Θ(n)`). `LinkedList` is not `RandomAccess`.

## `get` is a walk, not an array slot

There is no backing array. `get(int index)` is `checkElementIndex` then `node(index).item`. `node` uses `index < (size >> 1)` to pick a direction: `i` steps from the head, or `n − 1 − i` from the tail. Cost is `Θ(min(i, n − 1 − i))`. Interview bound: **`O(n)`** [[What is the cost of accessing the middle element of a LinkedList]].

`set(i, e)` is the same walk, then a `Θ(1)` field write. `add(i, e)` / `remove(i)` pay that walk and then splice [[What is the time complexity of inserting into a LinkedList]]. `getFirst` / `getLast` skip `node` and are `Θ(1)`.

This is not value search: `contains` / `indexOf` always start at `first` and do not pick the nearer end [[What is the time complexity of finding an element in a LinkedList]]. `ArrayList.get(i)` is `O(1)` on an array; `LinkedList` is a sequential list [[What is an ArrayList]]. A `for (i = 0; i < n; i++) get(i)` loop is quadratic — iterate instead [[How do you iterate elements LinkedList in order not using get(index]].

The `List` spec already flags that some implementations take time proportional to the index (`LinkedList` is the example). `List.of` / `ArrayList` implement `RandomAccess`; `LinkedList` does not.

```d2
direction: right
first: "first" {
  width: 80
  height: 50
  style.fill: "#e8f5e9"
}
mid: "middle\nΘ(n)" {
  width: 100
  height: 60
  style.fill: "#ffcdd2"
}
last: "last" {
  width: 80
  height: 50
  style.fill: "#e8f5e9"
}

first -> mid -> last
```

**Fig. 1.** Nearer-end walk: ends are cheap; `get` of the middle node is the long path.

```java
java.util.LinkedList<Integer> list = new java.util.LinkedList<>();
list.add(10);
list.add(20);
list.add(30);
Integer x = list.get(1); // node(1) from first or last; O(n) in list size, not O(1)
```

**Listing 1.** Conceptual: `get(i)` follows pointers. Do not treat it like `ArrayList.get`.

> [!warning] “Doubly-linked” does not mean `O(1) get(i)`
> Two pointers per node only let the walk start from **either end**. Index `i` is still `O(n)` hops in the worst case. `get(0)` / `get(n-1)` being cheap does not make random access cheap.

> [!warning] Indexed loops are the classic quadratic bug
> `for (int i = 0; i < list.size(); i++) list.get(i)` is `Θ(n²)` on `LinkedList`. Use an iterator, enhanced-for, or `ListIterator`. `contains` is also `O(n)`, but it is a different walk (always from `first`).

> [!tip] Interview answer
> **`O(n)` random access.** `get(i)` → `node(i)` from the nearer end; middle is worst. Contrast `ArrayList` `O(1)` and end ops `getFirst` / `getLast` (`Θ(1)`). Prefer iterators over index loops. Not `RandomAccess`.
