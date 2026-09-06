<!--
reps: 0
priority: 0
-->
#Java/String #Java/StringBuilder #Java/Performance #SRS

# How would you explain performance pitfalls of naive string concatenation

> [!abstract] Short answer
> **A non-constant `+` always yields a new `String`.** Doing `s = s + piece` (or `s += piece`) in a loop therefore **copies the whole prefix every iteration**. Cost scales with the square of the number of pieces when sizes are similar. One expression `a + b + c` is not that trap: the compiler may use one `StringBuilder` chain or (Java 9+) `invokedynamic` to `StringConcatFactory`. Compile-time constant concat is interned and is not a runtime copy loop. For many pieces, reuse **one** `StringBuilder` and `append`.

## New `String` per `+`, not per source file

`String` is immutable. Run-time concatenation creates a new object unless the expression is a **constant** (`"Hel"+"lo"`, `static final` pieces). A compiler **may** lower a single concatenation expression to `StringBuffer` / `StringBuilder` / `StringConcatFactory` so you do not pay a temporary `String` per `+` **inside that expression**. Java 9 `javac` uses `invokedynamic` for that shape so the runtime can pick a strategy without another bytecode change.

A **loop** is many expressions. Each `s = s + piece` reads the current `s`, builds a longer `String`, and drops the previous one. The k-th step copies about the first k pieces. That is the naive pitfall — not “`+` is always slow.”

Fix: one `StringBuilder` (default capacity 16, grows when full), `append` each piece, `toString()` once ([[How would you explain java.lang.StringBuilder]]). `StringBuffer` if you need a synchronized buffer. `StringJoiner` / `Collectors.joining` for delimited joins ([[How would you explain java.util.StringJoiner]]). Do not intern every piece to “save” concat.

```d2
direction: down
expr: "One expression a + b + c\njavac: builder chain or indy concat" {
  width: 340
  height: 50
}
loop: "Loop: s = s + piece\nnew String each time; copy growing prefix" {
  width: 340
  height: 50
}
fix: "One StringBuilder\nappend… then toString()" {
  width: 280
  height: 50
}

expr -> fix: "optional / compiler"
loop -> fix: "you must"
```

**Fig. 1.** Compiler help applies to **one** concatenation expression. A loop of `+=` is many concatenations.

```java
public class NaiveConcatDemo {
    static String naive(String[] parts) {
        String s = "";
        for (String p : parts) {
            s = s + p; // new String each time; copies s
        }
        return s;
    }

    static String builder(String[] parts) {
        StringBuilder sb = new StringBuilder();
        for (String p : parts) {
            sb.append(p);
        }
        return sb.toString();
    }
}
```

**Listing 1.** Same loop shape; only the builder reuses one buffer. `naive` is fine for tiny `parts`.

> [!warning] `+` in a loop is not “the compiler’s StringBuilder”
> Pre-9 `javac` turned **one** `+` chain into `StringBuilder.append` calls, then `toString`. Java 9+ may use `StringConcatFactory` for that chain. Neither rewrite shares one builder **across loop iterations** of `s += x`. Constant concat is free at run time; a handful of `+` in one return is usually fine. Microbenchmarks that ignore allocation still miss the copy cost.

> [!tip] Interview answer
> **Each run-time `+` makes a new `String`.** In a loop, `s += piece` recopies everything so far. Use one `StringBuilder` (or joining APIs) for many pieces. A single `a + b + c` is a different case: the compiler may already concat it in one shot.
