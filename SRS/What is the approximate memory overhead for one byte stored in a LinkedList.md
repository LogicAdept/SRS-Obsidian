<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #Java/Language/Wrappers/Autoboxing/Cache #Java/Language/Primitives #SRS

# What is the approximate memory overhead for one byte stored in a LinkedList?

> [!abstract] Short answer
> **About one `Node` per value — commonly ~24 bytes on 64-bit HotSpot with compressed oops — not a new `Byte` per row.** There is no `LinkedList<byte>`. Autoboxing uses `Byte.valueOf`, which caches **all** 256 `byte`s, so extra list memory is `prev` / `item` / `next` plus a header. The 1-byte payload sits in that shared wrapper. Versus a `byte[]`, overhead is tens of bytes per element, not 1.

## Node cost, not N wrappers

Generics store references. `add((byte) x)` boxes to `Byte`. `Byte.valueOf` caches every `byte` (`ByteCache` length 256). A normal insert therefore allocates **one `Node`** (`item`, `prev`, `next`) and points `item` at the cache. `new Byte(b)` (deprecated) is the path that adds a private wrapper per element [[How much extra memory does LinkedList add allocate per insertion]].

64-bit HotSpot: headers 12 bytes (compressed class pointers) or 16 without; compressed oops are 32-bit. Default node: 12 + 3×4 = **24 bytes** (8-aligned). Uncompressed refs + 16-byte header: **40 bytes**. Compact headers shrink the header term. A 32-bit VM is typically an 8-byte header plus three 4-byte refs (20, often padded to 24). Do not treat 24 as a language constant.

**Overhead** versus storing one primitive `byte` (8 bits, `Byte.SIZE`): you pay the node every time, plus the global cache (256 `Byte`s + the cache array) amortized across the JVM — not 16–24 extra wrapper bytes on every row. A `byte[]` of length N is about N payload bytes plus the array header. `ArrayList<Byte>` pays an array slot per element, still not two neighbor pointers [[What is the approximate memory overhead for one byte stored in an ArrayList]].

```d2
direction: right
payload: "1-byte value" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
box: "Byte cache\n(256 entries)" {
  width: 170
  height: 80
  style.fill: "#fff3e0"
}
node: "Node ~24 B\n3 oops + header" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}

payload -> box: "valueOf"
box -> node: "item ref"
```

**Fig. 1.** Useful data is 1 byte. Per-row overhead is the node. The `Byte` is shared for autoboxed values.

```java
java.util.LinkedList<Byte> list = new java.util.LinkedList<>();
list.add((byte) 7);
list.add((byte) 7);
// two Nodes (~24 B each, compressed oops); same cached Byte
```

**Listing 1.** Two “bytes” in the list: two nodes, one cached `Byte`. `list.get(0) == list.get(1)` is cache identity.

```java
byte[] raw = new byte[] { 7, 7 }; // two payload bytes + array header — Conceptual scale
```

**Listing 2.** Conceptual: a primitive array is the 1-byte-per-element baseline the list is overhead against.

> [!warning] Do not add wrapper size onto every node
> Interview dumps that quote 40 or 64 bytes per `byte` count a `Byte` object **and** a node for each row, then mention the cache. For `valueOf` / autobox, per-element extra is the **node**. Quote 24 bytes only with compressed oops (and say so).

> [!warning] `LinkedList<Byte>` is the wrong structure for a byte buffer
> You cannot store primitive `byte` in a `LinkedList`. N nodes plus object headers dominate. Use `byte[]` or `ByteBuffer` when the payload is actually bytes [[Why prefer primitives over wrappers in hot loops in Java]].

> [!tip] Interview answer
> **Overhead is one doubly-linked `Node` per element — often about 24 bytes with compressed oops — because `byte` is boxed and `Byte.valueOf` caches every value.** You do not pay a new `Byte` per insert. Compared with a `byte[]`, that is tens of bytes of pointers and header for one byte of data. `ArrayList<Byte>` is a slot, not two links, but still not a primitive array.
