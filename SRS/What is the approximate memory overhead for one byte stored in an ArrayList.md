<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Language/Wrappers/Autoboxing/Cache #Java/Language/Primitives #SRS

# What is the approximate memory overhead for one `byte` stored in an `ArrayList`?

> [!abstract] Short answer
> You do **not** store a primitive `byte`. `ArrayList` holds **references** to `Byte` objects. Per element you pay (1) one slot in the backing `Object[]` and (2) a `Byte` wrapper — **not** `Byte.BYTES` (1). Java SE does not publish object-header sizes, so there is no portable “N extra bytes” figure. Use `byte[]` when the payload should be one byte.

## A pointer plus a wrapper, not one byte

```d2
direction: down
list: "ArrayList<Byte>\nObject[] slot" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
box: "Byte object\none byte field + JVM header" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

list -> box: "reference"
```

**Fig. 1.** `ArrayList` is a resizable `Object[]` ([[What backing data structure does ArrayList use internally]]). A language `byte[]` stores the primitive directly ([[What is the difference between an array and an ArrayList]]).

`Byte` “wraps a value of primitive type `byte` in an object” with a **single `byte` field**. `Byte.BYTES` / `SIZE` describe that **primitive** encoding (1 byte / 8 bits), not the heap object. Autoboxing `list.add((byte) 1)` is a boxing conversion to `Byte` ([[How does adding an int to an ArrayList of Integer autobox]]).

`Byte.valueOf(byte)` caches **all** 256 `byte` values and is preferred to the deprecated `Byte(byte)` constructor for space and time. So distinct list slots can share one cached `Byte`. You still have **one reference per `size()`** (and unused **capacity** slots). Spare capacity is extra pointers, not extra `Byte`s.

```java
List<Byte> boxed = new ArrayList<>();
boxed.add((byte) 1); // autobox → cached Byte, plus one Object[] slot

byte[] raw = { 1 };   // one primitive byte in the array payload
```

**Listing 1.** Same numeric value; different layouts. Hot loops with wrappers: [[Why prefer primitives over wrappers in hot loops in Java]].

> [!warning] There is no JavaDoc “overhead = 24 bytes”
> Dumps that quote 16/20/24/40 bytes are describing a **particular JVM** (headers, compressed oops, alignment). The `ArrayList` spec does not state a byte tax. Answer with **reference + `Byte`**, then `byte[]` if you need density.

> [!warning] Cached identity is not zero cost
> Sharing `Byte.valueOf` avoids a **new** wrapper per `add`, not the array slot. `new Byte(b)` (deprecated) allocates a fresh object every time. Unused `ensureCapacity` still wastes references.

> [!tip] Interview answer
> **`ArrayList<Byte>` stores boxed `Byte`s, not `byte`s: each element is a heap object plus an `Object[]` pointer.** `valueOf` caches every `byte`, so the wrapper is often shared; the list still has one reference per index. For ~1 byte per value, use `byte[]`.
