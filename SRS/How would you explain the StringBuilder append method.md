<!--
reps: 0
priority: 0
-->
#Java/StringBuilder #Java/String #SRS

# How would you explain the StringBuilder append method

> [!abstract] Short answer
> **`append` adds characters at the end of the builder and returns `this` for chaining.** `sb.append(x)` is the same as `sb.insert(sb.length(), x)`. Overloads convert most arguments as if by `String.valueOf`, then copy those chars into the buffer. A `null` `String`, `StringBuffer`, `CharSequence`, or `Appendable` argument appends the four characters `"null"` — it does not throw. Length grows; if length would exceed **capacity**, the internal buffer is enlarged. Not safe across threads.

## End of the sequence, then maybe grow

The principal operations are `append` (tail) and `insert` (at an index). Primitive and `Object` overloads are specified as `String.valueOf(...)` then append those characters. `append(char)` increases length by 1. `appendCodePoint` appends `Character.toChars` and grows length by `Character.charCount(codePoint)`.

`append(String)` copies the argument in order. `null` → `"null"`. Same `"null"` rule for `append(StringBuffer)` and for `Appendable.append(CharSequence)` (including a `null` `CharSequence`). A `CharBuffer` may append only `position`..`limit`, not the whole array. The three-arg `append(s, start, end)` copies `[start, end)`; a `null` `s` is treated as the sequence `"null"`. Bad `start`/`end` → `IndexOutOfBoundsException`.

Each call returns the same `StringBuilder`, so `sb.append(a).append(b)` is one buffer. Capacity starts at 16 (or 16 + seed length). Overflow allocates a larger buffer; you can `ensureCapacity` first. `toString()` then copies to a new `String`; further `append`s do not change that snapshot ([[How would you explain java.lang.StringBuilder]]).

In a loop, `append` on **one** builder avoids the copy-the-prefix cost of `s = s + piece` ([[How would you explain performance pitfalls of naive string concatenation]]). `StringBuffer.append` is the synchronized twin.

```d2
direction: right
before: "length n · capacity C" {
  width: 200
  height: 45
}
ap: "append(x)\nvalueOf / copy / \"null\"" {
  width: 240
  height: 50
}
after: "length n+|x|\ngrow buffer if n+|x| > C" {
  width: 240
  height: 50
}

before -> ap -> after
```

**Fig. 1.** Append is always at index `length()`. Capacity is storage; length is the live character count.

```java
public class AppendDemo {
    static String label(String name, int n) {
        StringBuilder sb = new StringBuilder(32);
        return sb.append("id=").append(name) // name == null → "null"
                .append(", n=").append(n)
                .toString();
    }
}
```

**Listing 1.** Chained `append` returns `this`. `toString()` is a snapshot; the `int` overload uses `String.valueOf`.

> [!warning] `null` is the word null; `append` is not `+` on a `String`
> Class-wide “`null` argument → NPE” does **not** apply to these append overloads: they write `"null"`. Sharing one `StringBuilder` across threads is unsafe. `append(CharSequence)` on a `CharBuffer` is not always the full backing array. Do not assume `append` interns anything ([[How would you explain java.lang.String]]).

> [!tip] Interview answer
> **`append` mutates the builder at the end and returns `this`.** Most overloads are `valueOf` then copy; `null` String/CharSequence becomes `"null"`. Length grows, capacity grows when needed. Use one builder in a loop; `toString` when you need a `String`.
