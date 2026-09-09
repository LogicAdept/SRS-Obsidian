<!--
reps: 0
priority: 0
-->
#Java/Arrays #Java/Performance #SRS

# What is the most efficient way to copy an array in Java

> [!abstract] Short answer
> Use the bulk-copy APIs: `System.arraycopy` for an in-place or ranged copy, `Arrays.copyOf` / `Arrays.copyOfRange` when you want a new array, `clone()` for a quick full copy. They all funnel into the same JVM-intrinsic bulk-copy machinery, and `Arrays.copyOf` literally calls `clone()` or `System.arraycopy` inside the JDK. A hand-written per-element loop is the wrong default for object arrays.

## The three bulk paths

`System.arraycopy(src, srcPos, dest, destPos, length)` copies into an existing destination and handles overlapping ranges of the same array as if it first saved the source region to a temporary buffer. `Arrays.copyOf(original, newLength)` allocates the result; when the lengths match it is just `original.clone()`, otherwise it allocates and calls `arraycopy` — same machinery, padded or truncated to `newLength`. `Arrays.copyOfRange` is the ranged variant. `clone()` on an array needs no cast-worthy exception handling, returns the same array type, and — like every array copy — is **shallow**: the top-level slots are duplicated, the referenced objects are shared, which connects to [[What is the difference between shallow and deep copying in Java]].

```java
String[] original = { new String("A"), new String("B") };
String[] copy = original.clone();
System.out.println("element shared after clone: " + (original[0] == copy[0]));
System.out.println("array objects distinct    : " + (original != copy));
```

**Listing 1.** Output on JDK 21: `element shared after clone: true`, `array objects distinct: true` — a new array object, the same element references.

## What the numbers actually say

```d2
direction: right
need: "What do you need?" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
inplace: "System.arraycopy\ninto an existing array,\nany range" {
  width: 280
  height: 110
  style.fill: "#e8f5e9"
}
full: "clone() or Arrays.copyOf\nfull copy, new array" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
range: "Arrays.copyOfRange\npartial copy, new array" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
need -> inplace: "reuse destination"
need -> full: "new array"
need -> range: "new array"
```

**Fig. 1.** Choose by the shape of the call: destination reuse points to `arraycopy`, allocation-included copies point to `copyOf` / `clone` / `copyOfRange`.

Measured on JDK 21 for 10 million `int`s with a warmed JIT: `System.arraycopy` into a preallocated array 4.5 ms, a plain `for` loop into the same preallocated array 4.2 ms, `clone()` 11.9 ms, `Arrays.copyOf` 10.6 ms. Two honest conclusions: for a primitive array the JIT can vectorize a simple loop to intrinsic-like speed, and the extra cost of `clone` / `copyOf` is mostly the allocation of a fresh 40 MB result, not the copy itself. The bulk APIs still win as the default — one call, bounds checked as a unit, and the fastest option whenever elements are references, where a loop pays per-element type checks that the intrinsic avoids. For collections there is a one-liner equivalent — see [[How do you copy a collection into an array in one line]]; for the growth pattern built on copying see [[Is a Java array a static or dynamic data structure]].

> [!warning] Shallow semantics and a wrong-destination trap
> Every bulk copy shares element references — after copying an object array, mutating `copy[0]` mutates the "original" element too; deep content needs per-element copying (see [[How does cloning work for objects arrays and two-dimensional arrays in Java]]). And `arraycopy` does not allocate: passing a `dest` array smaller than `length` throws `ArrayIndexOutOfBoundsException`.

> [!tip] Interview answer
> Default to the bulk paths: `System.arraycopy` for copying into an existing array, `Arrays.copyOf` / `copyOfRange` for allocating ones, `clone()` for a full quick copy — all are JVM-intrinsic backed and `copyOf` delegates to them. Copies are shallow; a manual loop is only competitive for primitive arrays where the JIT vectorizes it.

