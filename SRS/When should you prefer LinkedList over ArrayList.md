<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/List/LinkedList #SRS

# When should you prefer `LinkedList` over `ArrayList`?

> [!abstract] Short answer
> Prefer `LinkedList` when the hot path is the **two Deque ends** (`addFirst` / `removeFirst` / `removeLast`) **or** you already hold a `ListIterator` for a local splice **and** you still need a `List`. That is a narrow case. Default `List` is `ArrayList`. A queue that is not a `List` should be `ArrayDeque`, not `LinkedList`.

## Ends and a cursor, not “lots of inserts”

```d2
direction: down
need: "Need LinkedList?" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
ends: "Deque ends + List API" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
cur: "ListIterator already at the hole" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
no: "Otherwise ArrayList\n(or ArrayDeque if not a List)" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}

need -> ends
need -> cur
need -> no
```

**Fig. 1.** `LinkedList` is a doubly-linked `List` **and** `Deque`. `ArrayList` is not a `Deque` ([[What is the difference between ArrayList and LinkedList]]).

`ArrayList.add(0, e)` / `remove(0)` shift the whole array. `LinkedList.addFirst` / `removeFirst` splice in expected O(1). If you need **both** `List` (`get`, `listIterator`, `subList`) and those end ops, `LinkedList` is the JDK type that is both.

A `ListIterator` on `LinkedList` can `add`/`remove` at the cursor without an indexed walk. `add(i, e)` on `LinkedList` still **finds** `i` first (from the nearer end) — that is not a reason to prefer it ([[When is ArrayList faster than LinkedList and when is it slower]], [[How would you explain for ArrayList or for LinkedList element in list.add(list.size 2 newElement]]).

Do **not** prefer `LinkedList` for random `get(i)`, for-each, or “frequent insert in the middle” by index. `ArrayList` documents a **lower constant factor** on linear work. Extra memory on `LinkedList` is per-node prev/next, not unused `elementData` slots ([[What backing data structure does ArrayList use internally]]). For a queue/stack that does not need `List`, `ArrayDeque` is “likely to be faster than `LinkedList` when used as a queue.”

| Need | Prefer |
| --- | --- |
| Random `get(i)`, iteration, append | `ArrayList` |
| Front insert/delete, or `Deque` + `List` | `LinkedList` |
| Middle insert **by index** | still `ArrayList` |
| Queue / stack, not a `List` | `ArrayDeque` (no `null`) |

“Guaranteed add time” is not an API guarantee. `ArrayList.add` can copy the whole array on grow. `LinkedList.addLast` allocates one node and does not recopy the list. That still does not beat `ArrayList` for a normal append-heavy `List`.

```java
LinkedList<String> q = new LinkedList<>();
q.addFirst("head");
q.removeLast();

ListIterator<String> it = q.listIterator();
it.next();
it.add("splice"); // O(1) at the cursor, not add(i)
```

**Listing 1.** The two cases that actually beat `ArrayList`.

> [!warning] Preferring `LinkedList` “for O(1) insert” without a node is the wrong interview
> Indexed middle insert is Θ(n) on both. `ArrayList` is usually faster there.

> [!warning] `LinkedList` is not the default queue
> `ArrayDeque` forbids `null` and is not a `List`. Keep `LinkedList` when you truly need `List` + Deque ends.

> [!tip] Interview answer
> **Prefer `LinkedList` only for Deque-end mutations or iterator-local splice while still needing `List`.** Otherwise `ArrayList`. For a queue that is not a `List`, use `ArrayDeque`.
