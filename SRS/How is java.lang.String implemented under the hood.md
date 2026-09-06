<!--
reps: 0
priority: 0
-->
#Java/String #Java/Versions/9 #SRS

# How is java.lang.String implemented under the hood

> [!abstract] Short answer
> **The language type is an immutable UTF-16 sequence; the JDK 9+ HotSpot object is a `byte[]` plus a coder flag (JEP 254 compact strings).** Latin-1 / ISO-8859-1 uses one byte per `char`; otherwise UTF-16 uses two. That is **not** UTF-8 and **not** a public `char[]`. Helpers `StringLatin1` / `StringUTF16` implement `charAt`, `equals`, `hashCode`, and so on. `length()` is `value.length >> coder` (`LATIN1 = 0`, `UTF16 = 1`). `intern()` is native. `toCharArray()` still **copies** into a new `char[]`.

## Compact `byte[]`, UTF-16 API

A `String` has a constant value: Unicode code points, public API in UTF-16 `char`s. Compact strings changed **only the store**. `StringBuilder` / `StringBuffer` / `AbstractStringBuilder` and HotSpot string intrinsics use the same `byte[]` + coder idea. No public API was added for the encoding.

If compaction is on and every `char` fits in Latin-1, `coder` is Latin-1 and `value.length == length()`. Otherwise `coder` is UTF-16 and `value` holds two bytes per code unit. The VM **injects** the static `COMPACT_STRINGS` flag; when compaction is off, bytes are always UTF-16 and Latin-1 branches fold away for the JIT. JDK 6 “compressed strings” (`String.value` as `Object` to `byte[]` **or** `char[]`, 7-bit ASCII) was a different, removed `-XX` experiment — do not describe 9+ that way ([[Is it accurate to say String is backed by a character array internally]]).

`value` and `coder` are VM-trusted (`@Stable` on `value`). Overwriting them after construction is undefined. Hash is cached in `hash`, with `hashIsZero` so a real zero hash is not recomputed. `substring` does **not** keep an offset into the parent: Latin-1 copies a range; UTF-16 copies (and may compress into Latin-1). A package-private constructor may **share** a `byte[]` only when that array is already the exact payload. `intern()` is the native intern pool ([[How do string literals enter the Java string pool]]). Callers never see `value`: `toCharArray()` allocates a new `char[]` ([[How do you turn a Java string into a char array]]).

```d2
direction: down
api: "Public String\nUTF-16 charAt / length / CharSequence" {
  width: 300
  height: 50
}
obj: "JDK 9+ instance\nbyte[] value + byte coder" {
  width: 280
  height: 50
}
l1: "LATIN1 = 0\n1 byte per char" {
  width: 220
  height: 45
}
u16: "UTF16 = 1\n2 bytes per char" {
  width: 220
  height: 45
}
help: "StringLatin1 / StringUTF16\n(+ native intern)" {
  width: 280
  height: 45
}

api -> obj: "implementation only"
obj -> l1: "all chars ≤ 0xFF"
obj -> u16: "otherwise"
obj -> help
```

**Fig. 1.** Compact strings pick Latin-1 or UTF-16 per instance. The API stays UTF-16 code units.

```java
// Conceptual — JDK 21 java.lang.String layout, not compilable API
final class StringLayout {
    byte[] value;       // Latin-1 or UTF-16 bytes; never null
    byte coder;         // 0 = LATIN1, 1 = UTF16
    int hash;           // 0 until computed
    boolean hashIsZero; // true hash is 0, so skip recompute
}
```

**Listing 1.** Conceptual field set (HotSpot 21). `length()` is `value.length >> coder()`. Public code must use `charAt` / `toCharArray`, not these fields.

```java
public class StringHoodDemo {
    static void stillUtf16Api(String s) {
        int units = s.length();                 // char count, not value.length when UTF-16
        char[] copy = s.toCharArray();          // new array; mutate freely
        int points = s.codePointCount(0, units);
        String slice = s.substring(0, units);   // new String (or this if the whole range)
    }
}
```

**Listing 2.** What you can write: UTF-16 indexes, a copied `char[]`, substring as another `String`.

> [!warning] Not UTF-8, not a shared `char[]`, not the public layout
> Compact strings are Latin-1 **or** UTF-16 in a `byte[]` — UTF-8 was an explicit non-goal. Do not read `String.value` by reflection (breaks across 8 vs 9, and the VM trusts the field). `toCharArray().length` is the code-unit length, not the code-point count and not `value.length` for a UTF-16 string. Pre-9 teaching (“`char[]` + offset/count, substring shares”) does not describe this object.

> [!tip] Interview answer
> **API: immutable UTF-16 `String`. JDK 9+ HotSpot: `byte[]` plus Latin-1 vs UTF-16 coder, not UTF-8.** Latin-1 strings use half the bytes of old `char[]`. Helpers do the encoding-specific work; `intern` is native; `toCharArray` copies. Substring copies a new `byte[]` rather than slicing with offset/count.
