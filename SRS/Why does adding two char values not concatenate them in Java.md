<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/NumericPromotion #Java/String #SRS

# Why does adding two `char` values not concatenate them in Java?

> [!abstract] Short answer
> `char` is a **numeric** primitive. `'a' + 'b'` is **integer addition** of the UTF-16 values 97 and 98, so the result is the `int` **195**, not the `String` `"ab"`. `+` concatenates only when **at least one** operand is already a `String`. Write `"" + 'a' + 'b'` (empty string **first**) or `Character.toString('a') + 'b'`.

## One `+`, two meanings — `String` decides

If either operand of `+` is `String`, the operator is string concatenation and the other operand undergoes string conversion. Otherwise both operands must be numeric (or unbox to numeric) and `+` is addition after binary numeric promotion. Two `char`s are not `String`; they widen to `int` and add. `'a' + "b"` **does** concatenate because the right operand is a `String`. `-` is never concatenation. [[What is the difference between char and String in Java]] is the type split; [[How does the Java char type relate to int]] is why 97 appears; [[Why does adding two byte values not compile as a byte in Java]] is the same promotion to `int`.

```d2
direction: down
plus: "x + y" {
  width: 160
  height: 40
}
q: "either operand String?" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
cat: "concatenation\n\"\" + 'a' + 'b' → \"ab\"" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
add: "numeric +\n'a' + 'b' → 195" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}

plus -> q
q -> cat
q -> add
```

**Fig. 1.** Concatenation is not “two characters next to each other.” It is a `String` operand on `+`.

`+` is left-associative even when the meaning switches mid-expression. `'a' + 'b' + ""` is `(97 + 98) + ""` → `"195"`. `"" + 'a' + 'b'` is `("" + 'a') + 'b'` → `"ab"`. A `char` in a string context converts as the **character**, not as its decimal code; an `int` 97 in a string context becomes `"97"`. [[How does numeric promotion work in Java arithmetic expressions]] is the `int` promotion; [[Is the Java char type signed or unsigned]] and [[What is the value range of the Java char type]] are the 16-bit unit, not a one-character `String`.

```java
public final class CharPlusIsNotConcat {
    public static void main(String[] args) {
        System.out.println('a' + 'b');           // 195
        System.out.println("" + 'a' + 'b');      // ab
        System.out.println('a' + 'b' + "");      // 195  (add first)
        System.out.println('a' + "b");           // ab
        System.out.println(Character.toString('a') + 'b'); // ab

        char a = 'a', b = 'b';
        int sum = a + b;                         // int, not String
        // String s = a + b;                     // does not compile
        System.out.println(sum);
    }
}
```

**Listing 1.** Two `char`s add. Put a `String` on the **left** if you want `"ab"`. Trailing `""` is too late.

> [!warning] `'a' + 'b' + ""` is `"195"`, not `"ab"`
> Left-to-right `+` adds the two `char`s before it ever sees the `String`. Do not say “code points” here: `'a'` is the UTF-16 unit 97, and the sum is an `int`, which can be far outside a single `char`. `Character` + `Character` unboxes, then the same `int` add — a `null` operand NPEs.

> [!tip] Interview answer
> `char` is an unsigned 16-bit integer, so `'a' + 'b'` adds 97 and 98 and yields `int` 195. Concatenation happens only if one operand is a `String`. Start with `"" + 'a' + 'b'`; putting `""` at the end is too late because `+` groups left to right.
