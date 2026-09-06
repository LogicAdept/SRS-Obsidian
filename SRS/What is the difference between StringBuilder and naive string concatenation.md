<!--
reps: 0
priority: 0
-->
#Java/StringBuilder #Java/String #Java/Performance #SRS

# What is the difference between StringBuilder and naive string concatenation

> [!abstract] Short answer
> **Naive concatenation is `s = s + piece` (or `s += piece`): each non-constant `+` allocates a new `String` and copies the prefix.** **`StringBuilder` keeps one mutable buffer: `append` each piece, `toString()` once.** A single expression `a + b + c` is not naive in that sense — `javac` may lower it to one builder chain or (Java 9+) `StringConcatFactory`. A loop of `+=` is many concatenations; the compiler does not reuse one builder across iterations.

## New `String` per `+` vs one buffer

`String` is immutable. Run-time `+` creates a new object unless the expression is a constant. A compiler **may** use `StringBuffer` / `StringBuilder` / `StringConcatFactory` to avoid *intermediate* `String`s **inside one expression** ([[How would you explain performance pitfalls of naive string concatenation]]).

Naive loop: the k-th `s = s + piece` copies everything already in `s`. Cost grows with the square of the number of similar-sized pieces.

`StringBuilder.append` writes into the same buffer; capacity starts at 16 and grows on overflow; `toString()` copies to a new `String` that later `append`s do not change ([[How would you explain the StringBuilder append method]]). That is the difference that matters in a loop. `StringBuffer.append` is the synchronized variant.

Do not equate `new StringBuilder().append(a).append(b).toString()` with `a + b` for two pieces — both are fine. The split is **repeated** concat that recopy vs **one** builder.

```d2
direction: down
naive: "Naive: s = s + piece\nnew String each time" {
  width: 300
  height: 50
}
sb: "StringBuilder\nappend into one buffer → toString()" {
  width: 320
  height: 50
}
expr: "One expression a + b + c\ncompiler may concat in one shot" {
  width: 320
  height: 50
}

naive -> sb: "loop of many pieces"
expr -> sb: "optional / javac"
```

**Fig. 1.** Naive means many `+` evaluations. One expression and one builder are different shapes.

```java
public class ConcatVsBuilderDemo {
    static String naive(String[] parts) {
        String s = "";
        for (String p : parts) {
            s = s + p; // new String; copies s
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

    static String oneExpression(String a, String b, String c) {
        return a + b + c; // one concat expression, not a loop
    }
}
```

**Listing 1.** Same loop: `+` vs `append`. `oneExpression` is the case the compiler may rewrite.

> [!warning] `+` in a loop is not “the compiler already used StringBuilder”
> Pre-9 `javac` turned **one** `+` chain into `StringBuilder.append` then `toString`. Java 9+ may use `invokedynamic` / `StringConcatFactory` for that chain. Neither shares a builder across `s += x` iterations. Two-piece `a + b` is not a performance crime.

> [!tip] Interview answer
> **Naive concat builds a new `String` on every `+`; a loop recopies the prefix.** **`StringBuilder` appends into one buffer and copies once in `toString`.** A single `a + b + c` may already be one concat at compile/runtime. For many pieces in a loop, use one builder.
