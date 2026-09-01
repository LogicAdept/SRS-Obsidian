<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/List/LinkedList #SRS

# What is the difference between `ArrayList` and `LinkedList`?

> [!abstract] Short answer
> `ArrayList` is a **resizable `Object[]` `List`**: O(1) `get`/`set`, amortized O(1) end `add`, linear middle insert/delete. `LinkedList` is a **doubly-linked `List` and `Deque`**: index ops walk from the nearer end; `addFirst`/`addLast` splice in O(1). Both allow `null` and are unsynchronized. Default `List` is `ArrayList`.

## Array vs nodes

```d2
direction: right
al: "ArrayList\nObject[] + size\nget(i) O(1)" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
ll: "LinkedList\nnodes + Deque ends\nget(i) walks" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Same `List` methods; different machines ([[What is an ArrayList]], [[What backing data structure does ArrayList use internally]]).

| Call | `ArrayList` | `LinkedList` |
| --- | --- | --- |
| `get`/`set(i)` | constant time | traverse from nearer end |
| `add(e)` (end) | amortized O(1) | `addLast`, expected O(1) |
| `addFirst` / `removeFirst` | O(n) shift (`add(0, e)`) | O(1) splice |
| `add(size()/2, e)` | O(n) `arraycopy` | O(n) walk + O(1) splice |

`ArrayList` says linear work has a **lower constant factor** than `LinkedList`. Indexed middle insert is **not** O(1) on `LinkedList` ([[How would you explain for ArrayList or for LinkedList element in list.add(list.size 2 newElement]]). `ListIterator.add` after you already hold a `LinkedList` cursor is the O(1) insert dumps remember.

Both: all optional list ops, fail-fast iterators, not synchronized. `Vector` is the synchronized array list ([[What is the difference between ArrayList Vector and CopyOnWriteArrayList]]). Which is faster for a workload: [[When is ArrayList faster than LinkedList and when is it slower]].

```java
List<String> a = new ArrayList<>();
a.add("x");
a.get(0);

LinkedList<String> d = new LinkedList<>();
d.addLast("x");
d.addFirst("y"); // Deque end, not ArrayList's cheap path
```

**Listing 1.** End/`get` vs front insert.

> [!warning] “`LinkedList` insert is O(1)” without a node in hand
> `add(i, e)` must **find** index `i` first. That walk is Θ(min(i, n−i)). Do not pick `LinkedList` “for middle inserts” by index.

> [!warning] `LinkedList` as a queue is not the fastest `Deque`
> `ArrayDeque` is “likely to be faster than `LinkedList` when used as a queue” (and vs `Stack` as a stack). It forbids `null`. `LinkedList` still implements `List`; `ArrayDeque` does not.

> [!tip] Interview answer
> **`ArrayList` is a growable array: O(1) index, amortized append, O(n) middle shift.** `LinkedList` is a doubly-linked `Deque`: O(1) at the ends, O(n) `get(i)`. Use `ArrayList` unless you live on the two ends (and then consider `ArrayDeque` if you do not need `List`).
