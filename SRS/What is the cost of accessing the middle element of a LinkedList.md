<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #SRS

# What is the cost of accessing the middle element of a LinkedList?

> [!abstract] Short answer
> **Θ(n) — about n/2 link hops.** `get(i)` walks from the nearer end. For `i ≈ size/2` both ends are equally far, so the middle is the **slowest** index, not the last. `getFirst` / `getLast` are O(1). `ArrayList.get` of the middle is O(1).

## Nearer end makes the middle the worst `get`

`LinkedList` is doubly linked. Indexed operations “traverse the list from the beginning or the end, whichever is closer to the specified index.” OpenJDK `get(index)` is `node(index).item`. `node` uses `index < (size >> 1)`: from `first` via `next`, otherwise from `last` via `prev` [[Is Java LinkedList a singly or doubly linked list]].

Let n = `size`. Steps are min(i, n−1−i) (plus a cheap branch). That minimum is **largest** at the middle: ~n/2 hops, Θ(n). The last index is 0 hops from `last`. “Access the end” and “access the middle” are not the same cost.

`List` already warns that positional access may take time proportional to the index on `LinkedList`, and that iterating is typically better than indexing when the implementation is unknown. Walking every index with `get(i)` is Θ(n²). Hold a `ListIterator` (or `descendingIterator`) if you need a mid-list cursor [[How do you iterate elements LinkedList in order not using get(index]] [[What is the difference between ArrayList and LinkedList]].

`contains` is a different linear scan from `first` (via `indexOf`), not nearer-end `get`.

```d2
direction: right
head: "first" {
  width: 90
  height: 55
  style.fill: "#e8f5e9"
}
mid: "i ≈ n/2\n~n/2 hops" {
  width: 130
  height: 70
  style.fill: "#fff3e0"
}
tail: "last\nO(1)" {
  width: 90
  height: 55
  style.fill: "#e8f5e9"
}

head -> mid: next…
mid -> tail: …next
tail -> mid: prev…
```

**Fig. 1.** Nearer-end `get`: ends are cheap; the middle is ~n/2 pointer follows.

```java
java.util.LinkedList<String> list = new java.util.LinkedList<>();
// n elements …
String mid = list.get(list.size() / 2); // Θ(n) walk from an end
String last = list.getLast();           // O(1) tail pointer
```

**Listing 1.** Middle `get` vs `getLast`. For even n, `size()/2` uses the from-`last` branch (`index < size/2` is false when equal).

```java
for (int i = 0; i < list.size(); i++) {
    list.get(i); // Conceptual: Θ(n²) — each get restarts
}
```

**Listing 2.** Conceptual anti-pattern. An iterator follows `next` once per element.

> [!warning] Last is not the worst index
> After the nearer-end optimization, `get(n-1)` is O(1) and `get(n/2)` is Θ(n). Interview answers that say “`get` is O(n) so the last element is slowest” describe a **singly**-linked list that can only walk from the head.

> [!warning] `get(size()/2)` is not “O(1) because it is one call”
> One call still follows Θ(n) nodes. `ListIterator` to the middle is also Θ(n) **once**; afterwards `next`/`previous`/`add` at that cursor are cheap. There is no array address for the midpoint.

> [!tip] Interview answer
> **Middle access is Θ(n): `get` walks from the closer end, and the middle is equally far from both.** That is the worst `get`, not `getLast`. Use an iterator to traverse; use `ArrayList` if you need O(1) indexes.
