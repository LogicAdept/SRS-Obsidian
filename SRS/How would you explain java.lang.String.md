<!--
reps: 0
priority: 0
-->
#Java/String #SRS

# How would you explain java.lang.String

> [!abstract] Short answer
> **`java.lang.String` is the language’s immutable sequence of Unicode code points.** Every `"literal"` (and text block) is a `String`. The public API is UTF-16: `length()` / `charAt` count **`char` code units**; a supplementary character is a surrogate pair (two indexes). Values never change after construction, so instances can be shared. Compare with `equals`, not `==`, unless you mean interned identity. Repeated `+` at run time allocates new `String`s; use `StringBuilder` (or a compiler-rewritten concat) for loops.

## Immutable UTF-16 sequence with language support

A `String` has a **constant** value. Constructors and methods copy in; later mutation of a `char[]` you passed in does not change the `String`. `null` arguments throw `NullPointerException` unless a method says otherwise. The class is `final` and implements `CharSequence`, `Comparable<String>`, and `Serializable`.

Indexes are code units. `length()` is that count, not the number of Unicode scalar values. `charAt` can return a surrogate. Use `codePointAt` / `codePoints` when you mean characters. Case mapping follows `Character`’s Unicode version. `equals` / `compareTo` / `equalsIgnoreCase` are **not** locale-sensitive; `Collator` is.

Literals and compile-time string constants are interned; run-time `+` creates a **new** `String` ([[How do string literals enter the Java string pool]]). `==` is interned identity; `equals` is the same `char` sequence. `intern()` is the explicit pool API.

The JDK 9+ object is a compact `byte[]` plus Latin-1 vs UTF-16 coder. That is **not** the contract and not UTF-8 ([[How is java.lang.String implemented under the hood]]). `toCharArray()` still copies UTF-16 units ([[How do you turn a Java string into a char array]]). Mutable text is `StringBuilder` / `StringBuffer` (“string buffers” in the class note).

```d2
direction: down
lang: "Language\nimmutable Unicode sequence · literals · +" {
  width: 320
  height: 50
}
api: "UTF-16 API\nlength / charAt / equals / substring" {
  width: 300
  height: 50
}
cp: "code points\ncodePointAt · surrogates = 2 chars" {
  width: 300
  height: 50
}
mut: "Need mutation?\nStringBuilder / StringBuffer" {
  width: 280
  height: 50
}

lang -> api
api -> cp: "supplementary"
lang -> mut: "loops / append"
```

**Fig. 1.** Explain the type and the UTF-16 API first. Heap layout and builders are supporting facts, not the definition.

```java
public class StringExplainDemo {
    static void demo() {
        String a = "café";
        String b = "café";
        String c = new String(a);          // distinct object; same chars
        boolean interned = a == b;         // true — literals interned
        boolean sameChars = a.equals(c);   // true
        int units = a.length();            // code units
        int points = a.codePointCount(0, units);
        String grown = a + "!";            // new String (not a constant here)
    }
}
```

**Listing 1.** Literal identity vs `equals`, code units vs code points, run-time concat allocates.

> [!warning] `==`, `length()`, and `+` in a loop
> `==` is not content equality except for interned literals / explicit `intern()`. `length() == 1` is not “one character” for an emoji. `equalsIgnoreCase` ignores locale; it is the wrong tool for some languages. Building a string with `s = s + piece` in a loop creates many intermediate `String`s. Do not treat the internal `byte[]` as API.

> [!tip] Interview answer
> **`String` is an immutable UTF-16 sequence of Unicode code points; literals are interned instances of that class.** `equals` compares characters; `==` is identity. Indexes count `char`s, so supplementary characters take two slots. For mutation or heavy concatenation, use `StringBuilder`, not `String` itself.
