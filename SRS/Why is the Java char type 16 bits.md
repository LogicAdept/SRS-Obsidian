<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# Why is the Java `char` type 16 bits?

> [!abstract] Short answer
> Java was designed when Unicode itself was a **fixed-width 16-bit** encoding. `char` stayed 16 bits when Unicode grew past U+FFFF: the language represents text as **UTF-16 code units**, not as 32-bit code points and not as C’s 8-bit `char`. `Character.SIZE` is 16; `Character.BYTES` is 2. Supplementary characters (U+10000…U+10FFFF), including many emoji, need **two** `char`s — a surrogate pair.

## Unicode grew; `char` did not widen

The language’s integral primitives are 8/16/32/64-bit two’s-complement plus `char`: a **16-bit unsigned** integer that is one UTF-16 unit. For U+0000…U+FFFF the code point and the `char` value match. Code points above U+FFFF use a high surrogate (U+D800…U+DBFF) plus a low surrogate (U+DC00…U+DFFF). Widening `char` to 32 bits would have broken every `String`, array, and JNI layout. Java 5 added **code-point** APIs (`int` in `Character` / `String`) instead of changing the primitive. [[What is the value range of the Java char type]] is 0…65535; [[Is the Java char type signed or unsigned]] is unsigned; [[How does the Java char type relate to int]] is promotion and code points.

```d2
direction: down
hist: "Unicode 1.x / early Java\n16-bit fixed width" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
now: "char stays 16-bit\nUTF-16 code unit" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
sup: "U+10000…U+10FFFF\ntwo chars (surrogates)" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}

hist -> now
now -> sup
```

**Fig. 1.** 16 bits is a UTF-16 unit, a compatibility choice after Unicode expanded.

A character literal `'A'` is one unit. `String` is a sequence of `char`. `String.length()` counts **units**, not user-perceived characters. `Character.charCount(codePoint)` is 1 or 2; `toChars` writes the pair. `Character` still wraps a single `char`, which is why there is no `Character(int)` code-point constructor. C `char` is a different type (often 8-bit); Java’s 8-bit integer is `byte`. [[What is the difference between char and String in Java]] is one unit vs a sequence; [[Why does Character reject an int constructor argument]] is `char` vs code point; [[How many bits are in one Java byte]] is the 8-bit neighbour; [[Why does adding two char values not concatenate them in Java]] is numeric `char`.

```java
public final class CharIsSixteenBits {
    public static void main(String[] args) {
        System.out.println(Character.SIZE);   // 16
        System.out.println(Character.BYTES);  // 2
        System.out.println(Character.MAX_VALUE + 0); // 65535

        int grinning = 0x1F600;               // supplementary emoji
        System.out.println(Character.charCount(grinning)); // 2
        char[] pair = Character.toChars(grinning);
        String s = new String(pair);
        System.out.println(s.length());       // 2 code units
        System.out.println(s.codePointCount(0, s.length())); // 1 code point
    }
}
```

**Listing 1.** Width is 16 bits per `char`. A supplementary code point occupies two units in a `String`.

> [!warning] One `char` is not “one character on screen”
> BMP letters fit in one `char`. Many emoji and historic scripts do not. `char c = 0x1F600;` does not compile as a character literal of that code point; you need a surrogate pair or an `int` code point. Do not call Java `char` “two-byte ASCII” or “always one glyph.”

> [!tip] Interview answer
> `char` is 16 bits because Java adopted Unicode when Unicode was a 16-bit encoding, and the primitive was never widened. Today each `char` is one UTF-16 code unit. Characters above U+FFFF take two `char`s. That is also why `char` is not C’s 8-bit `char`.
