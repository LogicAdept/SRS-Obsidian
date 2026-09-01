<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# How does the Java char type relate to int?

> [!abstract] Short answer
> `char` is a **16-bit unsigned** integral type (0…65535) that holds one UTF-16 **code unit**. `int` is a **32-bit signed** two’s-complement type. A `char` widens to `int` by **zero-extension** (so `'\uFFFF'` becomes `65535`, not `-1`). Arithmetic on `char` uses numeric promotion to `int`, so `c + 1` and `'a' + 'b'` are `int` values. Unicode **code points** above U+FFFF need an `int` (or a two-`char` surrogate pair), not one `char`.

## Unsigned 16-bit value inside a signed 32-bit arithmetic world

`char` sits with `byte`, `short`, `int`, and `long` as an integral type, but unlike the others it is unsigned and denotes a UTF-16 code unit (`'\u0000'`…`'\uffff'`). `int` ranges from `-2147483648` to `2147483647`. Widening primitive conversion includes `char` → `int` (also to `long`/`float`/`double`). That widen **zero-extends**; a signed `byte`/`short` **sign-extends**. Narrowing `int` → `char` keeps the low 16 bits and needs a cast, except when a constant `int` fits in `char`. [[Is the Java char type signed or unsigned]] and [[What is the value range of the Java char type]] are those two facts in isolation.

```d2
direction: down
ch: "char\n16-bit unsigned\nUTF-16 code unit" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
widen: "widen to int\nzero-extend" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
in: "int\n32-bit signed\ncode point APIs" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
narrow: "(char) n\nlow 16 bits" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}

ch -> widen -> in
in -> narrow -> ch
```

**Fig. 1.** `char` is the 16-bit unsigned code unit. `int` is the wider signed integer and the type used for full Unicode code points.

In arithmetic, `byte`/`short`/`char` promote to `int`, so the type of `c + 1` is `int`. That is why `char next = c + 1;` does not compile and `char next = (char) (c + 1);` does. `'a' + 'b'` is `195`, not `"ab"`: both operands are `char`, numeric `+` adds the code-unit values. String concatenation needs a `String` operand (`"" + 'a' + 'b'`). [[Why does adding two char values not concatenate them in Java]] and [[How does numeric promotion work in Java arithmetic expressions]] are those two operators.

A `char` is a BMP code point or a surrogate code unit. Supplementary characters (U+10000…U+10FFFF) are two `char`s in UTF-16, or one `int` code point. `Character` methods that take `char` cannot see those supplementary characters; methods that take `int` can. Character literals themselves only cover `\u0000`…`\uffff`.

```java
public final class CharAndInt {
    public static void main(String[] args) {
        char c = 'A';
        int code = c;                   // 65, implicit widening
        char next = (char) (c + 1);     // 'B' — c + 1 is int

        System.out.println('a' + 'b');  // 195, not "ab"
        System.out.println("" + 'a' + 'b'); // ab

        int fromMaxChar = '\uFFFF';     // 65535, not -1 (zero-extend)
        char wrap = (char) 65_536;      // 0 — low 16 bits of 0x10000
        int grinning = 0x1F600;         // supplementary code point; not one char
        System.out.println(code);
        System.out.println(next);
        System.out.println(fromMaxChar);
        System.out.println((int) wrap);
        System.out.println(grinning);
    }
}
```

**Listing 1.** Widen `char` to `int` without a cast; narrow back with `(char)`. High `char` values stay non-negative as `int`. An emoji code point does not fit in one `char`.

`byte` to `char` is not a simple widen: it is widen-to-`int` then narrow-to-`char`, because `byte` is signed and `char` is unsigned. You write an explicit cast. [[Why is the Java char type 16 bits]] is the UTF-16 history behind that 16-bit width.

> [!warning] `char` arithmetic is `int` arithmetic, and `\uFFFF` is not `-1`
> `'a' + 'b'` adds 97 and 98. Assigning `c + 1` back to `char` needs a cast; the add already overflowed into `int`. Do not treat a `char` as a signed 16-bit `short`: widening to `int` **zero-fills**, so the largest `char` is `65535`. One `char` is also not “a Unicode character” once you leave the BMP — that value is an `int` code point or a surrogate pair.

> [!tip] Interview answer
> **`char` is an unsigned 16-bit UTF-16 code unit; `int` is a signed 32-bit integer.** A `char` widens to `int` by zero-extension, and `char` math is done as `int`, so `'a' + 'b'` is `195` and `c + 1` needs a cast to store as `char`. Full Unicode code points, including emoji, are `int` values (or two `char`s), not a single `char`.
