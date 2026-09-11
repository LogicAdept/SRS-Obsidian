<!--
reps: 0
priority: 0
-->
#Java/Versions/11 #SRS

# What methods were added to String after Java 8

> [!abstract] Short answer
> **Java 11 added `isBlank`, `strip`/`stripLeading`/`stripTrailing`, `lines`, and `repeat`; Java 12 added `indent` and `transform`; Java 13 added `formatted`, `stripIndent`, and `translateEscapes`. The underlying storage also changed in 9 — compact strings. `isEmpty` is Java 6, not 11, and `chars()`/`codePoints()` came with 8's CharSequence default methods.**

## The version-attributed set

Java 11's batch is the interview staple: `strip` is Unicode-aware whitespace trimming (`Character.isWhitespace`) while legacy `trim` cuts only chars `<= U+0020`; `lines()` splits on line terminators including `\r\n`; `repeat(n)` throws `IllegalArgumentException` on negative counts. Java 12's `transform(Function)` is a pipeline helper — chain a function without nesting calls; `indent(n)` shifts a block left or right with normalization. Java 13's trio supports the text-block story: `formatted` is `format` as an instance method, `stripIndent` implements the text-block incidental-indentation removal, `translateEscapes` processes `\n`/`\t` escapes into real characters ([[What are text blocks]]).

```java
public class V41_StringMethods {
    public static void main(String[] args) {
        String s = "  Java 21  ";
        System.out.println("isBlank=" + "   ".isBlank());                        // 11
        System.out.println("strip=[" + s.strip() + "]");                          // 11
        System.out.println("repeat=[" + "ab".repeat(3) + "]");                    // 11
        "x\ny".lines().forEach(l -> System.out.println("line:" + l));             // 11
        System.out.println("indent=[" + "x".indent(2).stripTrailing() + "]");     // 12
        System.out.println("transform=[" + "5".transform(v -> Integer.parseInt(v) * 2) + "]"); // 12
        System.out.println("formatted=[" + "%s/%d".formatted("a", 7) + "]");      // 13
        System.out.println("stripIndent: " + "  hi\n  yo".stripIndent().replace("\n", "|") + " // 13");
        System.out.println("translateEscapes length=" + "a\\tb".translateEscapes().length()); // 13
    }
}
```

**Listing 1.** Verified on JDK 21 (V41_StringMethods in empirics): `isBlank=true`, `strip=[Java 21]`, `repeat=[ababab]`, `line:x` / `line:y`, `indent=[  x]`, `transform=[10]`, `formatted=[a/7]`, `stripIndent: hi|yo // 13`, `translateEscapes length=3` (out/V41_StringMethods.txt).

```d2
direction: right
j11: "Java 11\nisBlank, strip, lines, repeat" { style.fill: "#e8f5e9"; width: 250; height: 70 }
j12: "Java 12\nindent, transform" { style.fill: "#e3f2fd"; width: 200; height: 70 }
j13: "Java 13\nformatted, stripIndent, translateEscapes" { style.fill: "#fff3e0"; width: 300; height: 70 }
j11 -> j12 -> j13: ""
```

**Fig. 1.** String API growth after 8, one bucket per release.

> [!warning] strip versus trim is a Unicode difference, not a cosmetic one
> `"\u2000x".trim()` keeps the char (2000 > 0x20), `"\u2000x".strip()` removes it — mixing them in a migration changes string content, not just style. And `repeat(-1)` is an `IllegalArgumentException`, not an empty string ([[How would you explain java.lang.String]]).

> [!tip] Interview answer
> **After 8: Java 11 gave String isBlank, Unicode-aware strip, lines, and repeat; 12 added indent and transform; 13 added formatted, stripIndent, and translateEscapes alongside text blocks. The classic follow-up: strip differs from trim because it trims all Unicode whitespace, and the backing store changed in 9 with compact strings.**
