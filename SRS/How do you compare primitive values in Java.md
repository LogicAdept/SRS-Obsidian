<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# How do you compare primitive values in Java?

> [!abstract] Short answer
> **With `==` / `!=` and `<` / `<=` / `>` / `>=`.** Those operators compare the primitive values (after numeric promotion). Do not call `equals` on a primitive. `==` on two references is identity, not this. Floating-point `==` is IEEE 754: `NaN` is not equal to itself; `-0.0 == 0.0` is `true`.

## Operators, not `equals`

Equality (`==`, `!=`) is legal for two numeric primitives, two `boolean`/`Boolean` values, or two references. Mixing a number with a `boolean` is a compile-time error. The result type is always `boolean`. `a != b` is `!(a == b)`.

For numbers, both sides undergo binary numeric promotion ([[How does numeric promotion work in Java arithmetic expressions]]): `byte`/`short`/`char` widen to `int`; mixing with `long`/`float`/`double` follows the usual ladder. Then:

- Promoted `int`/`long` — signed integer equality or signed integer order (`<` `<=` `>` `>=`).
- Promoted `float`/`double` — IEEE 754 comparison.

`boolean` uses `==` / `!=` only for equality (`true` equals `true`). There is no `<` on `boolean`. A `Boolean` operand is unboxed first.

Relational `<` `<=` `>` `>=` require operands convertible to a primitive numeric type. `instanceof` is not a primitive comparison.

Objects are a different operator meaning: `==` on two `Integer` references is identity ([[Why should arbitrary objects not be compared with double equals in Java]], [[What is the difference between int and Integer in Java]]). `int == Integer` is numerical equality after unboxing (and can NPE if the wrapper is `null`).

```d2
direction: down
p: "primitive ==  !=  <  >" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
fp: "float/double\nNaN, ±0.0, inf" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}

p -> fp
```

**Fig. 1.** Primitive comparison is the operator on values. Two wrappers are not “primitive comparison.”

```java
public final class ComparePrimitives {
    public static void main(String[] args) {
        int a = 1;
        int b = 1;
        System.out.println(a == b);     // true
        System.out.println(a < 2);      // true
        System.out.println(true == true);

        double nan = Double.NaN;
        System.out.println(nan == nan);   // false
        System.out.println(nan != nan);   // true
        System.out.println(Double.isNaN(nan));
        System.out.println(-0.0 == 0.0);  // true
        System.out.println(-0.0 < 0.0);   // false

        Integer boxed = Integer.valueOf(1);
        System.out.println(a == boxed);   // true — unbox, numeric ==
        // System.out.println(a.equals(b)); // compile error: a is int
    }
}
```

**Listing 1.** Integers and booleans use `==`. `NaN != NaN`. `-0.0` equals `+0.0` but is not `<`. `int == Integer` unboxes.

> [!warning] `==` is a bad “are these the same number?” test for `float`/`double`
> `NaN == NaN` is `false`; `x != x` is the language’s NaN test (`Float.isNaN` / `Double.isNaN` exist too). `-0.0 == 0.0` is `true`, yet `1.0/-0.0` is negative infinity. Binary fractions also break naive equality ([[Why is 0.1 plus 0.2 not equal to 0.3 in Java]]). `a == b == c` is `(a == b) == c` — a `boolean` compared with `c`, not a three-way value test. Two `Integer` values with `==` do not follow these numeric rules.

> [!tip] Interview answer
> **Compare primitives with `==`, `!=`, and the relational operators — never `equals`.** Numbers are promoted first; `boolean` only has equality. For `float`/`double`, remember `NaN` is unordered (`NaN == NaN` is false) and `-0.0 == 0.0` is true. `==` on two wrapper objects is identity, not primitive comparison.
