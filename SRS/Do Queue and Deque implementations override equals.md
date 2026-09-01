<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/HashCodeEquals/Contract #SRS

# Do `Queue` and `Deque` implementations override `equals`?

> [!abstract] Short answer
> **Generally no.** The `Queue` and `Deque` contracts say implementations **usually inherit** identity-based `equals` / `hashCode` from `Object`, because element-based equality is not always well-defined across queues with the same elements but different ordering policies. Contrast with `List` / `Set`, which **mandate** content equality.

## What the interfaces say

```d2
direction: right
list: "List / Set\ncontent equals\nrequired" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
queue: "Queue / Deque\nidentity equals\n(generally)" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Framework split: ordered lists and sets compare by value; dedicated queues typically compare by reference.

Java SE 21 `Queue`: implementations generally do **not** define element-based `equals` / `hashCode`; they inherit `Object`’s identity versions, because element-based equality is not always well-defined for queues with the same elements but **different ordering properties** (FIFO vs priority vs LIFO). `Deque` repeats the same guidance.

`Collection` notes that `List` and `Set` mandate value comparison; a plain `Collection` (or types that are not `List`/`Set`) may keep reference equality. That is the same design story as [[How would you explain the equals and hashCode contract together in Java]] — when you *do* override `equals`, `hashCode` must follow; queues usually skip both.

```java
Queue<String> a = new ArrayDeque<>();
Queue<String> b = new ArrayDeque<>();
a.offer("x");
b.offer("x");
System.out.println(a.equals(b)); // false — distinct instances
System.out.println(a == b);      // false
```

**Listing 1.** Typical `ArrayDeque` / `PriorityQueue` behavior: same sequence, different objects → not equal.

## Exception: also a `List`

`LinkedList` implements `List` **and** `Deque` / `Queue`. As a `List`, it uses **content** `equals` / `hashCode` (same size, pairwise equal elements in order). Two `LinkedList`s with the same elements in the same order **are** equal even though they are also queues.

```java
Deque<String> asList = new LinkedList<>();
Deque<String> asDeque = new ArrayDeque<>();
asList.addLast("x");
asDeque.addLast("x");
System.out.println(asList.equals(asDeque)); // false (types / contracts differ)
System.out.println(
    new LinkedList<>(List.of("x")).equals(new LinkedList<>(List.of("x")))
); // true — List equals
```

**Listing 2.** Do not assume every `Deque` reference uses identity equality — check the concrete type (or the `List` role).

> [!warning] Same elements ≠ equal queues
> For `ArrayDeque`, `PriorityQueue`, and most concurrent queues, equal contents do **not** make `equals` true. Compare with a `List` copy or iterate if you need content equality.

> [!warning] `contains` still uses element `equals`
> Skipping collection-level `equals` does **not** mean elements are compared by `==`. Methods like `contains` / `remove(Object)` still use `Objects.equals` on elements.

> [!tip] Interview answer
> **`Queue`/`Deque` implementations generally do not override `equals`/`hashCode`** — they keep `Object` identity equality, because ordering policies differ. **`List`/`Set` do define content equality.** Exception: `LinkedList` is a `List`, so it *does* use sequence-based `equals` even when used as a deque.
