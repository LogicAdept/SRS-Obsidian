<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What is the remainder of a negative integer in Java?

> [!abstract] Short answer
> **It follows the dividend (the left operand), or is zero.** Integer `%` is defined so that `(a / b) * b + (a % b) == a` with toward-zero `/`. So `-15 % 4` is `-3`, not `1`. The result is negative only when the dividend is negative.

## Sign of `a`, not of `b`

`%` is the remainder of an implied division: left = dividend `a`, right = divisor `b`. After binary numeric promotion, the integer identity is `(a/b)*b+(a%b)` equals `a`. Integer `/` truncates toward zero ([[Why does integer division of 5 by 2 equal 2 in Java]]), so the leftover keeps `a`’s sign:

| `a % b` | `/` toward 0 | `%` |
| --- | --- | --- |
| `5 % 3` | `1` | `2` |
| `5 % (-3)` | `-1` | `2` |
| `(-5) % 3` | `-1` | `-2` |
| `(-5) % (-3)` | `1` | `-2` |
| `-15 % 4` | `-3` | `-3` |

The magnitude of `a % b` is strictly less than the magnitude of `b`. Changing the sign of the **divisor** does not flip the remainder (`5 % 3` and `5 % (-3)` are both `2`). `10 % 4` is `2` and `15 % 4` is `3` for the same reason.

`Math.floorMod(a, b)` is the other convention: remainder has the sign of the **divisor** (or zero). `floorMod(-15, 4)` is `1`. Use that when you want a non-negative slot for a positive modulus (indexes), not `%`.

```d2
direction: down
pct: "a % b\n(a/b)*b + (a%b) == a" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
sign: "sign follows a\n-15 % 4 → -3" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
floor: "Math.floorMod(a, b)\nsign follows b" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

pct -> sign
pct -> floor: "not this"
```

**Fig. 1.** Java `%` is remainder from truncating division. It is not an always-non-negative modulo.

```java
public final class NegativeRemainder {
    public static void main(String[] args) {
        System.out.println(10 % 4);          // 2
        System.out.println(15 % 4);          // 3
        System.out.println(-15 % 4);         // -3
        System.out.println(5 % 3);           // 2
        System.out.println(5 % (-3));        // 2
        System.out.println((-5) % 3);        // -2
        System.out.println((-5) % (-3));     // -2
        System.out.println(Math.floorMod(-15, 4)); // 1
        // System.out.println(-15 % 0);      // ArithmeticException
    }
}
```

**Listing 1.** Negative dividend → negative remainder (unless `0`). `floorMod` with a positive modulus lands in `0 … b-1`.

> [!warning] `%` is a bad wrap for negative indexes
> `array[i % array.length]` is negative when `i` is negative, and that is an `ArrayIndexOutOfBoundsException`, not a wrap to the end. Integer `% 0` throws `ArithmeticException` ([[What is ArithmeticException]]); floating-point `%` does not. `Integer.MIN_VALUE % -1` is `0` (the `/` overflows; the remainder identity still holds).

> [!tip] Interview answer
> **Integer `%` takes the sign of the dividend.** `-15 % 4` is `-3` because `/` truncates toward zero and `(a/b)*b + (a%b)` must equal `a`. The divisor’s sign does not change that. For a non-negative remainder with a positive modulus, use `Math.floorMod`.
