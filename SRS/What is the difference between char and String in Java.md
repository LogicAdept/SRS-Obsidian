<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/String #SRS

# What is the difference between `char` and `String` in Java?

> [!abstract] Short answer
> `char` is a **16-bit unsigned primitive**: one UTF-16 **code unit**, written in **single quotes** (`'A'`). `String` is an **immutable class**: a **sequence** of Unicode code points, written in **double quotes** (`"A"`, `""`). `'A'` and `"A"` are different types. Compare `char` with `==`; compare `String` content with `equals` (or `compareTo`), not `==`.

## One code unit vs a sequence object

`char` sits with `byte`/`short`/`int`/`long` as an integral type. Its range is `'\u0000'`…`'\uffff'` (0…65535). A character literal always holds **exactly one** UTF-16 unit; there is no empty `char`, and a supplementary-plane character is **two** `char`s (a surrogate pair) or an `int` code point — not one `char`. Fields default to `'\u0000'`; a `char` cannot be `null`. [[Is the Java char type signed or unsigned]] and [[How does the Java char type relate to int]] are that numeric picture.

```d2
direction: down
ch: "char\nprimitive, 16-bit\n'A'" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
st: "String\nclass, sequence\n\"A\"  \"\"" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
eqc: "== is the value" {
  width: 200
  height: 45
  style.fill: "#bbdefb"
}
eqs: "equals is the text\n== is the object" {
  width: 240
  height: 70
  style.fill: "#c8e6c9"
}

ch -> eqc
st -> eqs
```

**Fig. 1.** Quotes pick the type. `char` is a number; `String` is a reference to an unchanging sequence.

`String` is a reference type. A string literal (or text block) names a `String` instance; constant strings are interned so the same literal is the same object. The value does not change after creation. `+` concatenates when at least one operand is `String`; `'A' + 'B'` is **`int` 131**, not `"AB"`, because both sides are integrals. [[Why does adding two char values not concatenate them in Java]] is that `+`. `==` on two `String`s asks whether they are the **same object**; `s.equals(t)` tests the sequence. Distinct objects with the same text compare `false` with `==`. A `String` field defaults to `null`. [[Why is java.lang.String immutable and final]] and [[What does the String intern method do in Java]] are the object-side rules; [[Why should arbitrary objects not be compared with double equals in Java]] is the `==` habit.

```java
public final class CharVsString {
    public static void main(String[] args) {
        char c = 'A';
        String s = "A";
        String empty = "";
        // char none = '';                 // does not compile

        System.out.println(c == 'A');      // true: same code unit
        System.out.println(s.equals("A")); // true: same characters
        System.out.println(s == new String("A")); // false: two objects

        System.out.println('A' + 'B');     // 131, not "AB"
        System.out.println("A" + "B");     // AB

        System.out.println("\uD83D\uDE00".length()); // 2 code units, one emoji
        System.out.println(empty.length());          // 0
        System.out.println(c);
        System.out.println(s);
    }
}
```

**Listing 1.** `'A'` vs `"A"`. `char` `+` is arithmetic. `String` `+` concatenates. `length()` counts UTF-16 units; a single supplementary character is two `char`s. [[How do you turn a Java string into a char array]] is the sequence as `char[]`.

> [!warning] `"A"` is not a one-character `char`, and `==` is not `equals`
> Single quotes vs double quotes is a type error waiting to happen (`char c = "A"` does not compile). `char` is one code unit, not “one Unicode character” for anything above U+FFFF. Two interned `"hi"` literals can look equal with `==`; `new String("hi")` will not. Use `equals`.

> [!tip] Interview answer
> `char` is a 16-bit primitive, one UTF-16 code unit, written `'A'`, compared with `==`. `String` is an immutable object holding a sequence, written `"A"`, possibly empty, possibly `null`, compared with `equals`. `'A' + 'B'` adds integers; `"A" + "B"` concatenates. A character outside the BMP is two `char`s inside a `String`, not one `char`.
