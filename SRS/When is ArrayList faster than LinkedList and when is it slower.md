<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/List/LinkedList #SRS

# When is `ArrayList` faster than `LinkedList`, and when is it slower?

> [!abstract] Short answer
> **`ArrayList` is faster for `get`/`set`, scans, and most indexed middle insert/delete.** `LinkedList` is faster at the **Deque ends** (`addFirst` / `removeFirst`) and for a splice when you already hold a `ListIterator`. Indexed `add(i)` is Θ(n) on both; `ArrayList` documents a **lower constant factor**. Default `List` is `ArrayList`.

## Faster by the call, not by the type name

```d2
direction: right
al: "ArrayList faster\nget/set, scan, add(i)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
ll: "LinkedList faster\naddFirst / removeFirst\ncursor splice" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Same `List` methods; the hot method decides ([[What is the difference between ArrayList and LinkedList]]).

`ArrayList`: `size`, `isEmpty`, `get`, `set`, `iterator`, `listIterator` run in **constant time**; end `add` is **amortized** constant (`n` adds are O(n)); **all other operations are linear**, “constant factor low compared to `LinkedList`.” That includes `add(int, E)`, `remove(int)`, `contains` ([[How do you search for an element in an ArrayList]], [[Does ArrayList always add elements in O(1) time]]).

`LinkedList` `get(i)` walks from the nearer end. `add` ≡ `addLast` (expected O(1) node splice, no array copy of all elements). `addFirst`/`removeFirst` are O(1) on `LinkedList` and O(n) shifts on `ArrayList`. Indexed midpoint insert walks then splices on `LinkedList` and `arraycopy`s on `ArrayList` — both Θ(n); the array copy usually wins ([[How would you explain for ArrayList or for LinkedList element in list.add(list.size 2 newElement]], [[What is the difference between ArrayList and LinkedList]]).

| Hot path | Usually faster |
| --- | --- |
| `get(i)` / `set(i)` / for-each | `ArrayList` |
| `add(e)` at the end | both cheap; `ArrayList` until a grow |
| `add(i, e)` / `remove(i)` by index | `ArrayList` (shift vs pointer chase) |
| `addFirst` / `removeFirst` | `LinkedList` |
| Queue, not a `List` | `ArrayDeque` (faster than `LinkedList` as a queue) |

When to choose which type: [[When should you prefer LinkedList over ArrayList]].

```java
List<String> byIndex = new ArrayList<>();
byIndex.get(0);           // ArrayList wins
byIndex.add(0, "head");    // ArrayList still often wins vs LinkedList.add(0, e)

LinkedList<String> ends = new LinkedList<>();
ends.addFirst("head");    // LinkedList wins
ends.removeLast();
```

**Listing 1.** Index/`add(0)` vs Deque ends.

> [!warning] Empty “it depends” is not an answer
> Name the method. Random access and scans → `ArrayList`. Queue/stack **ends** → `LinkedList` (or another `Deque`). Middle-by-index → usually still `ArrayList`. `ListIterator.add` on `LinkedList` after you already sit on a node is the O(1) insert people remember — not `list.add(i, e)`.

> [!warning] “`LinkedList` is faster in the middle” is usually false
> `add(size()/2, e)` must **find** the node first. That walk dominates the O(1) splice. Do not pick `LinkedList` for “lots of middle inserts” by index.

> [!warning] One grow does not make `LinkedList` the append default
> A full `ArrayList.add` copies the array (O(n) that call). *n* appends are still amortized O(n). Use `ensureCapacity` if the spike matters; do not switch to `LinkedList` only to avoid grow.

> [!tip] Interview answer
> **`ArrayList` wins on index, iteration, and typical middle `add(i)`.** `LinkedList` wins on `addFirst`/`removeFirst` and iterator-local splice. Both are linear at an unknown index; for a queue that is not a `List`, use `ArrayDeque`.
