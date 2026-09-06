<!--
reps: 0
priority: 0
-->
#Java/StringBuilder #Java/String #Java/Versions/5 #SRS

# How would you explain java.lang.StringBuilder

> [!abstract] Short answer
> **`StringBuilder` (Java 5) is a mutable character sequence with the same operations as `StringBuffer`, and no synchronization.** `append` / `insert` grow an internal buffer whose **capacity** starts at 16 (or 16 plus a seed `String` / `CharSequence`). `toString()` allocates a **new** `String` snapshot; later builder edits do not change it. Use it on **one thread**. Prefer it over `StringBuffer` unless you need a thread-safe buffer. It is not `String`: `String` is immutable; run-time `+` creates a new `String`.

## Append into a growing buffer

Principal ops: `append` (end) and `insert` (at an index). `sb.append(x)` is `sb.insert(sb.length(), x)`. Overloads convert the argument as if by `String.valueOf` (except `append(String)` / `append(StringBuffer)` / some `CharSequence` forms). `append(String)` of `null` writes the four characters `"null"` — it does **not** throw.

Capacity is how many characters fit before a new internal buffer is allocated; overflow grows automatically. `ensureCapacity` is a no-op if the argument is nonpositive. `length()` is the character count, not capacity. `setLength` truncates or pads with `'\u0000'`.

`toString()` copies into a new `String`. The builder remains usable. `StringBuilder` implements `Comparable` but does **not** override `equals`, so natural order is inconsistent with equals — do not use builders as `SortedMap` keys.

`StringBuffer` is the synchronized twin (since 1.0): methods are synchronized where needed so calls on **one** instance serialize. It still does **not** lock a shared *source* you append from. Since JDK 5, `StringBuilder` is the recommended single-thread replacement and is faster under most implementations because it does no synchronization ([[Is StringBuilder faster than StringBuffer without synchronization]]).

A compiler may implement `+` with `StringBuilder`, `StringBuffer`, or `StringConcatFactory`. A **non-constant** `+` still produces a new `String`. In a loop, `s = s + piece` typically copies a longer prefix each time; reuse **one** builder and `append` ([[How would you explain java.lang.String]]). JDK 9+ compact strings also apply to `AbstractStringBuilder` ([[How is java.lang.String implemented under the hood]]).

```d2
direction: down
sb: "StringBuilder\nmutable · unsynchronized · Java 5" {
  width: 300
  height: 50
}
buf: "internal buffer\nlength ≤ capacity; grows on overflow" {
  width: 300
  height: 50
}
ops: "append / insert / delete / reverse" {
  width: 280
  height: 45
}
out: "toString()\nnew String snapshot" {
  width: 260
  height: 45
}

sb -> buf
sb -> ops
ops -> out: "when you need a String"
```

**Fig. 1.** One builder, one buffer, many `append`s, one `toString` when you need an immutable `String`.

```java
public class StringBuilderDemo {
    static String join(String[] parts) {
        StringBuilder sb = new StringBuilder(); // empty, capacity 16
        for (String p : parts) {
            sb.append(p); // null → "null"
        }
        String snapshot = sb.toString();
        sb.append('!'); // does not change snapshot
        return snapshot;
    }
}
```

**Listing 1.** Loop `append` on one instance. `toString()` copies; the builder can keep mutating.

> [!warning] Not a `String`, not a shared buffer, `null` is the word null
> Instances are **not** safe for multiple threads — use `StringBuffer` (and still protect a mutable source). `append(null)` inserts `"null"`. Sharing a builder as a `SortedSet` element is wrong: `compareTo` without `equals`. `+` inside a loop is not the same as one reused builder.

> [!tip] Interview answer
> **`StringBuilder` is a Java 5 unsynchronized mutable buffer, API-compatible with `StringBuffer`.** `append`/`insert` grow capacity from 16; `toString` copies to a new `String`. Prefer it over `StringBuffer` on one thread. For loops, append to one builder instead of `s = s + x`.
