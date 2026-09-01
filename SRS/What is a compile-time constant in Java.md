<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What is a compile-time constant in Java?

> [!abstract] Short answer
> A **constant variable**: a `final` variable of a **primitive** type or **`String`**, **initialized in its declaration** with a **constant expression**. The compiler treats that name as the value itself. `final Integer n = 10;` is not one. A blank `final` assigned in a constructor or `static` block is not one. Effectively final locals are not one.

## Constant variable vs any `final`

A constant expression is a primitive or `String` value built only from literals (including text blocks), casts to those types, unary `+ - ~ !` (not `++`/`--`), arithmetic and shifts, comparisons except `instanceof`, `==`/`!=`, bitwise operators, `&&`/`||`, `? :`, parentheses, and names of **other** constant variables (`Integer.MAX_VALUE / 2`, `"x" + Long.MAX_VALUE`). No method calls, no `new`, no `null`. Constant `String`s are interned. [[What does the final keyword mean in Java]] is the broader modifier; [[How would you explain effectively final]] is the lambda capture rule — neither is enough by itself.

```d2
direction: down
f: "final variable" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
cv: "constant variable\nprimitive or String\ninitialized with a constant expression" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}
no: "not constant:\nInteger, blank final, new, method call" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}

f -> cv
f -> no
```

**Fig. 1.** Compile-time constants are a **subset** of `final`. Wrappers, arrays, and `final` assigned later never qualify.

A field that is a constant variable is **resolved at compile time** to its initializer value. For a `static` one, other classes’ binaries typically contain that value with **no field access** — change the constant and **recompile the clients**, or they keep the old number. Reading that `static` field also does **not** initialize its declaring class. Uses include `case` labels, `while (true)` / dead-code reachability, and assignment of a small constant `int` to `byte`/`short`/`char` (and then to `Byte`/`Short`/`Character`). [[What are the autoboxing rules when assigning a primitive to a wrapper]] is that last conversion; [[What is the JVM class constant pool]] is a different “constant” (class-file entries), not this language rule.

```java
public final class CompileTimeConstant {
    static final int N = 10;                 // constant variable
    static final String HI = "hi" + "!";     // constant String, interned
    static final int HALF = Integer.MAX_VALUE / 2;
    static final Integer BOX = 10;           // not a constant variable
    static final int BLANK;
    static {
        BLANK = 10;                          // blank final — not a constant variable
    }

    public static void main(String[] args) {
        byte b = N;                          // constant int that fits in byte
        switch (N) {
            case 5 + 5:
                System.out.println(b);
                break;
            default:
                break;
        }
        System.out.println(HI);
        System.out.println(HALF);
        System.out.println(BOX);
        System.out.println(BLANK);
        // byte tooBig = 128;                // does not compile
        // case Math.abs(10):                // not a constant expression
    }
}
```

**Listing 1.** `N`, `HI`, and `HALF` are compile-time constants. `BOX` is a wrapper. `BLANK` is only `final`. `case` and `byte b = N` need a constant expression.

> [!warning] `final` plus a literal is not always a compile-time constant
> `static final int x; static { x = 1; }` is `final`, not a constant variable — clients see a real field, and using `x` initializes the class. `final Integer n = 1;` boxes; it is not a constant variable. `Math.PI` works because it is a `static final double` initialized with a literal, not because `Math` is special. `Math.abs(1)` is a call and is not constant.

> [!tip] Interview answer
> A compile-time constant is a `final` primitive or `String` initialized in the declaration with a constant expression — literals, arithmetic, and other such constants, not method calls. The compiler inlines that value, which is why `byte b = 10` and `case` labels work, and why changing a `public static final int` without recompiling callers leaves the old number in their binaries. `final Integer` and a `final` set in a static block do not count.
