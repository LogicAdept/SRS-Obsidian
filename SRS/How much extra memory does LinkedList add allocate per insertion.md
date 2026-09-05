<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #Java/JVM/Memory/Heap #SRS

# How much extra memory does LinkedList add allocate per insertion?

> [!abstract] Short answer
> **One `Node` object: the element reference plus `prev` and `next`.** `add` is `linkLast` → `new Node<>(last, e, null)`. That is three fields on a new heap object, **not** a new copy of `e`. On 64-bit HotSpot the node’s own size is header plus those three oops (commonly **24 bytes** with compressed class pointers and compressed oops: 12-byte header + three 4-byte refs). Exact bytes follow JVM flags; compact 8-byte headers shrink it.

## One node per successful insert

`LinkedList` is a doubly-linked `List` / `Deque`. OpenJDK stores each slot as a private static `Node`: `item`, `next`, `prev`. `add(e)` / `addLast` call `linkLast`: allocate that node, hang it off `last`, bump `size` and `modCount`. `addFirst`, `add(index, e)`, and `offer*` take the same `new Node` path (`linkBefore` / `linkLast`). There is no spare-capacity array: **every insert allocates**, including `null` (which is a legal `item`).

The payload object is whatever the caller already had. `add` does not allocate a `String` or box an `int` — boxing is the caller’s. Extra memory **of the list** is the node (and later GC of that node on remove).

64-bit HotSpot object headers are **96 bits (12 bytes)** with compressed class pointers, or **128 bits (16 bytes)** without. Compact object headers cut that to **64 bits** when enabled. Compressed oops are `uint32_t` narrow pointers (32 bits) when `UseCompressedOops` is on; otherwise each of `item` / `next` / `prev` is a full address. Objects are aligned; a 12+12 layout is already 8-byte aligned at **24 bytes** per node. Wide oops + 16-byte header is **40 bytes** before considering alignment of other shapes.

`ArrayList.add` usually writes one array slot; extra heap shows up on **resize**, not per element [[How much extra memory can ArrayList add trigger when resizing]] [[What backing data structure does ArrayList use internally]]. Autoboxed `byte` still costs one node, not a new `Byte` per row [[What is the approximate memory overhead for one byte stored in a LinkedList]].

```d2
direction: right
add: "add(e) / linkLast" {
  width: 180
  height: 80
  style.fill: "#fff3e0"
}
node: "new Node\nitem · prev · next" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
heap: "header + 3 oops\n(+ padding)" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}

add -> node
node -> heap
```

**Fig. 1.** Each insertion allocates a node that points at `e` and at its two neighbors. `e` itself is not copied.

```java
// OpenJDK shape (fields only) — Conceptual
final class NodeShape<E> {
    E item;
    NodeShape<E> next;
    NodeShape<E> prev;
}
```

**Listing 1.** Three references per node. `add` always `new`s this; it does not grow a backing array.

```java
java.util.LinkedList<String> list = new java.util.LinkedList<>();
String s = "x";
list.add(s); // one Node; s is not cloned
list.add(null); // still one Node, item == null
```

**Listing 2.** Two inserts → two nodes. The string object existed before `add`.

> [!warning] Do not quote one magic number without the JVM
> “24 bytes” is the common **compressed-oops + compressed-klass** 64-bit layout, not a JLS constant. Disable compressed oops or class pointers, or enable compact headers, and the node size changes. Counting `3 × 8` and stopping **drops the header**. Counting the `String` / boxed `Integer` **double-counts** the payload.

> [!warning] `add` always allocates; `ArrayList.add` often does not
> There is no `ensureCapacity` on `LinkedList`. A million `add`s are a million nodes and a million object headers. That is why a `LinkedList` of boxed bytes is far heavier than an `ArrayList` of the same length, and why `get(i)` is the wrong way to walk it [[Does LinkedList implement Queue and Deque in Java]]. `add(index, e)` still allocates **one** `Node`; the extra cost is the O(n) walk to the slot, not a second object.

> [!tip] Interview answer
> **Each `add` allocates one doubly-linked `Node`: `item`, `prev`, `next` — three references plus an object header.** The element object is not allocated by `add`. On typical 64-bit HotSpot with compressed oops that node is 24 bytes; say “header plus three pointers, JVM-dependent,” not a single universal constant. `ArrayList` pays per-element as an array slot and only allocates extra on resize.
