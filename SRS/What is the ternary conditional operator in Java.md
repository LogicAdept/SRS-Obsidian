<!--
reps: 0
priority: 0
-->
#Java/Language/Operators/Ternary #SRS

# What is the ternary conditional operator in Java?

> [!abstract] Short answer
> `? :` is Java’s only **ternary** operator — the **conditional operator**. `condition ? ifTrue : ifFalse` is an **expression**: the condition is `boolean` or `Boolean`, exactly **one** arm is evaluated, and that value is converted to a type computed from **both** arms. It can replace some value-producing `if`/`else`. It is not a statement; `if`/`else` chooses **statements**, which have no value.

## One condition, one chosen arm, one result type

Statements run for effect and do not have values, so `if`/`else` chooses one of two **statements**. `? :` does the same exclusive choice for **expressions**. Evaluate the first operand, unbox a `Boolean` if needed, evaluate **only** the chosen arm, convert that value to the expression type (boxing or unboxing allowed), and skip the other arm. A `null` `Boolean` condition NPEs **before** either arm. `!`, `&&`, and `||` often sit in the condition. [[How would you explain logical operators in Java expressions]] is that family.

The operator is **right-associative**: `a ? b : c ? d : e` is `a ? b : (c ? d : e)`. Either arm as a `void` method is a compile-time error. A bare `cond ? a : b;` is not a legal statement. You can rewrite `if`/`else` that **returns or assigns one value** (`return n >= 0 ? n : -n`); you cannot rewrite `void` calls or multi-statement blocks.

Classification of the **second and third** operands picks the kind, then the type:

- **Boolean.** Both arms are boolean expressions. Type is `Boolean` only when **both** arms are `Boolean`; otherwise `boolean`.
- **Numeric.** Both arms are numeric (including wrappers). Same primitive type keeps that type. Primitive `T` with wrapper `T` is **`T`** — `int` plus `Integer` is `int`. Otherwise numeric promotion: `true ? 1 : 2.0` is `double`. A constant `int` that fits in `byte` / `short` / `char` can keep that smaller type. [[How does numeric promotion work in Java arithmetic expressions]] is that ladder; [[What happens when a ternary operator unboxes a null Integer in Java]] is the `null` unbox.
- **Reference.** Anything else. Same reference type, or the other arm’s type if one arm is `null`, or `lub` after boxing. In assignment or invocation context this form is a **poly** expression (Java SE 8+): the target type is pushed into both arms, which is why lambdas can appear as arms.

`Object o = cond ? 0 : someInteger;` does **not** make the expression `Object`. `0` and `Integer` still form a numeric conditional of type `int`; assignment boxes afterward. If `cond` is `false` and `someInteger` is `null`, you NPE on unbox.

```d2
direction: down
cond: "evaluate condition\nunbox Boolean if needed" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
t: "true → evaluate 2nd arm\nconvert to expression type" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
f: "false → evaluate 3rd arm\nconvert to expression type" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

cond -> t
cond -> f
```

**Fig. 1.** The condition always runs. Only one arm runs. Conversion to the type computed from **both** arms happens after the choice.

```java
public final class TernaryConditional {
    static int side;

    static int bump(int v) {
        side++;
        return v;
    }

    static int abs(int n) {
        return n >= 0 ? n : -n; // value-producing if/else
    }

    public static void main(String[] args) {
        System.out.println(true ? 1 : 2);           // 1
        System.out.println(false ? "a" : "b");     // b
        System.out.println(false ? 1 : true ? 2 : 3); // 2  right-assoc
        System.out.println(true ? 1 : 2.0);       // 2.0  type double
        System.out.println(abs(-3));               // 3

        side = 0;
        System.out.println(true ? bump(1) : bump(2)); // 1
        System.out.println(side);                     // 1

        byte b = true ? (byte) 1 : 2;  // type byte: 2 is a fitting constant
        System.out.println(b);

        Integer n = null;
        System.out.println(true ? 0 : n);  // 0; n not evaluated
        // int boom = false ? 0 : n;      // NPE: numeric type int, unbox n

        Boolean boxedCond = null;
        // int z = boxedCond ? 1 : 2;    // NPE: unbox the condition

        Object o = true ? 0 : n;         // still int, then boxed
        System.out.println(o);           // 0

        // cond ? System.out.println("a") : System.out.println("b"); // void arms
    }
}
```

**Listing 1.** Only the chosen arm runs. Mixed numeric arms promote (`1` and `2.0` → `double`). Mixing `int` and `Integer` still types as `int`. Nesting associates to the right.

> [!warning] The type is not “whatever the live arm is”
> `true ? 0 : nullInteger` is safe; `false ? 0 : nullInteger` is not — the expression is `int` either way. Assigning to `Object` does not stop that unbox. `true ? 1 : 2.0` is `double`. A `null` `Boolean` condition NPEs before either arm. `cond ? a : b;` is not a statement, and `void` methods are illegal as arms — use `if`/`else` for actions.

> [!tip] Interview answer
> `? :` is Java’s only ternary operator: a `boolean` or `Boolean` condition, then exactly one of two expressions. The unused arm is skipped, so it is a compact `if`/`else` when both branches produce a value, not a replacement for statement-only branches. The result type is decided from both arms — `int` plus `Integer` is `int`, `1` and `2.0` is `double` — which is why a `null` wrapper on the chosen arm NPEs. Nesting associates to the right.
