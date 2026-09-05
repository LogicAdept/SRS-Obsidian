<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Language/Primitives #Java/JVM/Memory/Heap #SRS

# How much memory does an `Integer` object use compared with `int`?

> [!abstract] Short answer
> An `int` is **32 bits (4 bytes)** of value. An `Integer` is a **heap object**: HotSpot’s header (96 or 128 bits on 64-bit, or 64 bits with compact headers) plus a `private final int value`, then padding to the VM’s object alignment (8 bytes with compressed oops). That is commonly **16 bytes** of object on 64-bit HotSpot with compressed class pointers — **not** a language constant, and several times the primitive. The language does not specify object size.

## What the language fixes

`int` is a 32-bit two’s-complement integral type. `Integer.SIZE` is 32 and `Integer.BYTES` is `SIZE / Byte.SIZE` (**4**). Those constants describe the **primitive** representation, not the wrapper object. `Integer` “contains a single field whose type is `int`” — OpenJDK stores it as `private final int value`.

A variable of type `int` holds those 4 bytes. A variable of type `Integer` holds a **reference** (another 4 bytes with compressed oops, or 8 without) that points at a separate object.

```d2
direction: down
prim: "int field / local\n4 bytes of value" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
ref: "Integer variable\ncompressed oop 4 B or native 8 B" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
obj: "Integer instance\nheader 8–16 B + int 4 B + pad" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}

prim -> prim: "no object"
ref -> obj: "points at"
```

**Fig. 1.** Primitive storage versus reference-plus-header. Alignment and header width are HotSpot configuration, not JLS.

```java
int bits = Integer.SIZE;   // 32
int bytes = Integer.BYTES; // 4
```

**Listing 1.** Conceptual: portable sizes for the wrapped `int`, not for the `Integer` object.

## What HotSpot adds

On 64-bit HotSpot, every object has a header: a mark word (machine-word sized) plus a class word (32-bit compressed class pointer, or 64-bit uncompressed). JEP 450 states that layout occupies **96 bits (12 bytes)** or **128 bits (16 bytes)** depending on configuration. Compact object headers (experimental in JDK 24, product later) shrink the header to **64 bits**.

Heap objects are **8-byte aligned** when compressed oops are used, so sizes round up. A typical compressed-class-pointer `Integer` is 12-byte header + 4-byte `value` = **16 bytes**. Uncompressed class word is 16-byte header + 4-byte `value` = 20, then alignment to **24**. Compact headers: 8 + 4, then pad to **16**. Object sizes with compressed oops are meant to be comparable to 32-bit (ILP32) mode. Compressed oops themselves are on by default for heaps under about 32 GB.

That extra object is why wrappers cost allocation and GC compared with `int`, which is why [[Why prefer primitives over wrappers in hot loops in Java]] and [[What happens when you use Integer as a loop accumulator in Java]] exist. Small values still share cached instances (`Integer.valueOf` in **-128..127**), so not every boxing pays a new 16-byte object — see [[How can you extend the Integer autobox cache maximum]]. Escape analysis may even eliminate a short-lived `Integer` so it never hits the heap.

> [!warning] `Integer.BYTES` is not the object size
> `BYTES == 4` is the width of the primitive `int`. Interview answers that recite “`Integer` is 16 bytes” are describing a **common HotSpot shape**, not an API guarantee. Change compressed class pointers, compact headers, or alignment, and the instance size moves. Measure on the JVM you care about (heap dump / object-layout tooling).

> [!warning] Count the reference and the array case
> `Integer[]` stores pointers plus one object per element (unless cached). `int[]` stores packed 4-byte cells and no per-element header. A field of type `Integer` also costs the oop in the holder on top of the instance. Comparing “4 vs 16” without the pointer overstates how cheap the wrapper is in a graph of objects.

> [!tip] Interview answer
> **`int` is 4 bytes; `Integer` is a heap object with a VM header plus that 4-byte field, commonly 16 bytes on 64-bit HotSpot with compressed class pointers.** The language does not fix object size — headers are 12 or 16 bytes today, 8 with compact headers, then 8-byte alignment. Prefer `int` in hot loops; the cache and escape analysis only reduce how often you pay for a full object.
