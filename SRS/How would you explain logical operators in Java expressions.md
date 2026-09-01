<!--
reps: 0
priority: 0
-->
#Java/Language/Operators/Logical #SRS

# How would you explain logical operators in Java expressions?

> [!abstract] Short answer
> `!` flips a `boolean`. `&`, `|`, and `^` are the eager boolean AND, inclusive OR, and XOR: both operands run, then unbox if needed. `&&` and `||` are the **conditional** forms: the right operand runs only when the left is `true` (`&&`) or `false` (`||`). Operands must be `boolean` or `Boolean`. Integers are not “truthy”; `5 || 6` does not compile.

## Eager `&` `|` `^` versus conditional `&&` `||`

`boolean` has exactly the literals `true` and `false`. There is no C-style “nonzero is true”. The conversion idioms are `x != 0` and `obj != null`. `!`, `&`, `^`, `|`, `&&`, and `||` all require `boolean` or `Boolean` (unbox at run time). Mixing a `boolean` with an `int` is a compile-time error. [[Why cannot Java logical operators be applied to integers]] is that Java-versus-C split; [[Why cannot you assign 0 or TRUE to a Java boolean]] is why `TRUE` and `0` are not boolean values.

**Complement (`!`).** Unary. Operand must be `boolean` or `Boolean`. Result is `boolean`. `!true` is `false`. A `null` `Boolean` unboxes and throws `NullPointerException`. This is not `~`, which is bitwise complement on integers.

**Eager (`&`, `|`, `^`).** Both sides evaluate, left to right, then unbox. `&` is `true` only when **both** are `true`; `|` is `false` only when **both** are `false`; `^` is `true` when they **differ**. Same tokens on two **integers** are bitwise, not logical — the operand types pick the meaning. There is no `^^`. Compound `&=`, `|=`, `^=` exist; there is **no** `&&=` or `||=`. [[How would you explain bitwise operators on integers in Java]] is the integer reading of `&` `|` `^`.

**Conditional (`&&`, `||`).** Same truth table as `&` / `|` **when both operands complete normally**. The right-hand operand is skipped when it cannot change the result: `false && …` does not evaluate the right; `true || …` does not either. Each operand must still be `boolean` or `Boolean`. The expression type is `boolean`. Left-associative; `&&` binds tighter than `||`, so `a || b && c` is `a || (b && c)`. That skip is why `obj != null && obj.m()` is safe and `obj != null & obj.m()` is not.

`? :` is a separate **conditional operator**: its first operand is `boolean` or `Boolean`, and it chooses which of two other expressions to evaluate. [[What is the ternary conditional operator in Java]] is that operator.

```d2
direction: down
left: "evaluate left\nunbox Boolean if needed" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
eager: "& | ^\nalways evaluate right\nthen unbox" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
and: "&&\nright only if left is true" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
or: "||\nright only if left is false" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

left -> eager
left -> and
left -> or
```

**Fig. 1.** Same boolean result as `&` / `|` only if the right side is actually evaluated. `&&` / `||` exist to skip it.

```java
public final class LogicalOperators {
    static int side;

    static boolean bump(boolean v) {
        side++;
        return v;
    }

    public static void main(String[] args) {
        System.out.println(!false);       // true
        System.out.println(true & false); // false
        System.out.println(true | false);  // true
        System.out.println(true ^ true);    // false
        System.out.println(true ^ false);   // true

        side = 0;
        System.out.println(false && bump(true)); // false
        System.out.println(side);                // 0

        side = 0;
        System.out.println(false & bump(true));  // false
        System.out.println(side);               // 1

        int zero = 0;
        System.out.println(false && (1 / zero == 0)); // false; /0 skipped

        Boolean boxed = null;
        System.out.println(false && boxed);     // false; no unbox

        try {
            boolean ignored = false & boxed;    // unbox → NPE
        } catch (NullPointerException e) {
            System.out.println("eager & unbox NPE");
        }

        String s = null;
        if (s != null && s.length() > 0) {
            System.out.println(s);
        }

        // boolean bad = 5 || 6;       // does not compile
        boolean fromInt = (5 != 0);    // C-style idiom
        System.out.println(fromInt);
    }
}
```

**Listing 1.** `&&` skips the right operand; `&` does not. A `null` `Boolean` therefore NPEs on eager `&` even when the left is `false`.

> [!warning] Eager `&` / `|` still unbox, and `&&` is not a bitwise operator
> `false & boxedNull` throws: both sides run, then `Boolean` unboxes. `false && boxedNull` does not. `false & (1 / 0 == 0)` throws `ArithmeticException`; `false && (1 / 0 == 0)` does not. `5 && 6` and `5 || 6` never compile — use `!= 0` if you meant C. Operand types decide whether `&` is logical or bitwise; they do not convert an `int` into a `boolean`.

> [!tip] Interview answer
> Logical operators in Java take `boolean` or `Boolean` only: `!` flips, `&` `|` `^` evaluate both sides, and `&&` / `||` skip the right side when the left already decides. That skip is why null-checks are written `x != null && x.m()` and why a `null` `Boolean` can NPE on `&` even when the left is `false`. Integers are not truthy, so `5 || 6` is a compile-time error, unlike C.
