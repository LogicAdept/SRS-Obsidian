<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #SRS

# How does Java represent data in memory?

> [!abstract] Short answer
> The JVM spec fixes the **value ranges**, not the physical layout. Integral types are **signed two's-complement** integers (`byte` 8, `short` 16, `int` 32, `long` 64 bits); `char` is a 16-bit **unsigned** code unit; `float`/`double` are **IEEE 754** binary values; text is **UTF-16** sequences, and since JDK 9 `String` stores its bytes in a compact Latin-1/UTF-16 form (`byte[] value` + `coder`). `boolean` has **no dedicated bytecode**: it is compiled to `int` (1 = true, 0 = false), and a `boolean[]` is accessed by `byte` instructions. Object layout is explicitly **implementation-defined** — [[What are the JVM run-time data areas]], [[How do you calculate the memory footprint of a Java object]].

## What the spec fixes and what it leaves open

- **Integral types** — two's-complement, big enough to hold their range; `char` is the unsigned exception (U+0000–U+FFFF).
- **Floating point** — IEEE 754 `binary32`/`binary64` semantics with the usual `Infinity` / `NaN` values; the exact set of values and rounding is fixed by the spec, not by the FPU.
- **`boolean`** — no `boolean`-only instructions; expressions compile to `int` where compilers must use **1 for true, 0 for false**. `newarray boolean` creates a real boolean array read/written via `baload`/`bastore`; HotSpot stores **8 bits per element**.
- **References** — pointers to a class instance or array, plus the special `null`. The spec does **not** mandate how an object is laid out: "the JVM does not mandate any particular internal structure for objects."
- **In practice (HotSpot, 64-bit)** — an object is a **mark word** (8 bytes) + **class pointer** (4 bytes with compressed oops) + fields, padded to 8 bytes; a `String` object holds `byte[] value`, `int hash`, `byte coder`, `boolean hashIsZero` (JDK 21 `javap -p`), and its data array lives as a separate heap object.

```java
public final class Represent {
    public static void main(String[] args) {
        int i = -1;                    // 0xFFFFFFFF: two's-complement
        System.out.println(Integer.toBinaryString(i));
        char c = 'A';                  // unsigned 16-bit code unit
        int cp = "A😀".codePointAt(1); // supplementary: 2 UTF-16 units
        boolean[] flags = {true, false};
        System.out.println(c + " " + cp + " " + flags.length);
    }
}
```

**Listing 1.** `-1` prints as 32 ones — two's-complement at the language level. `"A😀"` is two UTF-16 code units (a surrogate pair); `codePointAt(1)` recovers the supplementary code point.

```d2
direction: right
lang: "Language view" {
  width: 250
  height: 110
  style.fill: "#e3f2fd"
  i: "int −1\n0xFFFFFFFF" {
    width: 170
    height: 44
  }
  b: "boolean" {
    width: 120
    height: 44
  }
}
spec: "JVM value model" {
  width: 280
  height: 110
  style.fill: "#fff8e1"
  t: "two's-complement\nIEEE 754\nint-encoded boolean" {
    width: 230
    height: 60
  }
}
impl: "HotSpot layout\n(mark + klass + fields,\n8-byte padding)" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
lang -> spec: "fixes ranges"
spec -> impl: "layout is\nimplementation-defined"
```

**Fig. 1.** The language fixes value semantics; the JVM spec fixes the value model; the physical layout (header, padding, endianness in memory) belongs to the implementation.

> [!warning] Byte order is not part of the language
> The class file format is big-endian, but nothing in the spec dictates the **in-memory** byte order of an `int` on your CPU — HotSpot on x86 stores it little-endian. Code that inspects raw bytes via `Unsafe` or `MemorySegment` must not assume either order. Also, `boolean` sizes are observable only through arrays and serialization, not through "sizeof(boolean)" — the language has none.

> [!tip] Interview answer
> The spec fixes values, not bytes: integers are signed two's-complement (`char` unsigned 16-bit), floats are IEEE 754, text is UTF-16 with compact Latin-1 storage inside `String` since JDK 9. `boolean` is compiled to `int` with 1/0 encoding and boolean arrays ride on `byte` instructions. Object layout — headers, compressed oops, padding — is deliberately implementation-defined; HotSpot uses a mark word plus class pointer.
