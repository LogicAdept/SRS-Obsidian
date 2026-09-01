<!--
reps: 0
priority: 0
-->
#Java/Language/Operators/Logical #SRS

# Which logical operation and operators you do you know?

> [!abstract] Short answer
> Boolean logic in Java is `!` (complement), eager `&` `|` `^` (AND, inclusive OR, XOR), and conditional `&&` / `||`. Compound forms are `&=` `|=` `^=` — there is no `&&=` or `||=`. Operands are `boolean` or `Boolean`. `==` / `!=` are **equality**, and `? :` is the **conditional** operator; they are not `&`/`&&`-style logical operators.

## Boolean catalog: complement, eager, conditional

**Complement.** `!` flips one `boolean` or `Boolean`. Result is `boolean`. A `null` `Boolean` unboxes and throws. Not `~`.

**Eager (`&`, `|`, `^`).** Both sides run, then unbox. `&` is `true` only when both are `true`; `|` is `false` only when both are `false`; `^` is `true` when they differ. Same tokens on two **integers** are bitwise. [[How would you explain bitwise operators on integers in Java]] is that reading; [[How would you explain logical operators in Java expressions]] is skip-versus-eager and the null-check idiom.

**Conditional (`&&`, `||`).** Same truth table as `&` / `|` when both operands complete normally. The right operand runs only if the left is `true` (`&&`) or `false` (`||`). Integers are illegal: `5 || 6` does not compile. [[Why cannot Java logical operators be applied to integers]] is the C split.

**Compound.** `&=` `|=` `^=` exist. No `&&=` / `||=`.

**Often listed beside them.** `==` / `!=` are equality operators (result `boolean`). On two booleans, `!=` matches `^`. `? :` chooses between two expressions after a `boolean` / `Boolean` condition. [[What is the ternary conditional operator in Java]] is that operator.

```d2
direction: down
bool: "boolean / Boolean operands" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
not: "!  complement" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
eager: "& | ^  eager\n&= |= ^=" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
cond: "&& ||  skip the right\nwhen left decides" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

bool -> not
bool -> eager
bool -> cond
```

**Fig. 1.** Logical operators proper. Equality and `? :` are separate boolean-related operators.

```java
public final class LogicalOperationsCatalog {
    static int side;

    static boolean bump(boolean v) {
        side++;
        return v;
    }

    public static void main(String[] args) {
        System.out.println(!false);        // true
        System.out.println(true & false);  // false
        System.out.println(true | false);  // true
        System.out.println(true ^ true);   // false
        System.out.println(true == true);  // true
        System.out.println(true != false); // true  same as ^

        side = 0;
        System.out.println(false && bump(true)); // false; side == 0
        System.out.println(side);

        side = 0;
        System.out.println(false & bump(true));  // false; side == 1
        System.out.println(side);

        boolean flag = false;
        flag |= true;
        System.out.println(flag);            // true
        System.out.println(flag ? 1 : 0);  // 1

        // boolean bad = 5 || 6;          // does not compile
    }
}
```

**Listing 1.** One example per operator family. `&&` skips `bump`; `&` does not. `!=` on booleans matches `^`.

> [!warning] `&` is not `&&`, and `==` is not a logical AND
> `false & boxedNull` unboxes and NPEs; `false && boxedNull` does not. `&` `|` `^` on ints are bitwise, not a C-style “truthy” test. `a==b==c` is `(a==b)==c`, not a three-way compare. There is no `&&=`.

> [!tip] Interview answer
> Logical operators on `boolean` are `!`, eager `&` `|` `^`, and short-circuit `&&` / `||`, plus compound `&=` `|=` `^=`. `&&` / `||` skip the right side when the left already decides; `&` / `|` never skip. I do not call `==` or `? :` logical operators — they are equality and the conditional operator — and I never apply `&&` to integers.
