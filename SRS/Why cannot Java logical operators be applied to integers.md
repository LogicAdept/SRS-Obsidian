<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Operators/Logical #SRS

# Why cannot Java logical operators be applied to integers?

> [!abstract] Short answer
> `&&`, `||`, and `!` demand operands of type **`boolean` or `Boolean`**. An `int` is not a boolean, and there is **no** integer-to-boolean conversion, so `5 || 6` and `!0` do not compile. C treats nonzero as true; Java does not. Write `n != 0`. The tokens `&`, `|`, and `^` on two **integers** are **bitwise**, not a substitute for `&&` / `||`. Full operator catalog: [[How would you explain logical operators in Java expressions]].

## Operand type is `boolean`, not “truthy int”

`boolean` has two values, `true` and `false` ([[Why cannot you assign 0 or TRUE to a Java boolean]]). Control-flow tests (`if`, `while`, `for`’s condition, `? :`’s first operand) use the same rule: `boolean` or unboxed `Boolean`, never a silent `int`.

| Tokens | Integer operands | `boolean` / `Boolean` operands |
| --- | --- | --- |
| `&&` `\|\|` `!` | compile-time error | logical (conditional for `&&` `\|\|`) |
| `&` `\|` `^` | bitwise on bits ([[How would you explain bitwise operators on integers in Java]]) | eager logical AND / OR / XOR |
| `~` | bitwise complement | compile-time error (`!` is the boolean flip) |

`&`, `|`, and `^` are **one** pair of tokens with **two** meanings, chosen by operand types. Mixing `boolean` with `int` is also a compile-time error (`true | 1`). Wrappers unbox: `Boolean` is legal for `&&`; a `null` `Boolean` throws `NullPointerException` at run time, it does not become `false`.

```d2
direction: down
tok: "||  &&  !" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
ok: "boolean / Boolean" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
no: "int and other numerics\ncompile error" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
tok -> ok
tok -> no
```

**Fig. 1.** Conditional-and, conditional-or, and logical complement are boolean operators. Integer “truth” is not a conversion.

```java
class Demo {
    static boolean flags(int n, boolean ready) {
        boolean nonzero = n != 0;     // the C idiom, written out
        int bits = n | 0x0f;          // bitwise inclusive OR
        // return n || ready;         // illegal: || is not bitwise
        // return !n;                 // illegal: ! is not ~
        return nonzero && ready;
    }
}
```

**Listing 1.** `n != 0` produces a `boolean`. `n | 0x0f` is bits. `n || ready` does not compile.

That split is **strong typing**: the type of the operand picks the operation and forbids the C overload of “integer used as condition” ([[What does strong typing mean in Java]], [[How would you explain Java primitive data types]]).

> [!warning] `&` and `|` on `boolean` are not short-circuit, and they still are not integer operators
> `ready & expensive()` always evaluates `expensive()`. `ready && expensive()` may skip it. Both forms still require booleans. `5 | 6` is the integer reading (bits 7); `5 || 6` is the illegal logical reading. Do not “fix” `5 || 6` by dropping one `|`.

> [!warning] `if (n)` does not compile either
> The same boolean-only rule applies to `if`, `while`, and the first operand of `? :`. `(n)` is still an `int`. Casts do not invent a boolean conversion: `(boolean) n` is illegal. Unboxing only applies to `Boolean`, not to `Integer`.

> [!tip] Interview answer
> **Java has no truthy integers.** `&&`, `||`, and `!` compile only for `boolean` or `Boolean`; `5 || 6` is an error. Use `n != 0`. `&` / `|` / `^` on ints are bitwise; on booleans they are eager logical operators, not a C-style integer-or.
